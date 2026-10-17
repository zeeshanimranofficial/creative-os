"""Creative OS v2 — Exporter (M2).

Final-mile module: crop (never stretch) -> resize -> margin/dimension
validation -> PNG post / PDF carousel / PNG sequence. Validation failures
raise; the retry-controller (M3) decides regenerate-vs-abort. img2pdf is
installed on demand (sandbox resets pip between sessions).
"""
import os, subprocess, sys
from PIL import Image

MARGIN = 30  # locked 30px grid


def _img2pdf():
    try:
        import img2pdf
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "img2pdf"], check=True)
        import img2pdf
    return img2pdf


def fit_to_canvas(img, w, h):
    """Center-crop to the target ratio then Lanczos resize. Stretching prohibited."""
    img = img.convert("RGB")
    sw, sh = img.size
    tr = w / h
    if sw / sh > tr:
        nw = int(sh * tr)
        img = img.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh))
    else:
        nh = int(sw / tr)
        img = img.crop((0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh))
    return img.resize((w, h), Image.LANCZOS)


def validate(img, w, h):
    """Hard checks before release: exact dimensions, RGB mode."""
    errs = []
    if img.size != (w, h):
        errs.append(f"size {img.size} != {(w, h)}")
    if img.mode not in ("RGB", "RGBA"):
        errs.append(f"mode {img.mode}")
    if errs:
        raise ValueError("export validation failed: " + "; ".join(errs))


def export_post(img, path, w=1080, h=1350):
    img = fit_to_canvas(img, w, h) if img.size != (w, h) else img.convert("RGB")
    validate(img, w, h)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    img.save(path)
    return path


def export_carousel_pdf(slide_paths, pdf_path, w=1080, h=1350):
    """Validated slides -> single PDF (user rule: carousel deliverables are PDFs)."""
    img2pdf = _img2pdf()
    for p in slide_paths:
        validate(Image.open(p), w, h)
    os.makedirs(os.path.dirname(pdf_path) or ".", exist_ok=True)
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(slide_paths))
    return pdf_path


def export_sequence(slide_paths, out_dir, w=1080, h=1920):
    """9:16 sequence export (independent re-layout upstream — never a 4:5 stretch)."""
    os.makedirs(out_dir, exist_ok=True)
    out = []
    for i, p in enumerate(slide_paths, 1):
        img = Image.open(p)
        validate(img, w, h)
        q = os.path.join(out_dir, f"{i:02d}.png")
        img.convert("RGB").save(q)
        out.append(q)
    return out
