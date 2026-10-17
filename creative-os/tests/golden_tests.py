"""Creative OS v2 — Golden Tests (M4).

Regression guard: the QA engine must keep PASSING known-good delivered work
and keep FAILING known-bad synthetic cases. Run after any engine/config change.
"""
import os, sys, glob, json
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WS = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import qa_engine as Q
import prompt_compiler as PC

BRAND_HEXES = ["#FF5A00", "#F5EFE6", "#1A1A1A"]
results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + ("  " + str(detail) if detail and not ok else ""))


# 1. Known-good finals must pass numeric suite
for p in sorted(glob.glob(os.path.join(WS, "facebook/week1/f*-post.png"))):
    img = Image.open(p)
    r = Q.run_numeric_suite(img, {"expected_size": (1080, 1350), "brand_hexes": BRAND_HEXES})
    check("golden-good " + os.path.basename(p), all(v["status"] == "pass" for v in r.values()), r)

# 2. Known-good series must hold QA26/27 (exclude _overview, exclude final slide)
seq = sorted(glob.glob(os.path.join(WS, "facebook/week1/seq-f2/f2-slide-*.png")))[:-1]
slides = [Image.open(p) for p in seq]
ok, d = Q.check_series_alignment(slides, (900, 30, 1050, 98), polarity="dark")
check("golden-good seq-f2 QA26", ok, d)
ok, d = Q.check_scale_lock(slides, (905, 40, 1045, 90), polarity="light")
check("golden-good seq-f2 QA27", ok, d)

# 3. Synthetic BAD cases must FAIL
bad = Image.new("RGB", (1080, 1350), (196, 196, 196))  # off-brand grey (t8 v1 drift lesson)
r = Q.run_numeric_suite(bad, {"expected_size": (1080, 1350), "brand_hexes": BRAND_HEXES})
check("golden-bad off-brand bg detected", r["QA03a"]["status"] == "fail", r["QA03a"])

wrong = Image.new("RGB", (1080, 1080), (245, 239, 230))
r = Q.run_numeric_suite(wrong, {"expected_size": (1080, 1350), "brand_hexes": BRAND_HEXES})
check("golden-bad wrong canvas detected", r["QA01"]["status"] == "fail")

drift = [Image.new("RGB", (400, 200), (245, 239, 230)) for _ in range(3)]
for i, s in enumerate(drift):
    ImageDraw.Draw(s).rectangle([50 + i * 6, 50, 150 + i * 6, 120], fill=(26, 26, 26))  # 6px/slide drift
ok, _ = Q.check_series_alignment(drift, (0, 0, 400, 200), polarity="dark")
check("golden-bad series drift detected", not ok)

# 4. Prompt compiler contracts
reg = PC.load_registry()
try:
    PC.get_entry(reg, "DNA_16")
    check("tombstone hard-block", False)
except ValueError:
    check("tombstone hard-block", True)

entry = PC.get_entry(reg, "HOB_01")
brand = json.load(open(os.path.join(ROOT, "config", "brand.config.sample.json")))
c = PC.compile_prompt({"topic": "cold email deliverability", "hero_description": "three hanging envelopes, one glowing orange",
                       "headline": "ONE EMAIL LANDS.", "format": "feed_45"}, brand, entry)
check("compiler: no pixel numbers leak", "px" not in c["prompt"] and "140" not in c["prompt"])
check("compiler: anti-artifact clause", "No guide lines" in c["prompt"])
check("compiler: exact hexes present", "#FF5A00" in c["prompt"] and "#F5EFE6" in c["prompt"])
check("compiler: reference attached", len(c["reference_images"]) >= 2)

fails = [n for n, ok, _ in results if not ok]
print(f"\n{len(results) - len(fails)}/{len(results)} golden tests passed" + (f" — FAILURES: {fails}" if fails else ""))
sys.exit(1 if fails else 0)
