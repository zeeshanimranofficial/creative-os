# Creative OS v2 — Autonomous AI Graphic Designer Agent

An open-source operating system for an AI agent that designs on-brand social
creatives end-to-end: it takes any **topic + brand + platform**, selects ONE
approved design DNA from a human-curated reference library, generates the
artwork with a top image model, composites brand-critical components
programmatically, runs a layered QA stack against the reference, and
regenerates (never patches) anything that drifts — with human approval gates
exactly where taste and rights decisions belong.

> **Design philosophy:** the reference library is the law. The AI never
> invents a new DNA, never hybridizes two references, and never lets trend
> research or model convenience override the approved visual system.
> Reference = **stage**, topic = **actor**.

## How it works

```
brief ─► DNA selector ─►[human gate if low confidence]─► prompt compiler
      ─► job card ─► image model (host agent) ─► QA engine (layers A–F)
      ─► retry controller (regen / recomposite / escalate) ─► component
         compositor ─► exporter (PNG / carousel-PDF / 9:16 sequence)
```

Every run is a resumable state machine persisted to `registry/runs/`, with a
JSONL audit trail of every decision, regeneration, and human gate.

## Core rules (enforced in code, not vibes)

| Rule | Where |
|---|---|
| One DNA per creative; no hybrids, no invention | `dna_selector.py`, `prompt_compiler.py` |
| Low-confidence match → suggest nearest + human approval BEFORE generating | `dna_selector.py` threshold gate |
| DNA-mismatched output → regenerate; Python only for programmatic elements | `retry_controller.py` classification |
| Purged references stay purged (tombstone hard-block) | compiler raises on tombstoned IDs |
| 4:5 → 9:16 requires an independent re-layout, never a stretch | `exporter.py`, platform policies |
| Trend research may change the actor, never the stage | `trend_research.py` key allowlist |
| New references enter ONLY through paired image+DNA intake with analysis | `config/os.policies.json` |
| Brand onboarding can never relax hard OS rules | `onboarding.py` conflict scan |

## Repository layout

```
creative-os/
├── ARCHITECTURE.md          # full pipeline + module spec
├── AUDIT-REPORT.md          # the audit that shaped the design
├── config/
│   ├── brand.config.example.json   # onboarding output example (generic brand)
│   ├── platform.policies.json      # canvases, icon policies, safe zones per platform
│   ├── qa.rules.json               # QA 1–27 machine-encoded into layers A–F
│   └── os.policies.json            # intake, icon-sourcing, background-system policies
├── lib/
│   ├── dna_selector.py      # transparent scoring + human gate
│   ├── prompt_compiler.py   # brief + brand + DNA → generation prompt
│   ├── provider.py          # model-agnostic job cards + result history
│   ├── qa_engine.py         # numeric checks + vision-task emission
│   ├── retry_controller.py  # regen/recomposite routing, caps, audit trail
│   ├── components.py        # profile strip, engagement icons, nav tabs, arrows
│   ├── exporter.py          # crop-never-stretch, validation, PNG/PDF/sequence
│   ├── orchestrator.py      # resumable end-to-end state machine
│   ├── onboarding.py        # first-run brand questionnaire + validation
│   └── trend_research.py    # research sanitizer (actor-only enrichment)
├── registry/
│   └── dna.registry.example.json   # registry schema with sample entries
└── tests/
    └── golden_tests.py      # known-good must pass, known-bad must fail
```

## What is NOT in this repo

- **Reference images.** A DNA library is built from designs you have the right
  to study. The registry stores *your* analysis (composition DNA, constraints,
  crop boxes) and private paths to *your* reference files. Third-party designs
  are never redistributed here — bring your own references through the intake
  flow, and never copy another brand's logos, handles, or names into output.
- **Private brand kits.** Real brand configs, fonts, profile photos and the
  production registry live outside version control (see `.gitignore`).

## Quickstart

1. `pip install -r requirements.txt`
2. Copy `config/brand.config.example.json` → run the onboarding questions in
   `lib/onboarding.py` with your host agent, or fill it by hand.
3. Add references: image + DNA JSON pairs via the intake policy in
   `config/os.policies.json` (your agent drafts missing DNA for your approval).
4. Drive the pipeline from your agent:
   ```python
   from lib import orchestrator
   run = orchestrator.start_run({
       "topic": "cold email follow-ups",
       "headline": "THE FORTUNE IS IN THE FOLLOW-UP.",
       "platform": "linkedin", "format": "linkedin_carousel", "slides": 9,
   })
   # low confidence? run["stage"] == "awaiting_dna_approval" → human picks
   # then: compile_stage → generate from the job card → report_qa → export
   ```
5. `python tests/golden_tests.py` after any change — golden refs must pass,
   synthetic bad cases must fail.

## The QA stack

- **A — Config:** canvas, DNA match, tombstones, type-system mapping
- **B — Pixel-numeric:** margins, exact brand hexes, reserved zones, strip continuity, keyline clearance
- **C — Vision-vs-reference:** hero dominance, device geometry, spacing hierarchy (the host agent answers emitted vision tasks by actually looking)
- **D — Content:** copy integrity, branding placement rules
- **E — Cross-slide:** series alignment lock, typographic scale lock, nav-kit consistency
- **F — Release gate:** all layers pass → export; DNA-level fail → regenerate; caps exhausted → escalate with audit trail. Never force-release.

## Host agent requirements

This OS is model-agnostic by design: generation happens through whatever
image model your agent runs. The host agent must honor the job-card
contract: open linked reference images with vision **before** generating,
copy-read all rendered text at full resolution **after**, and answer the QA
engine's vision tasks honestly.

## License

Apache-2.0 — see [LICENSE](LICENSE).
