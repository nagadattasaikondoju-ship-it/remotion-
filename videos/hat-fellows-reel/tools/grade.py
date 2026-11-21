# Talking-head pass (v2, after the user's notes): NO background blur and NO background dimming, the room stays as shot.
# What it does, whole frame alike:
#   punch-ins per clip (alternating, to hide the jump cuts; Lanczos so the zoomed hook stays sharp)
#   clarity grade read from the footage: the cream walls carry a faint green fluorescent cast → neutralised to a clean warm white;
#   highlights kept off the clip point (soft knee at 88 %), gentle S-curve for depth, +8 % saturation with skin left natural,
#   local contrast (CLAHE on luma, low strength) and a thresholded unsharp mask for an HD/crisp read; 8 % edge vignette.
#   python3 tools/grade.py out/base.mov out/graded.mov [--test t1,t2 out.jpg]
import sys, json, subprocess, cv2, numpy as np
SRC, DST = sys.argv[1], sys.argv[2]
W, H, FPS = 1080, 1920, 30
clips = json.load(open("edl.json"))["clips"]
bounds = np.cumsum([0] + [b - a for a, b, _ in clips])
ZOOM = [(1.42, 1.50), (1.00, 1.03), (1.13, 1.15), (1.00, 1.06), (1.13, 1.15), (1.00, 1.02), (1.14, 1.16), (1.00, 1.03),
        (1.12, 1.15), (1.00, 1.03), (1.13, 1.15), (1.00, 1.04), (1.13, 1.15), (1.00, 1.03), (1.20, 1.22), (1.00, 1.02)]
ANCHOR = [(540, 770)] + [(540, 790)] * (len(clips) - 1)
def tone_lut():
    x = np.arange(256) / 255.0
    y = np.where(x > 0.88, 0.88 + (x - 0.88) * 0.55, x)              # soft knee: walls keep texture instead of clipping
    y = y + 0.055 * np.sin(np.pi * np.clip(y - 0.04, 0, 0.92) / 0.92)  # S-curve: denser mids, cleaner separation
    y = np.clip((y - 0.018) / (1 - 0.018), 0, 1)                        # set a true black point
    return (y * 255).clip(0, 255).astype(np.uint8)
LUT = tone_lut()
WB = np.array([1.0, 0.982, 1.012], np.float32)                         # BGR: pull the green cast, tiny warm lift
yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.08 * np.clip(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H * 0.45) / (H * 0.7)) ** 2, 0, 1) ** 1.5)[..., None].astype(np.float32)
CLAHE = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(6, 10))
def process(f, t):
    k = min(int(np.searchsorted(bounds, t, side="right") - 1), len(clips) - 1)
    u = (t - bounds[k]) / max(1e-6, bounds[k + 1] - bounds[k]); z0, z1 = ZOOM[k]; z = z0 + (z1 - z0) * (u * u * (3 - 2 * u))
    ax, ay = ANCHOR[k]
    M = np.float32([[z, 0, ax - ax * z], [0, z, ay - ay * z]])
    f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    g = f.astype(np.float32) * WB
    g = cv2.LUT(np.clip(g, 0, 255).astype(np.uint8), LUT)
    lab = cv2.cvtColor(g, cv2.COLOR_BGR2LAB); L = lab[..., 0]
    Lc = CLAHE.apply(L); lab[..., 0] = cv2.addWeighted(L, 0.6, Lc, 0.4, 0)                      # 40 % local contrast
    lab[..., 1:] = np.clip((lab[..., 1:].astype(np.float32) - 128) * 1.08 + 128, 0, 255).astype(np.uint8)   # +8 % chroma
    g = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR).astype(np.float32)
    blur = cv2.GaussianBlur(g, (0, 0), 1.1); d = g - blur
    g = g + 0.75 * d * (np.abs(d) > 1.5)                                                      # unsharp, skips flat noise
    return np.clip(g * VIG, 0, 255).astype(np.uint8)
if "--test" in sys.argv:
    ts = [float(v) for v in sys.argv[sys.argv.index("--test") + 1].split(",")]; cap = cv2.VideoCapture(SRC); rows = []
    for t in ts:
        cap.set(cv2.CAP_PROP_POS_FRAMES, round(t * FPS)); ok, f = cap.read(); o = process(f, t)
        k = min(int(np.searchsorted(bounds, t, side="right") - 1), len(clips) - 1); z = ZOOM[k][0]; ax, ay = ANCHOR[k]
        raw = cv2.warpAffine(f, np.float32([[z, 0, ax - ax * z], [0, z, ay - ay * z]]), (W, H), flags=cv2.INTER_LANCZOS4)
        rows.append(np.hstack([raw[600:1400, 140:940], o[600:1400, 140:940]]))
    cv2.imwrite(sys.argv[-1], np.vstack(rows)); sys.exit()
cap = cv2.VideoCapture(SRC)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "8", "-pix_fmt", "yuv420p", DST], stdin=subprocess.PIPE)
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    ff.stdin.write(process(f, i / FPS).tobytes()); i += 1
    if i % 300 == 0: print(i, flush=True)
ff.stdin.close(); ff.wait(); print("frames", i)
