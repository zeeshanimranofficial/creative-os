"""Creative OS v2 — Orchestrator (M5).

End-to-end pipeline as an explicit, resumable state machine. The host agent
drives it turn by turn; every run persists to registry/runs/<run_id>.json so
a run survives context/session breaks.

Stages:
  brief -> dna_select -> [approval gate if low confidence] -> compile ->
  job_emitted -> (host generates + vision pre-check) -> qa -> retry loop ->
  composite (components) -> export -> released | escalated

Hard rules enforced here:
  - no generation while a human gate is open
  - one DNA per creative; 9:16 = separate re-layout run
  - QA fail routing via retry_controller (regen vs recomposite, caps, audit)
"""
import json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "registry", "runs")

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dna_selector, prompt_compiler, provider, qa_engine, retry_controller


def _default_brand_config():
    """Private brand config if present (gitignored), else the public example."""
    for name in ("brand.config.sample.json", "brand.config.example.json"):
        p = os.path.join(ROOT, "config", name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError("no brand config — run onboarding first")


def _save(run):
    os.makedirs(RUNS, exist_ok=True)
    run["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(os.path.join(RUNS, run["run_id"] + ".json"), "w") as f:
        json.dump(run, f, indent=1)
    return run


def load_run(run_id):
    with open(os.path.join(RUNS, run_id + ".json")) as f:
        return json.load(f)


def start_run(brief, brand_config_path=None):
    """brief: {topic, headline, hero_description?, support_lines?, platform,
    format, post_type_hint?, bg_variant?('A'|'B'|'C'), slides?}"""
    run = {"run_id": f"run-{int(time.time())}", "stage": "dna_select", "brief": brief,
           "brand_config": brand_config_path or _default_brand_config(),
           "history": []}
    reg = prompt_compiler.load_registry()
    sel = dna_selector.select(reg, brief)
    run["selection"] = sel
    if sel["decision"] == "needs_approval":
        run["stage"] = "awaiting_dna_approval"   # HUMAN GATE — nothing generates past this
        retry_controller.log("human_gate_open", run=run["run_id"], gate="dna_approval", candidates=sel["candidates"])
    else:
        run["dna_id"] = sel["chosen"]
        run["stage"] = "compile"
    return _save(run)


def approve_dna(run, dna_id):
    """Human resolves the gate (chooses a suggested profile or another valid id)."""
    run["dna_id"] = dna_id
    run["stage"] = "compile"
    retry_controller.log("human_gate_resolved", run=run["run_id"], gate="dna_approval", chosen=dna_id)
    return _save(run)


def compile_stage(run):
    assert run["stage"] == "compile", run["stage"]
    brand = json.load(open(run["brand_config"]))
    reg = prompt_compiler.load_registry()
    entry = prompt_compiler.get_entry(reg, run["dna_id"])
    brief = dict(run["brief"])
    brief.setdefault("hero_description", entry.get("working_label", "the DNA hero"))
    a = run.get("series_anchors", {}).get(brief.get("slide_class", "content"))
    if isinstance(a, str):  # pre-lock_mode runs stored a bare path
        a = {"path": a, "lock_mode": "full"}
    compiled = prompt_compiler.compile_prompt(brief, brand, entry,
                                              bg_variant=run["brief"].get("bg_variant", "A"),
                                              series_anchor=(a or {}).get("path"),
                                              lock_mode=(a or {}).get("lock_mode", "full"))
    out = run["brief"].get("output_path", f"/tmp/{run['run_id']}.png")
    job_path, job = provider.new_job(compiled, run["dna_id"], run["run_id"], out)
    run.update({"stage": "job_emitted", "job_path": job_path, "compiled_canvas": compiled["canvas"],
                "reference_images": compiled["reference_images"]})
    run["history"].append("compiled + job emitted; host must vision-open references before generating (QA20b)")
    return _save(run)


def report_qa(run, failed_rules, slide_id=None, results=None):
    """Host runs qa_engine (numeric) + answers vision tasks, then reports here.

    Pass the FULL results map as `results` so coverage is audited: a rule
    nobody evaluated blocks release (FC-09 — unknown is not a pass). Calls
    that omit `results` are treated as zero-coverage and routed to review."""
    st = run.setdefault("slide_states", {})
    sid = slide_id or run["run_id"]
    s = st.setdefault(sid, {"regens": 0, "recomposites": 0})
    ctl = retry_controller.SlideState(sid)
    ctl.regens, ctl.recomposites = s["regens"], s["recomposites"]
    unknown = qa_engine.coverage_gaps(results or {})
    action = ctl.decide(failed_rules, unknown=unknown)
    s["regens"], s["recomposites"] = ctl.regens, ctl.recomposites
    run["stage"] = {"release": "composite", "regenerate": "job_emitted",
                    "recomposite": "composite", "escalate_to_human": "escalated",
                    "needs_review": "qa_review"}[action]
    run["history"].append(f"qa report {sid}: failed={failed_rules or 'none'}"
                          + (f", unresolved={unknown}" if unknown else "") + f" -> {action}")
    _save(run)
    return action


def set_series_anchor(run, anchor_path, slide_class="content", lock_mode="full",
                      force=False, revise=False):
    """Reference-Locked Generation Mode (docs/REFERENCE-LOCKED-GENERATION.md).

    Lock an APPROVED raw slide as the Master Reference for every remaining
    sibling of its repeat family in this run (anti micro-drift).

    DNA GATE (rule 1): this mode is NOT default. It activates only when the
    selected DNA/recipe declares repeat requirements (entry field
    'repetition', or a locked constraint mentioning repeat/same background).
    Pass force=True only on explicit human approval for a DNA that doesn't
    declare them. Never assume all slides share one layout — hook and closing
    slides keep their own treatments (their own slide_class) unless the DNA
    says otherwise.

    lock_mode: 'full' (repeat the whole design, swap content only) or
    'background' (repeat background only, layout free per DNA).

    Doctrine: the master is the SAME DNA instance, not a second DNA. Set only
    after the slide passed full QA + vision review; pass the RAW
    pre-compositing image, never a composited final; siblings always clone
    from this ORIGINAL master, never from slide N-1. Replacing an existing
    master requires revise=True (an explicitly approved revised master)."""
    if not os.path.exists(anchor_path):
        raise FileNotFoundError(f"series anchor not found: {anchor_path}")
    if lock_mode not in ("full", "background"):
        raise ValueError(f"unknown lock_mode '{lock_mode}' (use 'full' or 'background')")
    if not force:
        entry = prompt_compiler.get_entry(prompt_compiler.load_registry(), run["dna_id"])
        declared = bool(entry.get("repetition")) or any(
            ("repeat" in str(c).lower() or "same background" in str(c).lower())
            for c in entry.get("constraints", {}).get("locked", []))
        if not declared:
            raise ValueError(
                f"DNA {run['dna_id']} declares no repeat requirements — Reference-Locked "
                "Generation is DNA-gated (rule 1). Pass force=True only with human approval.")
    anchors = run.setdefault("series_anchors", {})
    if slide_class in anchors and not revise:
        raise ValueError(
            f"master for class '{slide_class}' already set — replacing it requires an "
            "explicitly approved revised master (revise=True), never the latest generation.")
    anchors[slide_class] = {"path": anchor_path, "lock_mode": lock_mode}
    run["history"].append(f"master reference set for family '{slide_class}' "
                          f"(mode={lock_mode}{', revised' if revise else ''}): {anchor_path}")
    return _save(run)


def mark_released(run, final_paths):
    run["stage"] = "released"
    run["final_paths"] = final_paths
    retry_controller.log("released", run=run["run_id"], files=final_paths)
    return _save(run)
