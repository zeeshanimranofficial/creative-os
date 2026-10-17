# CREATIVE OS — AGENT ARCHITECTURE SPEC (v0.1 draft for approval)
Locked decisions: (1) missing DNA → suggest nearest + pre-approval; (2) fully autonomous otherwise;
(3) audit-first. Core principle: **creativity inside the DNA, never outside it.**

---

## 1. Pipeline (single creative)
```
REQUEST (topic, platform, format, brand?)
  → 1. BRAND VALIDATION      load/validate brand config; first-run onboarding if absent
  → 2. PLATFORM POLICY       canvas, safe zones, component policy (e.g., engagement icons:
                             LinkedIn=default-on, IG/FB=design-motivated only), export policy
  → 3. DNA SELECTION         rank approved registry entries by archetype fit; confidence < threshold
                             → nearest-DNA suggestion + WAIT FOR APPROVAL (locked decision 1)
  → 4. TREND RESEARCH (opt)  timely metaphors/angles via web search; log source+date;
                             output constrained to selected DNA's allowed elements
  → 5. PROMPT COMPILE        DNA recipe + brand hex remap + topic actors + reserve clauses
                             (NO px numbers in clauses) + typography ref image + no-dash clause
  → 6. GENERATE (raw)        provider layer, top available image model; reference image attached
                             when linkage mode = image; blueprint-driven when json_only
  → 7. COMPOSE (Python)      exact-4:5/9:16 crop (never stretch), Lanczos resize, brand-critical
                             text/labels/pills/icons/profile blocks rendered programmatically
  → 8. QA STACK (A–F below)  all mandatory checks
  → 9. GATE                  any mandatory fail → classify defect → fix policy (regen vs
                             programmatic) → re-run failed checks; retry caps enforced
  → 10. EXPORT + AUDIT TRAIL PNG/lossless PDF, naming rules, full decision log
```

## 2. QA stack (maps the proven 27-item checklist)
| Layer | Checks | Engine |
|---|---|---|
| A. Config | brand config valid, fonts present, canvas/platform/format legal | Python |
| B. Pixel | 30px margins, dimensions, color snapping, component positions, edge-mean white-frame scan (>249), QA25 margin-column jump (<1.5 flat), QA26 alignment (±4%), QA27 cap-heights (±5%), QA16 footprint (±3%), QA23 clearance (≥10px) | Python, deterministic |
| C. Vision | DNA composition/hierarchy/style fidelity vs reference (or golden for json_only), QA21 geometry, QA22 spacing, style-drift detection | Vision model + explicit criteria + goldens |
| D. Content | copy diff vs intended text, spelling, dash/px prompt-leaks, clone copy-leak (QA27e), clipped text | Vision read + text diff |
| E. Cross-slide | nav kit consistency, typographic scale lock, label placement, shared transform | Python measures + vision confirm |
| F. Release gate | all mandatory pass; defect log; retry budget respected | Controller |

**Fix policy (hard rule):** DNA/visual mismatch → REGENERATE (improved prompt/conditioning), never
patch-to-pass. Programmatic correction only for programmatic elements. Band-fills near copy banned (QA25c).
**Retry caps:** 2 regens per defect class; convergence ceiling detection (two identical-magnitude failures
→ accept documented ceiling or escalate to human) — prevents infinite loops.

## 3. Modules
1. **dna-registry** — normalized index (81 entries, namespaced IDs, status: active/purged/phantom,
   linkage: image/sheet-crop/json_only, hard vs flexible fields). Source of truth. AI cannot write to it.
2. **brand-config** — JSON schema: colors, fonts, logo/DP assets, icon set, canvas rules, restrictions,
   export prefs. First-run interactive onboarding; defaults = documented OS brand. Config can never
   override hard rules silently — conflicts produce an approval request.
3. **platform-policies** — per platform: canvases, safe zones, component policy, export policy.
   4:5→9:16 = independent re-layout + full QA re-run (stretching prohibited).
4. **component-library** — Python renderers: profile strips, wordmarks, nav tabs, swipe arrows,
   engagement icon rows, counter pills, page numbers. Pixel-exact, real fonts.
5. **prompt-compiler** — DNA recipe → generation prompt with proven clause set (continuous-background,
   uppercase lock, no-dash, reserve-without-px, same-cap-height-as-reference for clones).
6. **generation-provider layer** — pluggable image + vision model adapters (no hardcoded vendor).
7. **qa-engine** — `qa.rules.json` (machine-readable QA 1–27 + session patterns), runners per layer.
8. **retry-controller** — defect classification → fix route → budget → escalation.
9. **exporter** — PNG/PDF, dimension/page validation, naming, audit trail writer.
10. **golden-tests** — approved golden creatives as regression set; OS changes must not degrade them.

## 4. Repo structure (open-source release)
```
creative-os/
  README.md  LICENSE  setup/          (install, env vars, model config)
  config/    brand.config.sample.json  platform.policies.json  models.config.json
  registry/  dna.registry.json  references/   (images + sheet crops)
  rules/     qa.rules.json  failure-patterns.md
  components/  compositor/  qa/  agent/   (python packages)
  goldens/   tests/  docs/
```

## 5. Implementation phases (each ends with your approval)
- **M1** dna.registry.json + vision mapping pass (fix F1–F7) — the foundation
- **M2** brand-config + platform-policies + component library + exporter
- **M3** qa.rules.json + QA engine (programmatic layers B/D/E first, vision layer C criteria)
- **M4** agent loop: selection → compile → generate → compose → QA → gate (end-to-end on 1 topic)
- **M5** golden regression set + multi-topic/platform/format test matrix
- **M6** docs, sample configs, licensing, GitHub release

## 6. Open questions (answer when convenient — not blockers for M1)
1. GitHub repo language for docs: English, Roman Urdu, or both?
2. License preference (MIT / Apache-2.0)?
3. Should the 4 missing reference categories (occasions, infographics, vertical-first, before/after)
   be sourced before release, or shipped as a documented coverage gap v1?
