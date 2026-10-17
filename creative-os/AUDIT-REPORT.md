# CREATIVE OS — STEP 1 AUDIT REPORT
Date: 2026-10-17 · Status: for review/approval · No code written, no existing file modified.

---

## 1. Scope & method
Audited: `brand/reference-dna.json` (all 5 collections), `uploads/` (65 files), `brand/BRAND_SYSTEM.md`
(QA 1–27 + sections 1–10), fonts, icons, and this project's session-proven failure patterns.
Method: programmatic JSON parsing, file-existence checks, label extraction, rule classification.

## 2. Asset inventory
| Asset | Count | Status |
|---|---|---|
| Reference images in `uploads/` | 61 | OK (JPEG/PNG) |
| DNA JSON collections (merged) | 5 collections, **81 recipe entries** | OK, heterogeneous schemas |
| Redundant source JSONs in `uploads/` | 2 (`creative_design_dna.json`, `design_dna_library_extended.json`) | Already merged into `brand/reference-dna.json` — safe to archive |
| Brand fonts | 16 statics (Poppins ×8, Playfair ×5, Anton, Dancing Script ×2) | OK |
| Engagement icons | IG set (like/repost/save ×3 colors ×3 sizes) + FB set (×2 colors, 40px) | OK |
| Profile assets | `dp-circle.png`, `font-specimen.png` | OK |

## 3. DNA collections
| Collection | Entries | Schema richness | Reference-image linkage |
|---|---|---|---|
| `design_dna_library` | 22 active (28 − 6 purged) | RICH (14 fields: hero, layout rules, lighting, avoid-list) | ❌ **NO source-image fields — image↔JSON mapping lost** |
| `creative_design_dna` (CD1) | 10 | Medium | ✅ All 10 paths verified present |
| `sage_green_collection` | 24 | Medium (label + dna) | ⚠️ Single sheet image for all 24 (one-to-many) |
| `skincare_neutral_collection` | 15 | Medium (label + dna) | ⚠️ Single sheet image for all 15 (one-to-many) |
| `creative_design_dna_v2` (CD2) | 10 | RICH (incl. prompt_blueprint) | ❌ All 10 phantom (`48643.jpg` etc. never uploaded) — JSON-only by design |

**Purge list (hard exclusion, must be machine-enforced):** DNA_16, 17, 19, 22, 25, 26 — permanently
removed per user order 2026-10-15. Currently encoded only in QA item 20 prose.

## 4. Findings (F1–F8)
- **F1 — Lost image mapping:** `design_dna_library`'s 22 entries have no `source_image` field. ~44 of the
  61 uploads images are unmapped (61 − 10 CD1 − 2 sheets − 3 brand icons − 1 carousel ref − 1 DP source).
  These 44 include the DNA_01–28 originals AND the 6 purged-DNA images (which must be flagged, not used).
  → Requires a one-time vision mapping pass (match each image to its DNA entry) before the registry is built.
- **F2 — ID collisions:** `design_01–10` exists in BOTH CD1 and CD2; `creative_01+` in BOTH sage and
  skincare. Registry must use globally unique namespaced IDs (e.g., `CD1_03`, `CD2_03`, `SAGE_07`, `SKIN_04`).
- **F3 — Schema heterogeneity:** 4 different entry schemas across 5 collections. Registry needs a
  normalization layer mapping all to one canonical schema (id, name, type, source_image(s), palette-remap
  policy, layout DNA, hard constraints, flexible fields, use cases, status: active/purged/phantom).
- **F4 — Redundant JSONs in uploads/** (already merged) → mark as archived in registry, never double-load.
- **F5 — Sheet-derived collections:** sage/skincare entries reference crop regions of one sheet. Registry
  should store crop coordinates per entry (one-time task) so vision QA can compare against the right crop.
- **F6 — Purge enforcement:** exclusion list must be a machine-readable `status:"purged"` field, not prose.
- **F7 — Phantom policy:** CD2 is JSON-only (prompt_blueprint-driven). Registry must mark
  `reference_mode: "json_only"` so vision QA compares against generated golden examples instead of
  a nonexistent reference image. (Proven workable: FB kit + Week 1 were built this way.)
- **F8 — Session-learned rules not yet centralized:** QA 1–27 exists, but several proven failure patterns
  live only in chat history/KIT guides: trailing-dash leak clause, "no px numbers in reserve clauses"
  (prompt-leak), hidden-white-frame edge check (>249 edge mean), model convergence ceilings (2-retry cap),
  copy-leak check after clone regens (QA27e has it; dash/px-leak don't have numbers). → Architecture spec
  consolidates all into the machine-readable rules file.

## 5. QA 1–27 classification (automation mapping)
| Type | Items | Automation |
|---|---|---|
| Fully programmatic (pixel/numeric) | 1–8 core layout, 15 (centering scan), 16 (±3% footprint), 17 (zone scan), 23 (≥10px clearance), 25 (margin-column jump audit), 26 (±4% alignment), 27 (±5% cap-height) | Python, deterministic |
| Vision-model judgment | 20/20b/20c/20d (DNA match), 21 (geometry fidelity), 22 (spacing hierarchy), style drift | Vision QA with explicit criteria + golden examples |
| Hybrid (numeric flag → visual confirm) | 25 (design edges legitimately high), 18 (list rows carry text), 19 (label hierarchy) | Python flags, vision confirms |
| Content QA | spelling/copy verification, leak checks | Vision read at full res + text diff vs intended copy |

## 6. Coverage map (archetype taxonomy vs available DNA)
| Category | Covered by | Gap |
|---|---|---|
| Calendar/announcement | DNA_01/02/03, CD2_02 | Occasion-specific (Eid, Ramadan, 14 Aug, New Year) — **missing** |
| Testimonial/social proof | DNA_04, SKIN_12 | OK |
| Educational/explainer | DNA_09/10, CD2_04/05/06 | True data-infographics (charts/stats/comparisons) — **missing** |
| Question/engagement | DNA_11, CD2_07 | OK |
| Hero-object/conceptual | DNA_05/13/14/15/24/27, CD2_03 | OK |
| Collage/cutout editorial | DNA_02/23/27, CD2_01 | OK (taxonomy tagging needed) |
| Mascot/character | DNA_12/18/20 | OK |
| Grid/multi-tile systems | CD2_09/10 | OK |
| Product/e-commerce | SKIN_01–10, SAGE mockup entries | Non-beauty physical product photography-led — **partial gap** |
| Device/app mockups | SAGE_01/03/09/11–14/20, DNA_21 | OK |
| Vertical-first (9:16 native) | none — all 4:5/1:1 re-laid | **missing** |
| Before/after transformation | none | **missing** |
| Typography-only statements | DNA_04/21/28 | OK |

Per locked policy: gaps = agent reports + suggests nearest DNA with pre-approval; never invents.

## 7. Recommendations (all require your approval before execution)
1. Build `dna.registry.json` — canonical normalized index of all 81 entries with namespaced IDs,
   status flags (active/purged/phantom), linkage mode, and hard/flexible field separation (fixes F1–F7).
2. One-time **vision mapping pass**: match the ~44 unmapped uploads images to DNA_01–28 entries +
   record sheet crop boxes for sage/skincare (fixes F1, F5).
3. Archive the 2 redundant uploads JSONs (move note in registry; files untouched).
4. Convert QA 1–27 + session failure patterns into one machine-readable `qa.rules.json` with
   check-type, threshold, fix-policy, and retry-cap per rule.
5. Acquire designer-approved references for the 4 missing categories (occasions, data-infographics,
   vertical-first, before/after) — human-selected, per DNA policy.
