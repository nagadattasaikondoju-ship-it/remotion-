# Per-frame caption masks: thin bright strokes (top-hat) with low saturation inside the caption band, plus the drop shadow.
import os, sys, glob, numpy as np, cv2
W = sys.argv[1]
K = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r, r))
def text_mask(f, zone, title=False):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, cv2.getStructuringElement(cv2.MORPH_RECT, (41, 41)))
    white = (th > 35) & (hsv[..., 2] > 185) & (hsv[..., 1] < 75)
    m = white
    if title:   # copper "Oneloop": warm, mid-bright, also thin strokes vs the dark hair
        th2 = cv2.morphologyEx(hsv[..., 1], cv2.MORPH_TOPHAT, cv2.getStructuringElement(cv2.MORPH_RECT, (51, 51)))
        copper = (hsv[..., 0] >= 6) & (hsv[..., 0] <= 22) & (hsv[..., 1] > 80) & (hsv[..., 2] > 60) & (th2 > 25)
        m = m | copper
    m = (m & zone).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    # drop small specks: keep components that look like glyphs (enough pixels)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= 40 and st[i, cv2.CC_STAT_HEIGHT] <= 140: keep[lab == i] = 255
    return keep
for d in sorted(glob.glob(os.path.join(W, "*/"))):
    name = os.path.basename(d.rstrip("/")); frames = sorted(glob.glob(os.path.join(d, "frames", "*.png")))
    title = name.startswith("01")
    if name.startswith(("02", "03")):   # no captions in these shots
        for i, _ in enumerate(frames): cv2.imwrite(os.path.join(d, "masks", f"{i:05d}.png"), np.zeros((1920, 1080), np.uint8))
        print(name, "no caption"); continue
    zone = np.zeros((1920, 1080), bool)
    if title: zone[680:1210, 15:1065] = True
    else: zone[430:640, 0:1080] = True
    raw = [text_mask(cv2.imread(f), zone, title) for f in frames]
    # the line is one block: union with neighbours (captions drift a few px), add the down-right shadow, dilate generously
    out = []
    for i in range(len(raw)):
        u = np.max(raw[max(0, i - 3): i + 4], axis=0)
        sh = np.roll(np.roll(u, 9, 0), 9, 1)
        m = cv2.dilate(np.maximum(u, sh), K(21 if not title else 19))
        out.append(m)
    for i, m in enumerate(out): cv2.imwrite(os.path.join(d, "masks", f"{i:05d}.png"), m)
    for j, k in enumerate([0, len(frames) // 2, len(frames) - 1]):
        pv = cv2.imread(frames[k]); sel = out[k] > 0; pv[sel] = (0.45 * pv[sel] + [0, 0, 140]).astype(np.uint8)
        cv2.imwrite(os.path.join(W, f"mp_{name}_{j}.jpg"), cv2.resize(pv, (270, 480)))
    print(name, "mask px (mid):", int((out[len(out) // 2] > 0).sum()))
