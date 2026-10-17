"""Creative OS v2 — Retry Controller + Audit Trail (M3).

Policy (user hard rules):
- DNA/composition-level fail -> REGENERATE via image model (never Python-patch artwork).
- Programmatic-element fail (strip, icons, tabs, exported dims) -> RECOMPOSITE only.
- Glyph surgery on generated text is banned -> regenerate.
- Caps below; exhausted -> ESCALATE to human with full audit trail. Never force-release.
"""
import json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.join(ROOT, "registry", "audit-trail.jsonl")

POLICY = {
    "max_regens_per_slide": 3,
    "max_recomposites_per_slide": 2,
    "max_vision_rounds": 2,
    "dna_mismatch_action": "regenerate",        # never patch
    "programmatic_fail_action": "recomposite",
    "generated_text_defect_action": "regenerate",  # glyph surgery banned
    "cap_exhausted_action": "escalate_to_human",
}

# layer->failure class
DNA_LEVEL = {"QA05", "QA09", "QA10", "QA13", "QA15", "QA18", "QA21", "QA22", "QA25", "QA26", "QA27", "QA03b"}
PROGRAMMATIC = {"QA01", "QA02", "QA06", "QA07", "QA08", "QA17", "QA19", "QA23"}


def classify(rule_id):
    base = rule_id.split(".")[0]
    if base in PROGRAMMATIC:
        return POLICY["programmatic_fail_action"]
    if base in DNA_LEVEL or base.startswith("QA2"):
        return POLICY["dna_mismatch_action"]
    return POLICY["dna_mismatch_action"]


def log(event, **kw):
    os.makedirs(os.path.dirname(AUDIT), exist_ok=True)
    with open(AUDIT, "a") as f:
        f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event, **kw}) + "\n")


class SlideState:
    def __init__(self, slide_id):
        self.slide_id, self.regens, self.recomposites = slide_id, 0, 0

    def decide(self, failed_rules):
        """failed_rules: [rule_id]. Returns action string; logs every decision."""
        if not failed_rules:
            log("release_gate_pass", slide=self.slide_id)
            return "release"
        actions = {classify(r) for r in failed_rules}
        if "regenerate" in actions:
            self.regens += 1
            if self.regens > POLICY["max_regens_per_slide"]:
                log("escalate", slide=self.slide_id, reason="regen cap", failed=failed_rules)
                return POLICY["cap_exhausted_action"]
            log("regenerate", slide=self.slide_id, attempt=self.regens, failed=failed_rules)
            return "regenerate"
        self.recomposites += 1
        if self.recomposites > POLICY["max_recomposites_per_slide"]:
            log("escalate", slide=self.slide_id, reason="recomposite cap", failed=failed_rules)
            return POLICY["cap_exhausted_action"]
        log("recomposite", slide=self.slide_id, attempt=self.recomposites, failed=failed_rules)
        return "recomposite"
