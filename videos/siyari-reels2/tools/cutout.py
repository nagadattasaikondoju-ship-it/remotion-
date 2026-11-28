"""Cut Siyari product photos (jewellery on a plain light studio background) out to RGBA.
bg = big median blur of the photo; alpha from colour distance to that bg; small enclosed light areas (white diamond facets)
are filled back in, large enclosed ones (inside a hoop) stay clear. The soft contact shadow is kept as a faint shadow.
usage: python3 cutout.py in.jpg out.png"""
import cv2, numpy as np, sys
im = cv2.imread(sys.argv[1]); h, w = im.shape[:2]
f = im.astype(np.float32)
bg = cv2.medianBlur(im, 151 if min(h, w) > 300 else 51).astype(np.float32)
d = np.abs(f - bg).max(2)
sat = (f.max(2) - f.min(2)) - (bg.max(2) - bg.min(2))            # metal/colour stones are more saturated than the grey bg
a = np.clip((np.maximum(d, sat * 1.4) - 9) / 26, 0, 1)
core = (a > .5).astype(np.uint8)
core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
inv = (1 - core).astype(np.uint8); n, lab, st, _ = cv2.connectedComponentsWithStats(inv, connectivity=4)
for i in range(1, n):
    x, y, ww, hh, ar = st[i]
    touches = x == 0 or y == 0 or x + ww >= w or y + hh >= h
    if not touches and ar < h * w * .004: a[lab == i] = 1.0       # diamond facet holes
# shadows: soft, low-texture, slightly darker than the bg -> keep them as a real (dark) contact shadow
lum = f.mean(2); mu = cv2.blur(lum, (7, 7)); sd = np.sqrt(np.maximum(cv2.blur(lum * lum, (7, 7)) - mu * mu, 0))
dark = np.clip((bg.mean(2) - lum) / 40, 0, 1); shadow = (sd < 5) & (a < .9) & (dark > 0) & (sat < 12)
out = im.copy(); out[shadow] = 0; a = np.where(shadow, dark * .55, a)
a = np.where(sd > 9, np.maximum(a, np.clip((sd - 9) / 10, 0, 1)), a)      # textured = jewellery: fully opaque
im = out
a = cv2.GaussianBlur(a, (3, 3), 0)
ys, xs = np.where(a > .08); pad = 6
y0, y1, x0, x1 = max(0, ys.min() - pad), min(h, ys.max() + pad), max(0, xs.min() - pad), min(w, xs.max() + pad)
rgba = np.dstack([im, (a * 255).astype(np.uint8)])[y0:y1, x0:x1]
cv2.imwrite(sys.argv[2], rgba); print(sys.argv[2], rgba.shape[1], rgba.shape[0])
