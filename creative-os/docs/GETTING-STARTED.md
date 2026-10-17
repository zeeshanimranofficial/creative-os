# Getting Started

## 1. What you need

- A host AI agent that can: generate images with a modern image model,
  view images ("vision"), run Python, and talk to a human for approvals.
- Python 3.10+ with `pip install -r requirements.txt`.
- Your own reference designs (images you have the right to study) and your
  brand kit (fonts, colors, profile photo, icon set).

## 2. First run — brand onboarding

Have your agent walk the questionnaire in `lib/onboarding.py` (`QUESTIONS`).
`build_config(answers)` validates everything: invalid hexes, a missing real
profile photo, or any attempt to weaken a hard rule (margins, no-initials DP,
single font family…) returns blocking issues instead of a config. Missing
non-required answers fall back to OS defaults.

Save the result with `save_config(config, "yourbrand")` — it lands in
`config/brand.yourbrand.json` (gitignored).

## 3. Build your reference library (the law)

References enter ONLY through the paired intake flow
(`config/os.policies.json → reference_intake_policy`):

1. Provide an image AND its DNA JSON — or let the agent draft the DNA from
   the image for your approval.
2. The agent analyzes the pair against the existing library: schema,
   duplicates, hard-rule conflicts, image↔json agreement.
3. You approve → the entry becomes active in `registry/dna.registry.json`.

Rejected profiles become **tombstones**: permanently blocked IDs the
compiler refuses forever. Template sheets are parsed into per-tile entries
with crop boxes (`linkage.mode = sheet_crop`).

## 4. Produce a creative

```python
import sys; sys.path.insert(0, "lib")
import orchestrator, qa_engine, exporter

run = orchestrator.start_run({
    "topic": "why consistency beats intensity",
    "headline": "SHOW UP SMALL. EVERY DAY.",
    "platform": "instagram", "format": "feed_45",
    "post_type_hint": "educational explainer",
    "bg_variant": "A",
})

if run["stage"] == "awaiting_dna_approval":
    # the OS will not generate — show run["selection"]["candidates"] to the human
    run = orchestrator.approve_dna(run, "DEMO_01")

run = orchestrator.compile_stage(run)
# -> registry/jobs/<id>.json: the agent opens the reference with vision,
#    generates from job["prompt"] at job["canvas"], saves to job["output_path"]

# after generation: numeric QA + answer emitted vision tasks, then
action = orchestrator.report_qa(run, failed_rules=[])   # [] = clean
# "release" -> composite components (lib/components.py) and export:
# exporter.export_post / export_carousel_pdf / export_sequence
```

## 5. The two habits that make it work

- **Copy-read everything.** After every generation, read all rendered text
  at full resolution. Image models drift typography — QA 27 exists for a
  reason, and the fix is REGENERATE from a verified sibling, never patch.
- **Respect the gates.** When the selector or QA escalates to a human,
  that's the system working. Autonomy lives inside the rules, not above them.

## 6. Platform notes

`config/platform.policies.json` carries canvases, icon policies (e.g.
Facebook/Instagram show their own engagement UI — composite your own icon
trio only when the design calls for it), story safe zones, and the hard
rule that 4:5 → 9:16 is an independent re-layout, never a stretch.
