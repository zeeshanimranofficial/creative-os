"""Creative OS v2 — Trend Research (M5).

Trend input ENRICHES the brief; it never redesigns. Hard boundary (user rule):
research may change the ACTOR (topic, metaphor, hero object, copy angle) —
it may NEVER change the STAGE (DNA composition), the palette, the components,
or platform policies.

The host agent does the actual web research; this module structures the
findings and strips anything that would violate the boundary.
"""
FORBIDDEN_KEYS = {"palette", "colors", "font", "typography", "layout", "composition",
                  "background_system", "components", "margins", "canvas"}

ALLOWED_KEYS = {"topic_angle", "hero_metaphor", "copy_hooks", "hashtags", "facts",
                "trending_formats_note", "sources"}


def sanitize(findings):
    """findings: dict from the agent's research. Returns (clean, rejected)."""
    clean, rejected = {}, {}
    for k, v in findings.items():
        if k in ALLOWED_KEYS:
            clean[k] = v
        else:
            rejected[k] = v  # logged, never applied
    return clean, rejected


def enrich_brief(brief, findings):
    """Apply sanitized findings to a brief. DNA-affecting fields untouched."""
    clean, rejected = sanitize(findings)
    out = dict(brief)
    if "topic_angle" in clean:
        out["topic"] = f"{brief['topic']} — angle: {clean['topic_angle']}"
    if "hero_metaphor" in clean and not brief.get("hero_description"):
        out["hero_description"] = clean["hero_metaphor"]
    if "copy_hooks" in clean and not brief.get("headline"):
        out["headline"] = clean["copy_hooks"][0]
    out.setdefault("research", {})["applied"] = clean
    if rejected:
        out["research"]["rejected_as_dna_override"] = list(rejected)
    return out


def research_prompt(topic, platform):
    """Instruction block for the host agent's web research step."""
    return (f"Research current angles for '{topic}' on {platform}: hooks, stats, metaphors in trending posts. "
            f"Collect ONLY: topic angles, hero metaphors, copy hooks, hashtags, verifiable facts + sources. "
            f"Do NOT collect or propose palettes, fonts, layouts or compositions — the DNA library governs those.")
