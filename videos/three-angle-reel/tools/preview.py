# Review sheet: base picture (tools/base.py's frame(t), downscaled) + overlay stills from render.mjs, side by side.
#   python3 tools/preview.py HOST SAMPLE out.jpg t1 t2 …     (run `node render.mjs stills t1 t2 …` first)
import sys, cv2, numpy as np
HOST, SAMPLE, DST, *TS = sys.argv[1:]
sys.argv = ["base.py", HOST, SAMPLE, "/dev/null"]
src = open("tools/base.py").read().split('if "--test" in sys.argv:')[0]
g = {"__name__": "base"}; exec(src, g)
tiles = []
for t in map(float, TS):
    b = cv2.resize(g["frame"](t), (540, 960), interpolation=cv2.INTER_AREA).astype(np.float32)
    o = cv2.imread(f"out/stills/o_{t:.2f}.png", cv2.IMREAD_UNCHANGED)
    if o is not None:
        o = cv2.resize(o, (540, 960), interpolation=cv2.INTER_AREA).astype(np.float32); a = o[..., 3:4] / 255
        b = b * (1 - a) + o[..., :3] * a
    b = b.astype(np.uint8); cv2.putText(b, f"{t:.2f}", (8, 30), 0, 0.9, (0, 255, 255), 2); tiles.append(b)
rows = [np.hstack(tiles[i:i + 6] + [np.zeros_like(tiles[0])] * (6 - len(tiles[i:i + 6]))) for i in range(0, len(tiles), 6)]
cv2.imwrite(DST, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
