"""Leakage linter — keeps the instruction set general.

Principle enforced here:

    EVIDENCE may be concrete. INSTRUCTIONS must not be.

An "instruction" that names a colour, a product, a pixel value or a slide
number is instance data. It belongs in the campaign folder, not in the
playbook, because it teaches the next agent nothing transferable.

Usage:
    python lint_rules.py errors.json
    python lint_rules.py errors.json --lexicon lexicon.txt

Exit code 1 if any instruction contains instance leakage.
"""
import json
import re
import sys

# Anything a rule may legitimately cite as a value must arrive as a symbol.
SYMBOL = re.compile(r"\{\{[A-Z0-9_]+\}\}")

CHECKS = [
    ("hex-colour", re.compile(r"#[0-9A-Fa-f]{3,8}\b"),
     "colour literal — resolve from BRAND_PALETTE"),
    ("pixel-literal", re.compile(r"\b\d{2,5}\s?(?:px|pixels?)\b"),
     "pixel value — resolve from CHROME_BBOX / SAFE_MARGIN"),
    ("dimension-pair", re.compile(r"\b\d{2,5}\s?[x\u00d7]\s?\d{2,5}\b"),
     "canvas dimension — resolve from TARGET_SIZE"),
    ("slide-id", re.compile(r"\b(?:s0?\d|slide[-_ ]?\d{1,2}|v[1-9])\b", re.I),
     "slide/version reference — a rule must hold for every slide"),
    ("filename", re.compile(r"\b[\w-]+\.(?:png|jpe?g|webp|svg|psd)\b", re.I),
     "asset filename — resolve from CANONICAL_ENTITY(role)"),
    ("magic-number", re.compile(r"(?<![\w.])\d{2,3}(?:\.\d+)?%(?![\w])"),
     "bare percentage — declare it as a parameter with an authority"),
]


def load_lexicon(path):
    """Product/brand nouns for this campaign. Extend per campaign."""
    base = {
        "bottle", "bottles", "cap", "caps", "navy", "matte", "steel",
        "water", "splash", "pet", "plastic", "pedestal", "tote", "bench",
        "sleeve", "flask", "hydration", "insulated",
    }
    if path:
        with open(path) as f:
            base |= {w.strip().lower() for w in f if w.strip()}
    return base


def lint_text(text, lexicon):
    leaks = []
    for name, rx, hint in CHECKS:
        for m in rx.finditer(text):
            leaks.append((name, m.group(0), hint))
    for w in re.findall(r"[A-Za-z']+", text):
        if w.lower() in lexicon:
            leaks.append(("product-noun", w, "product adjective — belongs in ENTITY_MANIFEST, not the rule"))
    return leaks


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "errors.json"
    lexicon = load_lexicon(sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--lexicon" else None)
    doc = json.load(open(path))
    errors = doc["errors"] if isinstance(doc, dict) else doc

    total = 0
    clean = 0
    for e in errors:
        text = e.get("instruction_to_add", "")
        leaks = lint_text(text, lexicon)
        if not leaks:
            clean += 1
            continue
        total += len(leaks)
        print(f"\n{e['id']}  {e['title']}")
        for kind, value, hint in leaks:
            print(f"    ! {kind:15s} {value!r:24s} -> {hint}")

    print(f"\n{'-'*66}")
    print(f"{len(errors)} instructions · {clean} general · {len(errors)-clean} leaked {total} instance value(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
