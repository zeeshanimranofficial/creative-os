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


def compile_prompt(brief, brand, entry, bg_variant="A"):
    """brief: {topic, hero_description, headline, support_lines[], platform, format}
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
    link = entry.get("linkage", {})
    if link.get("mode") == "image":
        refs.append(link["source_image"])
    elif link.get("mode", "").startswith("sheet_crop"):
        refs.append({"sheet": link["sheet"], "crop_box": link["crop_box"]})
    refs.append(brand["assets"]["font_specimen"])
    return {"prompt": " ".join(p), "reference_images": refs, "canvas": canvas,
            "notes": "9:16 formats require an independent re-layout compile, never a stretch of this one."}
