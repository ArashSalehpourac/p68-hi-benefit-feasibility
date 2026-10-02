#!/usr/bin/env python3
"""
Gate-1 / P0 pilot: does encoded payload size depend on corruption type and severity?

For each source image: resize shorter side to 256, center-crop 224, apply each
ImageNet-C-style corruption at severities 1-5 (plus severity 0 = clean), and
encode ONCE (JPEG and WebP at fixed quality, no metadata). Records bytes.

IMPORTANT (corrected per v4 review round)
- Original ILSVRC validation images are ALREADY JPEG. The pipeline is:
  decode the original image -> corrupt -> encode once. Do NOT describe the
  input as "raw". Do NOT feed the released ImageNet-C files (already lightly
  JPEG-compressed).
- Uses the `imagecorruptions` pip package, a port of the ImageNet-C code.
  For the final paper, regenerate with the official code
  (github.com/hendrycks/robustness) and confirm sizes match; record the
  corruption-code commit, seeds and output hashes.
- Pick the class subset and image count yourself and report them.

Usage:
  pip install imagecorruptions pillow numpy scipy --break-system-packages
  python pilot_payload_vs_severity.py --img_dir /path/to/val_images --n 500 \
      --out payload.csv --skip glass_blur
"""
import argparse, csv, io, os, random, sys
import numpy as np
if not hasattr(np, "float_"):  # imagecorruptions (fog) still uses np.float_ under NumPy 2
    np.float_ = np.float64
from PIL import Image
from scipy.stats import spearmanr

try:
    from imagecorruptions import corrupt, get_corruption_names
except ImportError:
    sys.exit("pip install imagecorruptions")


def load_224(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    s = 256 / min(w, h)
    im = im.resize((max(256, round(w * s)), max(256, round(h * s))), Image.BILINEAR)
    w, h = im.size
    l, t = (w - 224) // 2, (h - 224) // 2
    return np.asarray(im.crop((l, t, l + 224, t + 224)), dtype=np.uint8)


def enc_bytes(arr, fmt, q):
    buf = io.BytesIO()
    im = Image.fromarray(arr)
    if fmt == "jpeg":
        im.save(buf, "JPEG", quality=q, optimize=False, progressive=False, subsampling="4:2:0")
    else:
        im.save(buf, "WEBP", quality=q, method=4)
    return buf.tell()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img_dir", required=True)
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--quality", type=int, default=75)
    ap.add_argument("--out", default="payload.csv")
    ap.add_argument("--skip", nargs="*", default=[])
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    exts = (".jpg", ".jpeg", ".png", ".JPEG")
    files = sorted(os.path.join(r, f) for r, _, fs in os.walk(a.img_dir) for f in fs if f.endswith(exts))
    if not files:
        sys.exit("no images found")
    random.Random(a.seed).shuffle(files)
    files = files[: a.n]
    names = [c for c in get_corruption_names() if c not in a.skip]
    print(f"{len(files)} images, {len(names)} corruptions: {names}")

    rows = []
    for i, p in enumerate(files):
        x = load_224(p)
        for fmt in ("jpeg", "webp"):
            rows.append([os.path.basename(p), "clean", 0, fmt, enc_bytes(x, fmt, a.quality)])
        for c in names:
            for s in range(1, 6):
                try:
                    y = np.uint8(corrupt(x, corruption_name=c, severity=s))
                except Exception as e:
                    print("skip", c, s, e)
                    continue
                for fmt in ("jpeg", "webp"):
                    rows.append([os.path.basename(p), c, s, fmt, enc_bytes(y, fmt, a.quality)])
        if (i + 1) % 25 == 0:
            print(f"  {i + 1}/{len(files)}")

    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["image", "corruption", "severity", "codec", "bytes"])
        w.writerows(rows)

    # summary: per codec x corruption
    import collections
    d = collections.defaultdict(list)
    for img, c, s, fmt, b in rows:
        d[(fmt, c, s)].append(b)
    print("\nSUMMARY (median bytes; ratio = sev5 / clean; Spearman of severity vs bytes over all samples)")
    print(f"{'codec':5} {'corruption':20} {'sev1/clean':>10} {'sev5/clean':>10} {'rho':>6}  monotone-medians")
    for fmt in ("jpeg", "webp"):
        clean = np.median(d[(fmt, "clean", 0)])
        for c in names:
            meds = [np.median(d[(fmt, c, s)]) for s in range(1, 6) if d.get((fmt, c, s))]
            if len(meds) < 5:
                continue
            sev, byt = [], []
            for s in range(1, 6):
                for b in d[(fmt, c, s)]:
                    sev.append(s); byt.append(b)
            rho = spearmanr(sev, byt).correlation
            mono_up = all(meds[k] <= meds[k + 1] for k in range(4))
            mono_dn = all(meds[k] >= meds[k + 1] for k in range(4))
            tag = "up" if mono_up else ("DOWN" if mono_dn else "non-monotone")
            print(f"{fmt:5} {c:20} {meds[0]/clean:10.2f} {meds[4]/clean:10.2f} {rho:6.2f}  {tag}")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
