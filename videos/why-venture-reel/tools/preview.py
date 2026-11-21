# preview: graded+zoomed frames at given times with the overlay stills composited → one contact strip
import sys, cv2, numpy as np, importlib.util, os
sys.argv = [sys.argv[0], "out/base.mov", "x"] + sys.argv[1:]
spec = importlib.util.spec_from_file_location("g", "tools/grade.py"); g = importlib.util.module_from_spec(spec)
src = open("tools/grade.py").read().split("if \"--test\" in sys.argv:")[0]; exec(compile(src, "grade", "exec"), g.__dict__)
cap = cv2.VideoCapture("out/base.mov"); tiles = []
for ts in sys.argv[3:]:
    t = float(ts); cap.set(cv2.CAP_PROP_POS_FRAMES, min(round(t * 30), 1174)); ok, f = cap.read(); o = g.process(f, min(t, 39.1))
    ov = cv2.imread(f"out/stills/{t:.2f}.png", cv2.IMREAD_UNCHANGED)
    if ov is not None and ov.shape[2] == 3: o = ov
    elif ov is not None:
        a = ov[..., 3:4] / 255.0; o = (ov[..., :3] * a + o * (1 - a)).astype(np.uint8)
    tiles.append(cv2.resize(o, (300, 533)))
cv2.imwrite("out/preview.jpg", np.hstack(tiles))
