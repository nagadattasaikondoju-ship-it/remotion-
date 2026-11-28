"""Real diamond sprites for the shapes reel, cut from Siyari's own product photos (face-up stones), masked to each cut's outline
so only the diamond remains (no prongs / halo / band). Output: img/stone_<cut>.png, 512x512 RGBA, long axis vertical."""
import cv2, numpy as np, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
D = "research/shapes/hi/"
# file, centre (fx, fy), half-size (fw, fh) as fractions of image width/height, shape
S = {"round": ("round_0", (.535, .664), (.066, .066), "round"), "oval": ("oval_0", (.19, .455), (.132, .196), "oval"),
     "marquise": ("marquise_0", (.5, .508), (.192, .335), "marquise"), "cushion": ("cushion_0", (.503, .588), (.104, .104), "cushion"),
     "emerald": ("emerald_0", (.502, .694), (.087, .153), "emerald"), "heart": ("heart_0", (.508, .665), (.118, .108), "heart")}
def outline(kind, n=360):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False); c, s = np.cos(t), np.sin(t)
    if kind in ("round", "oval"): return np.c_[c, s]
    if kind == "marquise": return np.c_[s * np.abs(s) ** .0 * .98 * (1 - 0) * np.sign(s) * np.abs(s) ** .35 * 0 + c * 0 + np.sin(t) * np.abs(np.sin(t)) ** 0 * 0 + (np.abs(c) ** .0) * 0 + c * np.abs(c) ** -1e-9 * 0 + c, s][:, ::-1] * [1, 1] if False else np.c_[np.sign(s) * np.abs(s) ** 1.0 * 0 + .98 * c * np.abs(c) ** 0, s]
    if kind == "cushion": return np.c_[np.sign(c) * np.abs(c) ** .55, np.sign(s) * np.abs(s) ** .55]
    if kind == "emerald": k = .22; return np.array([[1, -1 + k], [1, 1 - k], [1 - k, 1], [-1 + k, 1], [-1, 1 - k], [-1, -1 + k], [-1 + k, -1], [1 - k, -1]], float)
    if kind == "heart":
        x = 16 * np.sin(t) ** 3; y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)); y = y - (y.max() + y.min()) / 2
        return np.c_[x / 16.5, y / (y.max() * 1.02)]
def lens(n=360):                    # marquise: two circular arcs meeting in points top and bottom (long axis vertical)
    t = np.linspace(-1, 1, n // 2); x = (1 - t ** 2) ** 1.0; return np.r_[np.c_[x, t], np.c_[-x[::-1], t[::-1]]]
os.makedirs("img", exist_ok=True)
for cut, (fn, (fx, fy), (fw, fh), kind) in S.items():
    im = cv2.imread(D + fn + ".img"); h, w = im.shape[:2]
    cx, cy, rx, ry = fx * w, fy * h, fw * w, fh * h
    pts = lens() if kind == "marquise" else outline(kind)
    poly = np.c_[cx + pts[:, 0] * rx, cy + pts[:, 1] * ry].astype(np.int32)
    m = np.zeros((h, w), np.uint8); cv2.fillPoly(m, [poly], 255, cv2.LINE_AA); m = cv2.GaussianBlur(m, (5, 5), 0)
    x0, x1, y0, y1 = int(cx - rx * 1.08), int(cx + rx * 1.08), int(cy - ry * 1.08), int(cy + ry * 1.08)
    crop = im[max(0, y0):y1, max(0, x0):x1]; a = m[max(0, y0):y1, max(0, x0):x1]
    g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)[..., None].astype(np.float32); crop = np.clip(((crop * .3 + g * .7) - 128) * (1.18 if cut == 'round' else 1.06) + 132, 0, 255).astype(np.uint8)   # neutral white, a touch more contrast
    side = 512; hh, ww = crop.shape[:2]; sc = 470 / max(hh, ww)
    crop = cv2.resize(crop, (int(ww * sc), int(hh * sc)), interpolation=cv2.INTER_LANCZOS4); a = cv2.resize(a, (crop.shape[1], crop.shape[0]), interpolation=cv2.INTER_LINEAR)
    out = np.zeros((side, side, 4), np.uint8); oy, ox = (side - crop.shape[0]) // 2, (side - crop.shape[1]) // 2
    out[oy:oy + crop.shape[0], ox:ox + crop.shape[1], :3] = crop; out[oy:oy + crop.shape[0], ox:ox + crop.shape[1], 3] = a
    cv2.imwrite(f"img/stone_{cut}.png", out); print(cut, crop.shape[1], crop.shape[0])
