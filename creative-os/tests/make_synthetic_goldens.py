"""Creative OS v2 — Synthetic golden fixture generator.

Builds known-good canvases from config/brand.config.example.json (the PUBLIC
brand config) so that every clone of this repo can run the full golden-test
shape — including the "known-good work must PASS" direction — without the
maintainer's private delivered artwork.

Fixtures are pure geometry (no text glyphs), so output is deterministic and
independent of font availability or freetype version. They are committed to
the repo; re-run this script only if the fixture spec changes, then re-commit.

Usage:  python3 tests/make_synthetic_goldens.py
Output: tests/fixtures/synthetic/good-post-01.png, good-post-02.png
        tests/fixtures/synthetic/seq/slide-01..04.png
"""
import json, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tests", "fixtures", "synthetic")

cfg = json.load(open(os.path.join(ROOT, "config", "brand.config.example.json")))
C = cfg["colors"]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PRIMARY, PAPER, INK = hexrgb(C["primary"]), hexrgb(C["background"]), hexrgb(C["text"])
W, H = 1080, 1350  # feed_45 canvas
M = 60             # content margin (outer 30px stays clean per the grid rule)

# Series contract — golden_tests.py asserts against these exact boxes:
# QA26 searches SYN_BOX (dark polarity) and must find the pill at PILL on
# every slide; QA27 measures light ink-height inside SYN_TEXT_BOX.
SYN_BOX = (900, 40, 1040, 104)       # search box for the repeating chip
PILL = (916, 52, 1024, 92)           # dark pill, identical on every slide
SYN_TEXT_BOX = (920, 56, 1020, 88)   # fully inside the pill


def base_canvas():
    img = Image.new("RGB", (W, H), PAPER)
    return img, ImageDraw.Draw(img)


def make_post(path, block_h, accent_w):
    """Known-good single post: flat brand bg (clean corners for QA03a),
    charcoal content block + primary accent bar, all inside margins."""
    img, d = base_canvas()
    d.rounded_rectangle([M, 220, W - M, 220 + block_h], radius=24, fill=INK)
    d.rectangle([M, 260 + block_h, M + accent_w, 300 + block_h], fill=PRIMARY)
    d.rounded_rectangle([M, 360 + block_h, W - M, H - 160], radius=24,
                        outline=INK, width=4)
    img.save(path)


def make_slide(path, idx, bar2_w):
    """Known-good series slide: pill shape locked at PILL on every slide
    (QA26); light 'numeral' bars inside share a constant 20px ink height
    (QA27) while bar widths vary per slide — content may change, scale and
    position may not."""
    img, d = base_canvas()
    # repeating counter chip (the locked element)
    d.rounded_rectangle(PILL, radius=18, fill=INK)
    d.rectangle([928, 62, 944, 82], fill=PAPER)             # fixed bar
    d.rectangle([952, 62, 952 + bar2_w, 82], fill=PAPER)    # varying-width bar
    # per-slide body content (legitimately different each slide)
    y = 300 + idx * 60
    d.rounded_rectangle([M, y, W - M, y + 420], radius=24, fill=INK)
    d.rectangle([M, y + 460, M + 300 + idx * 40, y + 500], fill=PRIMARY)
    img.save(path)


def main():
    os.makedirs(os.path.join(OUT, "seq"), exist_ok=True)
    make_post(os.path.join(OUT, "good-post-01.png"), block_h=340, accent_w=360)
    make_post(os.path.join(OUT, "good-post-02.png"), block_h=260, accent_w=520)
    for i, w in enumerate([28, 20, 24, 32], start=1):
        make_slide(os.path.join(OUT, "seq", f"slide-{i:02d}.png"), i, w)
    print("synthetic goldens written to", OUT)


if __name__ == "__main__":
    main()
