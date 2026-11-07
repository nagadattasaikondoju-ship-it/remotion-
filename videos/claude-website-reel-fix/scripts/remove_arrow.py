import sys, subprocess, numpy as np, cv2, json
src, out = sys.argv[1], sys.argv[2]
W, H, FPS = 1080, 1920, 30
END_F = int(27.2 * FPS)
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "ffv1", "-level", "3", out], stdin=subprocess.PIPE)
X0, X1, Y0, Y1 = 780, 1070, 760, 1120  # search box on the wall right of the speaker
log = []
for f in range(END_F):
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
    roi = img[Y0:Y1, X0:X1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    yel = cv2.inRange(hsv, (15, 110, 150), (40, 255, 255))
    n = int(yel.sum() / 255)
    if f >= 712 and n > 30:
        # arrow body + its dark outline: grow the yellow core, keep the largest blob only
        k, lab, st, _ = cv2.connectedComponentsWithStats(yel, 8)
        big = 1 + int(np.argmax(st[1:, 4]))
        core = (lab == big).astype(np.uint8) * 255
        mask = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
        x, y, w, h = st[big, :4]
        if not (840 <= x + X0 <= 960 and w <= 100 and h <= 130): enc.stdin.write(img.tobytes()); continue
        roi[:] = cv2.inpaint(roi, mask, 7, cv2.INPAINT_TELEA)
        log.append([f, n, int(x + X0), int(y + Y0), int(w), int(h)])
    enc.stdin.write(img.tobytes())
enc.stdin.close(); enc.wait(); dec.kill()
json.dump(log, open("arrow_log.json", "w"))
print("frames with arrow:", len(log), "first", log[0][:1] if log else None, "last", log[-1][:1] if log else None, "max bbox", max((l[4] for l in log), default=0), max((l[5] for l in log), default=0))
