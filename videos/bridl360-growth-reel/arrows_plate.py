"""Clean plate of the growth-arrows scene without the old brand's logo: img/plate_arrows.png + img/arrows_mask.png.
Frame 24.0 s of the base (BASE env); the logo (red mark + dark-grey letters in its box) is masked by colour, dilated, filled with
OpenCV's Telea inpaint for the shading, and the grid detail is copied from clean squares one or more grid steps away; arrows kept.
   BASE=out/base_smooth.mp4 python3 arrows_plate.py"""
import cv2, numpy as np, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "24.0", "-i", os.environ["BASE"], "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
im8 = np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3).copy(); im = im8.astype(np.float32)
b, g, r = [im8[..., i].astype(int) for i in range(3)]
x0, y0, x1, y1 = 120, 560, 680, 975
red = (r > 140) & (g < 130) & (b < 140) & (r - g > 60)
dark = (r < 170) & (g < 170) & (b < 170) & (abs(r - g) < 35) & (abs(g - b) < 35)
m = np.zeros(im8.shape[:2], np.uint8); m[y0:y1, x0:x1] = (red | dark)[y0:y1, x0:x1] * 255
n, lab, st, _ = cv2.connectedComponentsWithStats(m); keep = np.zeros_like(m)
for i in range(1, n):
    if st[i, 4] > 40: keep[lab == i] = 255
mk8 = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))); mk = mk8 > 0
tel = cv2.inpaint(im8, mk8, 7, cv2.INPAINT_TELEA).astype(np.float32)
green = (im[..., 1] - im[..., 2] > 25) & (im[..., 1] - im[..., 0] > 25)
bad = mk | cv2.dilate(green.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
px, py = 56, 56
src = im.copy(); ys, xs = np.nonzero(mk); filled = np.zeros(mk.shape, bool)
for dx, dy in [(0, -k * py) for k in range(1, 9)] + [(-k * px, 0) for k in range(1, 9)] + [(-k * px, -j * py) for k in range(1, 5) for j in range(1, 5)]:
    sel = ~filled[ys, xs]; yy = ys[sel] + dy; xx = xs[sel] + dx
    ok = (yy >= 0) & (xx >= 0); yy2 = np.clip(yy, 0, 1919); xx2 = np.clip(xx, 0, 1079); ok &= ~bad[yy2, xx2]
    src[ys[sel][ok], xs[sel][ok]] = im[yy2[ok], xx2[ok]]; filled[ys[sel][ok], xs[sel][ok]] = True
rec = np.clip(cv2.GaussianBlur(tel, (0, 0), 12) + src - cv2.GaussianBlur(src, (0, 0), 12), 0, 255)
a = cv2.GaussianBlur(mk.astype(np.float32), (0, 0), 4)[..., None]
out = im * (1 - a) + rec * a; out[green] = im[green]
cv2.imwrite("img/plate_arrows.png", out.astype(np.uint8))
am = cv2.GaussianBlur(mk8, (0, 0), 4); cv2.imwrite("img/arrows_mask.png", np.dstack([np.full_like(am, 255)] * 3 + [am]))
print("arrows plate: filled", round(float(filled[ys, xs].mean()), 3), "mask px", int(mk.sum()))
