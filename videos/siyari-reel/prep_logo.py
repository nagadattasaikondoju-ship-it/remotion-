"""Cut Siyari's own logo artwork into clean white-on-alpha layers (no redrawing):
   img/swan.png       swan body from ref/logo_mark.png (1080 px original), crown diamond removed
   img/crown.png      the small diamond above the head (separate so it can be animated), same canvas as swan.png
   img/wordmark.png   SIYARI(R) from the website header file (623 px)
   img/lockup.json    where each piece sits in the user's full logo (ref/logo_full.png), in that file's pixels"""
import cv2, numpy as np, json, os
os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs("img", exist_ok=True)
m = cv2.imread("ref/logo_mark.png").astype(np.float32)               # BGR
green = np.array([0x20, 0x30, 0x24], np.float32); cream = np.array([0xC0, 0xD8, 0xEC], np.float32)
a = np.clip(((m - green) @ (cream - green)) / ((cream - green) @ (cream - green)), 0, 1)   # project onto green->cream
a = (a * 255).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats((a > 128).astype(np.uint8))
comps = sorted([(st[i, cv2.CC_STAT_AREA], i) for i in range(1, n)], reverse=True)
print("components (area, top, height):", [(s, st[i, 1], st[i, 3]) for s, i in comps[:6]])
crown_i = [i for s, i in comps if st[i, 1] < 230 and st[i, 3] < 60][0]   # small piece at the very top
cm = cv2.dilate((lab == crown_i).astype(np.uint8), np.ones((7, 7), np.uint8))
x0, y0, x1, y1 = 224, 165, 844, 947                                    # bbox 244..823 x 185..927 + 20 px pad
def save(alpha, name):
    rgba = np.dstack([np.full_like(alpha, 255)] * 3 + [alpha])[y0:y1, x0:x1]
    cv2.imwrite(f"img/{name}.png", rgba)
save(np.where(cm > 0, 0, a).astype(np.uint8), "swan"); save(np.where(cm > 0, a, 0).astype(np.uint8), "crown")
cx, cy = st[crown_i, 0] + st[crown_i, 2] / 2 - x0, st[crown_i, 1] + st[crown_i, 3] / 2 - y0
w = cv2.imread("research/AD_DESIGNS_UNIQUE_CREATIVE_280_x_80_px_623_x_189_px.png", cv2.IMREAD_UNCHANGED)
al = w[:, :, 3]; ys, xs = np.where(al > 8); wy0, wy1, wx0, wx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
wm = np.dstack([np.full_like(al, 255)] * 3 + [al])[wy0:wy1, wx0:wx1]; cv2.imwrite("img/wordmark.png", wm)
# letter columns of the wordmark (gaps in alpha) so letters can be revealed one by one
col = (al[wy0:wy1, wx0:wx1] > 30).any(0); runs = []; on = False
for x, c in enumerate(list(col) + [False]):
    if c and not on: s = x
    if on and not c: runs.append([int(s), int(x)])
    on = c
json.dump({"swan_canvas": [x1 - x0, y1 - y0], "swan_bbox_in_canvas": [20, 20, 600, 763], "crown_center": [round(cx, 1), round(cy, 1)],
           "wordmark_size": [int(wx1 - wx0), int(wy1 - wy0)], "wordmark_letters": runs,
           "lockup_ref_px": {"file": [185, 173], "swan": [71, 29, 126, 99], "wordmark": [34, 108, 162, 132], "tagline": [34, 139, 155, 145]},
           "colors": {"mark_green": "#263222", "mark_cream": "#EDDAC2"}}, open("img/lockup.json", "w"), indent=1)
print(open("img/lockup.json").read())
# separate layers for the swan's three solid parts (neck+body, upper wing, lower wing), same canvas
parts = [i for s, i in comps if i != crown_i][:3]
for k, (nm, i) in enumerate(zip(["body", "wing_upper", "wing_lower"], sorted(parts, key=lambda i: -st[i, cv2.CC_STAT_AREA])[:1] + sorted(sorted(parts, key=lambda i: -st[i, cv2.CC_STAT_AREA])[1:], key=lambda i: st[i, 1]))):
    mk = cv2.dilate((lab == i).astype(np.uint8), np.ones((5, 5), np.uint8))
    save(np.where((mk > 0) & (cm == 0), a, 0).astype(np.uint8), "swan_" + nm)
# geodesic "draw-on" maps: for each swan part, distance (inside the part) from a seed point, normalised 0..1.
# The page reveals a part where map < progress, so the swan paints itself along its own S curve. Packed R/G/B -> img/reveal_map.png
import heapq
def geodesic(mask, seed):
    h, w = mask.shape; INF = 1e9; d = np.full((h, w), INF, np.float32)
    ys, xs = np.where(mask); i = np.argmin((xs - seed[0]) ** 2 + (ys - seed[1]) ** 2); sy, sx = ys[i], xs[i]
    d[sy, sx] = 0; pq = [(0.0, sy, sx)]; steps = [(-1,0,1),(1,0,1),(0,-1,1),(0,1,1),(-1,-1,1.414),(-1,1,1.414),(1,-1,1.414),(1,1,1.414)]
    while pq:
        dd, y, x = heapq.heappop(pq)
        if dd > d[y, x]: continue
        for dy, dx, c in steps:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and dd + c < d[ny, nx]:
                d[ny, nx] = dd + c; heapq.heappush(pq, (dd + c, ny, nx))
    d[d >= INF] = d[d < INF].max(); return d / d.max()
maps = []
for nm, seed in [("body", "top"), ("wing_upper", "top"), ("wing_lower", "right")]:
    al = cv2.imread(f"img/swan_{nm}.png", cv2.IMREAD_UNCHANGED)[:, :, 3]; mk = cv2.dilate((al > 10).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    ys, xs = np.where(al > 128)
    s = (xs[np.argmin(ys)], ys.min()) if seed == "top" else (xs.max(), ys[np.argmax(xs)])
    g = geodesic(mk, s); g[~mk] = 1; maps.append((g * 255).astype(np.uint8)); print(nm, "seed", s)
cv2.imwrite("img/reveal_map.png", np.dstack([maps[2], maps[1], maps[0]]))   # BGR -> R=body, G=wing_upper, B=wing_lower
