"""Creative OS v2 — QA Engine (M3).

Runs the numeric/config subset of qa.rules.json directly on pixels and
emits VISION TASKS (prepared crops + question) for vision-method rules —
the agent answers those by actually viewing the crops, per QA20b/QA14.

Result object per creative: {rule_id: {"status": pass|fail|vision_task,
"detail": ...}}. The retry controller consumes this.
"""
import json, os
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_rules():
    with open(os.path.join(ROOT, "config", "qa.rules.json")) as f:
        return json.load(f)


def _hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------- numeric checks ----------

def check_canvas(img, expected):
    ok = img.size == tuple(expected)
    return ok, f"{img.size} vs {tuple(expected)}"


def check_exact_hex(img, brand_hexes, zones=None, tol=14):
    """QA03a: sample corner zones; each must sit within tol of ONE brand hex.
    tol=14 covers approved paper-grain textures (calibrated on delivered Week-1
    finals); use tol<=6 only immediately after a brand-color snap pass on flat
    fills. Zones must be clean corners away from designed shapes."""
    w, h = img.size
    zones = zones or [(8, 8), (8, h - 9), (w - 9, h - 9), (w - 9, 8)]
    rgb = img.convert("RGB")
    bad = []
    targets = [_hexrgb(x) for x in brand_hexes]
    for (x, y) in zones:
        px = rgb.getpixel((x, y))
        if min(max(abs(a - b) for a, b in zip(px, t)) for t in targets) > tol:
            bad.append((x, y, px))
    return not bad, bad or "all zones on brand hex"


def check_reserved_zone_empty(img, box, bg_rgb, tol=18, max_frac=0.02):
    """QA17: zone must be bg-only BEFORE compositing."""
    crop = img.convert("RGB").crop(box)
    px = list(crop.getdata())
    off = sum(1 for p in px if max(abs(a - b) for a, b in zip(p, bg_rgb)) > tol)
    frac = off / len(px)
    return frac <= max_frac, f"{frac:.3%} non-bg pixels in {box}"


def check_strip_continuity(img, y_seam, x0=40, x1=None, band=24, max_delta=8):
    """QA25a: mean tone above vs below the strip seam (clean-corner sampling —
    callers must pass x-ranges away from designed shapes)."""
    x1 = x1 or img.size[0] - 40
    g = img.convert("L")
    top = g.crop((x0, y_seam - band, x1, y_seam)).resize((1, 1)).getpixel((0, 0))
    bot = g.crop((x0, y_seam, x1, y_seam + band)).resize((1, 1)).getpixel((0, 0))
    return abs(top - bot) <= max_delta, f"above {top} / below {bot}"


def _elem_bbox(img, box, polarity="dark", thresh=100):
    """Bounding box of the element SHAPE inside box (mask by polarity).
    polarity 'dark' = charcoal element on light bg; 'light' = cream on dark."""
    g = img.convert("L").crop(box)
    if polarity == "dark":
        mask = g.point(lambda p: 255 if p < thresh else 0)
    else:
        mask = g.point(lambda p: 255 if p > 255 - thresh else 0)
    return mask.getbbox()


def check_series_alignment(slides, box, max_shift=3, polarity="dark"):
    """QA26/QA19/QA07: the repeating element's SHAPE position/size must match
    across slides. Compares the element mask bbox (content such as 01/07 vs
    02/07 numerals legitimately changes — raw pixel diff is the wrong test)."""
    anchor = _elem_bbox(slides[0], box, polarity)
    if anchor is None:
        return False, "no element found in anchor slide"
    fails = []
    for i, s in enumerate(slides[1:], 1):
        bb = _elem_bbox(s, box, polarity)
        if bb is None:
            fails.append((i, "missing element"))
            continue
        drift = max(abs(a - b) for a, b in zip(anchor, bb))
        if drift > max_shift:
            fails.append((i, f"bbox {bb} vs anchor {anchor} drift {drift}px"))
    return not fails, fails or f"locked (anchor bbox {anchor})"


def check_scale_lock(slides, text_box, max_ratio_drift=0.05, polarity="dark"):
    """QA27: ink-height of the repeating text row must match across slides.
    polarity 'light' for cream text inside dark tabs/pills."""
    heights = []
    for s in slides:
        bb = _elem_bbox(s, text_box, polarity)
        heights.append((bb[3] - bb[1]) if bb else 0)
    if not heights or heights[0] == 0:
        return False, "no ink in anchor row"
    drift = max(abs(h - heights[0]) / heights[0] for h in heights)
    return drift <= max_ratio_drift, f"heights {heights} drift {drift:.1%}"


# ---------- vision task emission ----------

def vision_task(rule_id, question, crops):
    """crops: list of (image, box, out_path) — saved for the vision model to open."""
    paths = []
    for img, box, out in crops:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        (img.crop(box) if box else img).save(out)
        paths.append(out)
    return {"status": "vision_task", "rule": rule_id, "question": question, "crops": paths}


# ---------- runner ----------

def run_numeric_suite(img, ctx):
    """ctx: {expected_size, brand_hexes, reserved_zones:[(box,bg_rgb)], strip_seam_y or None}"""
    out = {}
    ok, d = check_canvas(img, ctx["expected_size"]); out["QA01"] = {"status": "pass" if ok else "fail", "detail": d}
    ok, d = check_exact_hex(img, ctx["brand_hexes"]); out["QA03a"] = {"status": "pass" if ok else "fail", "detail": str(d)}
    for i, (box, bg) in enumerate(ctx.get("reserved_zones", [])):
        ok, d = check_reserved_zone_empty(img, box, bg)
        out[f"QA17.{i}"] = {"status": "pass" if ok else "fail", "detail": d}
    if ctx.get("strip_seam_y"):
        ok, d = check_strip_continuity(img, ctx["strip_seam_y"])
        out["QA25a"] = {"status": "pass" if ok else "fail", "detail": d}
    return out
