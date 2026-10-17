"""Creative OS v2 — Component Library (M2).

Programmatic brand-critical elements composited OVER generated artwork.
Rule: Python renders ONLY these components; it never rebuilds artwork
(user hard rule: DNA-mismatched generations are regenerated, not patched).

All renderers take (canvas: PIL.Image RGBA-safe, brand: dict loaded from
brand.config json) and draw in place. Coordinates follow the proven specs
recorded in brand/BRAND_SYSTEM.md.
"""
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WS = os.path.dirname(ROOT)  # /home/user


def load_brand(path=None):
    """Load the brand config. Default resolution falls back
    brand.config.sample.json (maintainer's private config, not tracked in the
    public repo) -> brand.config.example.json (public), same as the
    orchestrator — a fresh clone must never crash on the default path (E1/FC-13)."""
    if path is None:
        for cand in ("brand.config.sample.json", "brand.config.example.json"):
            p = os.path.join(ROOT, "config", cand)
            if os.path.exists(p):
                path = p
                break
        else:
            raise FileNotFoundError("no brand config found in config/ — run onboarding or add brand.config.example.json")
    with open(path) as f:
        return json.load(f)


def _font(brand, role, size):
    fp = os.path.join(WS, brand["typography"]["font_dir"], brand["typography"]["roles"][role])
    return ImageFont.truetype(fp, size)


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def dp_circle(brand, size):
    """Real DP image, circle-masked. Never initials (hard rule)."""
    dp = Image.open(os.path.join(WS, brand["assets"]["dp_circle"])).convert("RGBA")
    dp = ImageOps.fit(dp, (size, size), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size * 4 - 1, size * 4 - 1], fill=255)
    dp.putalpha(mask.resize((size, size), Image.LANCZOS))
    return dp


def profile_strip(canvas, brand, y=1197, dp_x=190, dp_size=96, text_x=314):
    """Name + role strip (proven 1080x1350 FB/LI spec). Last-slide/minimal-post only."""
    d = ImageDraw.Draw(canvas)
    canvas.paste(dp_circle(brand, dp_size), (dp_x, y), dp_circle(brand, dp_size))
    d.text((text_x, y + 15), brand["brand"]["name"], font=_font(brand, "headline", 38),
           fill=_hex(brand["colors"]["text"]))
    d.text((text_x, y + 67), brand["brand"]["role_line"], font=_font(brand, "body", 24),
           fill=_hex(brand["colors"]["primary"]))


def engagement_row(canvas, brand, y=1225, xs=(718, 784, 850), size=40,
                   trio=("save", "repost", "like"), color=None):
    """Save/Repost/Like brand icons — all equal size (hard rule). Platform policy decides IF.

    color: 'charcoal'|'cream'|'orange'; if None, picked for contrast against the
    pixel under the first icon (hard rule: widgets must contrast their background).
    Pass trio=('fb-like','fb-comment','fb-share') for the FB set where a design needs it.
    """
    icons_dir = os.path.join(WS, brand["assets"]["icons_dir"])
    if color is None:
        r, g, bl = canvas.convert("RGB").getpixel((xs[0] + size // 2, y + size // 2))
        color = "charcoal" if (r + g + bl) / 3 > 140 else "cream"
    for x, name in zip(xs, trio):
        # prefer exact-size asset, else largest available, scaled down
        cands = sorted(f for f in os.listdir(icons_dir)
                       if f.startswith(f"{name}-{color}-") and f.endswith(".png"))
        exact = [f for f in cands if f"-{size}." in f]
        pick = exact[0] if exact else cands[-1]
        ic = Image.open(os.path.join(icons_dir, pick)).convert("RGBA")
        ic = ImageOps.contain(ic, (size, size))
        canvas.paste(ic, (x, y), ic)


def counter_tab(canvas, brand, cur, total, box=(900, 30, 1050, 98), radius=14):
    """'NN/NN' carousel tab (proven 9:16 spec). Consistent box across a series (QA 26)."""
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box, radius=radius, fill=_hex(brand["colors"]["text"]))
    t = f"{cur:02d}/{total:02d}"
    f = _font(brand, "headline", 30)
    w = d.textlength(t, font=f)
    cx = (box[0] + box[2]) / 2
    d.text((cx - w / 2, (box[1] + box[3]) / 2 - 19), t, font=f, fill=_hex(brand["colors"]["background"]))


def swipe_arrow(canvas, brand, y=1848, x0=460, x1=614, width=6):
    """Horizontal swipe marker; omitted on last slide."""
    d = ImageDraw.Draw(canvas)
    p = _hex(brand["colors"]["primary"])
    d.line([x0, y, x1, y], fill=p, width=width)
    d.line([x1 - 26, y - 20, x1, y], fill=p, width=width)
    d.line([x1 - 26, y + 20, x1, y], fill=p, width=width)


def handle_chip(canvas, brand, xy=(40, 1294), size=26):
    d = ImageDraw.Draw(canvas)
    d.text(xy, brand["brand"]["handle"], font=_font(brand, "label", size),
           fill=_hex(brand["colors"]["text"]))
