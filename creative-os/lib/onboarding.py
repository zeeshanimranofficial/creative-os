"""Creative OS v2 — Brand Onboarding (M5).

First run with a new brand: the host agent asks the questions below, builds
the config, VALIDATES it against hard OS rules, and only then activates it.
Missing answers fall back to OS defaults. A brand config can never override
hard OS rules — conflicts become human-approval items, not silent overrides.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUESTIONS = [
    ("brand.name", "Brand / person name?", None),
    ("brand.role_line", "Role line / tagline under the name?", ""),
    ("brand.handle", "Social handle?", ""),
    ("colors.primary", "Primary accent color (hex)?", "#FF5A00"),
    ("colors.background", "Background/base color (hex)?", "#F5EFE6"),
    ("colors.text", "Text color (hex)?", "#1A1A1A"),
    ("typography.primary_family", "One primary font family?", "Poppins"),
    ("assets.dp_circle", "Path to real profile photo (REQUIRED for profile blocks)?", None),
    ("background_system.A_primary", "Variant A — primary background?", "brand background color, flat/subtle texture"),
    ("background_system.B_contrast", "Variant B — contrast background (DNA-permitted)?", "charcoal or light inverse"),
    ("background_system.C_expressive", "Variant C — expressive background (DNA-gated)?", "texture/collage/photo per DNA"),
    ("brand.company_branding_allowed", "Company name/logo allowed on creatives? (false for personal brands)", False),
]

HARD_RULES = [
    "30px margin lock", "profile circle uses a REAL photo (no initials)",
    "one primary font family", "engagement trio equal-size",
    "no third-party brand references", "DNA tombstones blocked",
    "one DNA per creative / no hybrids", "carousel = one BG variant family",
]


def _hex_ok(v):
    return bool(re.fullmatch(r"#[0-9A-Fa-f]{6}", v or ""))


def build_config(answers):
    """answers: flat dict keyed like 'colors.primary'. Returns (config, issues).
    issues = things a human must resolve; config inactive until issues empty."""
    base = json.load(open(os.path.join(ROOT, "config", "brand.config.sample.json")))
    issues = []
    for key, _q, default in QUESTIONS:
        val = answers.get(key, default)
        if val is None and default is None:
            issues.append(f"missing required answer: {key}")
            continue
        node = base
        parts = key.split(".")
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = val if val is not None else default
    for ck in ("primary", "background", "text"):
        if not _hex_ok(base["colors"].get(ck)):
            issues.append(f"colors.{ck} is not a valid hex")
    dp = answers.get("assets.dp_circle")
    if dp and not os.path.exists(os.path.join(os.path.dirname(ROOT), dp)):
        issues.append(f"dp image not found at {dp}")
    # hard-rule conflict scan: onboarding may not relax hard rules
    for k in answers:
        if k.startswith("layout_hard_rules") or k.startswith("restrictions"):
            issues.append(f"attempt to modify hard rule via onboarding: {k} — requires explicit human approval")
    base["_onboarding"] = {"status": "active" if not issues else "blocked", "issues": issues,
                           "hard_rules_in_force": HARD_RULES}
    return base, issues


def save_config(config, name):
    path = os.path.join(ROOT, "config", f"brand.{name}.json")
    with open(path, "w") as f:
        json.dump(config, f, indent=1)
    return path
