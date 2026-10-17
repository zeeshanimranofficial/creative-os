"""Creative OS v2 — Prompt Compiler (M4).

Brief + brand config + ONE registry DNA entry -> generation prompt.
Encodes every production lesson as mandatory clauses:
  - hero FIRST, typography second (Sec 9b: reference = stage, topic = actor)
  - exact brand hexes with drift-reinforcement wording
  - reserve clauses WITHOUT pixel numbers (pixel numbers leak as canvas labels)
  - anti-artifact clauses (no guide lines / measurement labels / annotations)
  - no third-party logos/brand names on products
  - never hybridize: exactly one DNA entry per compile; tombstones hard-blocked.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOMBSTONES = {"DNA_16", "DNA_17", "DNA_19", "DNA_22", "DNA_25", "DNA_26"}


def load_registry():
    with open(os.path.join(ROOT, "registry", "dna.registry.json")) as f:
        return json.load(f)


def get_entry(registry, dna_id):
    if dna_id in TOMBSTONES:
        raise ValueError(f"{dna_id} is PURGED (user order 2026-10-15) — hard block, suggest nearest instead")
    for e in registry["entries"]:
        if e.get("id", e.get("registry_id")) == dna_id:
            if e.get("status") == "purged":
                raise ValueError(f"{dna_id} is purged")
            return e
    raise KeyError(dna_id)


def compile_prompt(brief, brand, entry, bg_variant="A", series_anchor=None, lock_mode="full"):
    """brief: {topic, hero_description, headline, support_lines[], platform, format}
    series_anchor: optional path to an APPROVED master reference for this
    slide's repeat family (Reference-Locked Generation Mode — DNA-gated,
    activated by orchestrator.set_series_anchor, never default).
    lock_mode: 'full'       — reproduce the whole design, swap only content
               'background' — reproduce background only, layout free per DNA
    Discipline: always the ORIGINAL approved master, never slide N-1 (drift
    compounds); always the raw pre-compositing image (composited chrome would
    be hallucinated back); full-resolution copy-read of all rendered text is
    mandatory on every clone (copy-leak lesson).
    Returns {prompt, reference_images, canvas, notes}. The caller (agent) passes
    reference_images to the image model per QA20b (image-linked DNA must be
    re-opened with vision before use — enforced upstream)."""
    colors = brand["colors"]
    bg_map = brand.get("background_system", {})
    bg = {"A": bg_map.get("A_primary"), "B": bg_map.get("B_contrast"), "C": bg_map.get("C_expressive")}[bg_variant]

    p = []
    # 1. Hero first (Sec 9a/9b)
    p.append(f"A single dominant hero graphic — {brief['hero_description']} — occupying roughly half the canvas, "
             f"composed exactly like this stage: {entry.get('composition_dna', entry.get('working_label', ''))}")
    # 2. Topic swap, never DNA swap
    p.append(f"Topic of the design: {brief['topic']}. Keep the reference composition; only the subject/metaphor changes.")
    # 3. Locked constraints from the DNA entry
    locked = entry.get("constraints", {}).get("locked", [])
    if locked:
        p.append("Non-negotiable composition traits: " + "; ".join(locked) + ".")
    # 3b. Anti-dilution clause (lesson: run-1792215268 — a bold infographic DNA
    # drifted into a minimalist editorial read; rhythm counts and
    # illustration-first scale weakened while every numeric check still passed)
    p.append("Match the reference's composition DENSITY, SCALE and RHYTHM faithfully: "
             "if the reference is illustration-first, artwork must dominate over text; "
             "if it uses a repeated card or numbered-step rhythm, reproduce that exact "
             "rhythm and count. Do not simplify, minimalize or editorialize the "
             "reference layout.")
    # 3c. Reference-Locked Generation (anti micro-drift; DNA-gated upstream)
    if series_anchor and lock_mode == "full":
        p.append("An approved master slide of this EXACT repeat family is attached as the "
                 "primary reference. Reproduce its design EXACTLY — background, texture, "
                 "palette, lighting, gradients, shapes, shadows, decorative elements, "
                 "illustration style, composition, grid, spacing, alignment, relative scale "
                 "and every micro-detail. Change ONLY the content layer: the headline, "
                 "supporting lines and hero subject specified below for THIS slide. Do NOT "
                 "copy any words, numbers or labels from the reference slide — the only text "
                 "on this slide must be the text specified below.")
    elif series_anchor and lock_mode == "background":
        p.append("An approved background reference is attached. Reproduce its BACKGROUND "
                 "exactly — color, texture, lighting, gradients and decorative background "
                 "elements. The layout and composition of THIS slide are free to follow the "
                 "stage composition described above — do NOT copy the reference's layout, "
                 "and do NOT copy any words, numbers or labels from it.")
    # 4. Typography
    p.append(f"Headline text: \"{brief['headline']}\" in clean {brand['typography']['primary_family']}-style "
             f"geometric sans, strong hierarchy, readable at thumbnail size.")
    for s in brief.get("support_lines", []):
        p.append(f"Supporting line: \"{s}\" — much smaller than the headline.")
    # 5. Palette with anti-drift reinforcement (lesson: tones drift)
    p.append(f"Background: {bg}. Exact hex colors ONLY: primary {colors['primary']}, background {colors['background']}, "
             f"text {colors['text']}. Backgrounds must be EXACTLY the stated hex — bright and clean, no off-tone patches, "
             f"no color drift.")
    # 6. Reserve zones WITHOUT pixel numbers (lesson: numbers render as labels)
    p.append("Keep the very top-right corner and the entire bottom edge of the canvas completely empty of text, "
             "objects and labels — clean background only in those areas.")
    # 7. Anti-artifact + anti-trademark clauses (lessons: guide-frame leak, Rolex crown)
    p.append("No guide lines, no measurement labels, no annotations, no watermarks, no frames around the canvas. "
             "No third-party logos, no brand names, no handles anywhere — all products and props clean and unbranded.")
    canvas = {"linkedin_carousel": (1080, 1350), "post": (1080, 1080), "feed_45": (1080, 1350),
              "story_916": (1080, 1920)}.get(brief.get("format", "feed_45"), (1080, 1350))
    refs = []
    if series_anchor:
        refs.append(series_anchor)  # PRIMARY reference: the approved sibling
    link = entry.get("linkage", {})
    if link.get("mode") == "image":
        refs.append(link["source_image"])
    elif link.get("mode", "").startswith("sheet_crop"):
        refs.append({"sheet": link["sheet"], "crop_box": link["crop_box"]})
    refs.append(brand["assets"]["font_specimen"])
    notes = "9:16 formats require an independent re-layout compile, never a stretch of this one."
    if series_anchor:
        notes += (f" REFERENCE LOCK ACTIVE (mode={lock_mode}): clone only from the ORIGINAL "
                  "approved master (never slide N-1); master must be a RAW pre-compositing "
                  "slide; full-resolution copy-read of all rendered text is mandatory after "
                  "generation (copy-leak check); verify against the master per QA30.")
        if lock_mode == "background":
            notes += (" Prefer reusing the original background ASSET directly with "
                      "programmatic content compositing when the change is content-only — "
                      "reference-prompting is the fallback, not the first choice (rule 9).")
    return {"prompt": " ".join(p), "reference_images": refs, "canvas": canvas, "notes": notes}
