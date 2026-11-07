# Picture pass for the Three Angle reel, written straight to 2160×3840 (4K vertical), 30 fps.
#   intro  host full screen ("Guys, watch this first.")
#   split  sample clip (top half, its square picture with the burned-in text cropped off) + host listening below,
#          live and silent (his own silent tail, ping-ponged); both panels slide in and out on an expo ease
#   main   host full screen, pauses cut, alternating punch-ins to hide the jump cuts, slow push inside each clip
#   plate  for the two full-screen graphics moments the host frame shrinks into a rounded, tilted card on near-black,
#          so the graphics are built around him (the reference's "frame becomes a card" move)
# Grade (no blur, no dimming of the room): warm-neutral white balance (the lilac wall pulled toward warm grey), soft
# highlight knee, gentle S-curve, light local contrast, +6 % chroma, thresholded unsharp at 4K, 9 % vignette.
# Every frame is graded at native 1080 and resampled ONCE (Lanczos) into 4K, so zooms and the upscale cost one resample.
#   python3 tools/base.py HOST.mp4 SAMPLE.mp4 out/base4k.mp4            full render
#   python3 tools/base.py HOST.mp4 SAMPLE.mp4 out.jpg --test 1,3,13,20.5  half-size preview sheet
import sys, json, math, subprocess, cv2, numpy as np
HOST, SAMPLE, DST = sys.argv[1:4]
FPS, W, H, K = 30, 2160, 3840, 2.0                    # K: 1080-space → 4K
HFPS = 30.01                                          # the phone file's real rate
TL = json.load(open("timeline.json")); E = json.load(open("edl.json"))
END, T_SPLIT, T_MAIN = TL["END"], TL["T_SPLIT"], TL["T_MAIN"]
MAIN = [s for s in TL["segs"] if s["kind"] == "main"]
PLATES = json.load(open("plate.json"))
L0, L1 = E["listen"]

def eout(x): return 1 - math.pow(2, -10 * min(max(x, 0), 1)) if x < 1 else 1.0
def einout(x):
    x = min(max(x, 0), 1); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2
def smooth(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)

# ---------- grade ----------
def tone_lut():
    x = np.arange(256) / 255.0
    y = np.where(x > 0.86, 0.86 + (x - 0.86) * 0.5, x)                # soft knee: the bright wall keeps texture
    y = y + 0.05 * np.sin(np.pi * np.clip(y - 0.04, 0, 0.92) / 0.92)   # S-curve
    y = np.clip((y - 0.02) / (1 - 0.02), 0, 1)                          # true black point
    return (y * 255).clip(0, 255).astype(np.uint8)
LUT = tone_lut()
WB = np.array([0.965, 1.0, 1.035], np.float32)                         # BGR: less blue/magenta, a touch warmer
CLAHE = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(6, 10))
def grade(f, wb=WB, chroma=1.06, local=0.35):
    g = cv2.LUT(np.clip(f.astype(np.float32) * wb, 0, 255).astype(np.uint8), LUT)
    lab = cv2.cvtColor(g, cv2.COLOR_BGR2LAB); L = lab[..., 0]
    lab[..., 0] = cv2.addWeighted(L, 1 - local, CLAHE.apply(L), local, 0)
    ab = lab[..., 1:].astype(np.float32) - 128
    ab[..., 0] -= 1.5                                                   # a*: pull the wall's magenta a little
    lab[..., 1:] = np.clip(ab * chroma + 128, 0, 255).astype(np.uint8)
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.09 * np.clip(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H * 0.42) / (H * 0.72)) ** 2, 0, 1) ** 1.5)[..., None].astype(np.float32)
del yy, xx
def finish(img):                                                        # 4K: thresholded unsharp + vignette
    g = img.astype(np.float32); d = g - cv2.GaussianBlur(g, (0, 0), 1.6)
    g = g + 0.6 * d * (np.abs(d) > 2.0)
    return np.clip(g * VIG, 0, 255).astype(np.uint8)

# ---------- geometry ----------
ZOOM = [(1.00, 1.025), (1.09, 1.11)]                                    # alternating per clip: wide push / punched
AX, AY = 540, 760                                                       # face anchor (1080 space)
def host_M(t):
    """1080-space affine for the host at output time t (punch-ins), or None in the split."""
    if t < T_SPLIT: u = t / T_SPLIT; z = 1.0 + 0.03 * smooth(u)
    else:
        k = next((i for i, s in enumerate(MAIN) if s["t0"] <= t < s["t1"]), len(MAIN) - 1); s = MAIN[k]
        z0, z1 = ZOOM[k % 2]; u = (t - s["t0"]) / (s["t1"] - s["t0"]); z = z0 + (z1 - z0) * smooth(u)
    return np.float64([[z, 0, AX - AX * z], [0, z, AY - AY * z], [0, 0, 1]])
def plate_state(t):
    for p in PLATES:
        if p["t0"] - 0.01 <= t <= p["t1"] + p["out"]:
            a = eout((t - p["t0"]) / p["in"]); b = einout((t - p["t1"]) / p["out"]) if t > p["t1"] else 0
            m = a * (1 - b); return m, p
    return 0, None
def plate_M(m, p):
    s = 1 + (p["s"] - 1) * m; rot = math.radians(p["rot"] * m)
    cx = 540 + (p["cx"] - 540) * m; cy = 960 + (p["cy"] - 960) * m
    c, si = math.cos(rot) * s, math.sin(rot) * s
    # scale+rotate about the frame centre, then move the centre to (cx, cy)
    return np.float64([[c, -si, cx - (c * 540 - si * 960)], [si, c, cy - (si * 540 + c * 960)], [0, 0, 1]])
S4 = np.float64([[K, 0, 0], [0, K, 0], [0, 0, 1]])
def warp(img, M3, size=(W, H)):
    return cv2.warpAffine(img, M3[:2].astype(np.float32), size, flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
def rrect_mask(M3, r):
    m = np.zeros((H, W), np.uint8)
    pts = np.float64([[0, 0, 1], [1080, 0, 1], [1080, 1920, 1], [0, 1920, 1]]) @ (S4 @ M3).T
    # rounded corners: draw at 4× supersampling-free precision with a polygon of the rounded rectangle in 1080 space
    rr = []
    for (x, y, a0) in [(1080 - r, r, -90), (1080 - r, 1920 - r, 0), (r, 1920 - r, 90), (r, r, 180)]:
        for a in np.linspace(a0, a0 + 90, 12): rr.append([x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a)), 1])
    P = (np.float64(rr) @ (S4 @ M3).T)[:, :2]
    cv2.fillPoly(m, [np.round(P * 4).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=2)
    return cv2.GaussianBlur(m, (0, 0), 1.0)
BG = np.array([14, 13, 12], np.float32)
PX0, PY0, PX1, PY1 = 212, 368, 1030, 592                                # the pop-up's box in her square (measured)
PM = np.zeros((1080, 1080), np.float32); PM[PY0:PY1, PX0:PX1] = 1; PM = cv2.GaussianBlur(PM, (0, 0), 4)[..., None]
_c = cv2.VideoCapture(SAMPLE); _c.set(cv2.CAP_PROP_POS_FRAMES, 76); _f = _c.read()[1][:, 462:1542]; _c.release()
CUR = (cv2.cvtColor(_f[108:168, 556:608], cv2.COLOR_BGR2GRAY) > 228).astype(np.float32)   # the screen recording's hand cursor
def hide_cursor(sq):                                                    # find the hand by shape, paint it out from its surroundings
    g = (cv2.cvtColor(sq, cv2.COLOR_BGR2GRAY) > 228).astype(np.float32)
    r = cv2.matchTemplate(g, CUR, cv2.TM_CCORR_NORMED); _, v, _, (x, y) = cv2.minMaxLoc(r)
    if v < 0.86: return sq
    m = np.zeros(sq.shape[:2], np.uint8); m[y:y + CUR.shape[0], x:x + CUR.shape[1]] = (CUR * 255).astype(np.uint8)
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    return cv2.inpaint(sq, m, 7, cv2.INPAINT_TELEA)
def hide_popup(sq):                                                     # blur only inside the pop-up, as strongly as it is visible
    box = cv2.cvtColor(sq[PY0:PY1, PX0:PX1], cv2.COLOR_BGR2GRAY)
    a = 1.0 if (box < 40).mean() > 0.3 else 0.0                         # the card is on for frames 56–95 at ~58 % cover, off ≤ 6 %
    if a <= 0: return sq
    b = cv2.GaussianBlur(cv2.resize(cv2.resize(sq, (36, 36), interpolation=cv2.INTER_AREA), (1080, 1080)), (0, 0), 10)
    return (sq * (1 - a * PM) + b * a * PM).astype(np.uint8)                                # near-black behind the plate (BGR)

# ---------- sources ----------
class Seq:
    def __init__(s, path, fps): s.cap, s.fps, s.i, s.f = cv2.VideoCapture(path), fps, -1, None
    def at(s, t):
        want = max(0, round(t * s.fps))
        if want < s.i: s.cap.set(cv2.CAP_PROP_POS_FRAMES, want); s.i = want - 1
        while s.i < want:
            ok, f = s.cap.read()
            if not ok: break
            s.f = f; s.i += 1
        return s.f
host, samp = Seq(HOST, HFPS), Seq(SAMPLE, 30)
listen = []                                                              # cache the silent tail for the ping-pong
cl = cv2.VideoCapture(HOST); cl.set(cv2.CAP_PROP_POS_FRAMES, round(L0 * HFPS))
for _ in range(int((L1 - L0) * HFPS)):
    ok, f = cl.read()
    if not ok: break
    listen.append(grade(f))
cl.release()
def listen_frame(u):                                                     # u: seconds into the split
    n = len(listen); k = int(u * 30) % (2 * n - 2); return listen[k if k < n else 2 * n - 2 - k]
def host_src_t(t):
    if t < T_SPLIT: return E["intro"][0] + t
    s = next((s for s in MAIN if s["t0"] <= t < s["t1"]), MAIN[-1]); return s["src0"] + t - s["t0"]

def frame(t):
    sp_in = eout((t - T_SPLIT) / 0.38) if t >= T_SPLIT else 0
    sp_out = einout((t - T_MAIN) / 0.40) if t >= T_MAIN else 0
    p = sp_in * (1 - sp_out)                                             # 1 = fully split
    in_split = T_SPLIT <= t < T_MAIN
    if in_split: hf = listen_frame(t - T_SPLIT); Mh = np.eye(3)
    else: hf = grade(host.at(host_src_t(t))); Mh = host_M(t)
    m, pl = plate_state(t)
    if p > 0.001:                                                        # split: host pushed down by 650p, sample panel on top
        Mh = np.float64([[1, 0, 0], [0, 1, 650 * p], [0, 0, 1]]) @ Mh
        out = warp(hf, S4 @ Mh)
        sq = samp.at(min(max(t - T_SPLIT, 0), 10.73))[:, 462:1542].copy()  # the square picture inside the pillarbox
        if 50 <= samp.i <= 96: sq = hide_popup(sq)                      # Instagram "… liked your reel" pop-up: a stranger's username
        sq = hide_cursor(sq)
        sq = grade(sq, wb=np.array([0.98, 1.0, 1.02], np.float32), chroma=1.04, local=0.25)
        top = int(round(960 * p * K))
        if top > 0:
            # her clip has a burned-in title + cursor in the top 12 % and two-line captions in the bottom 20 %:
            # keep the clean middle of her square, scaled ×1.33 to fill the half-screen
            z = 960 / 720                                               # source window x 55–865, y 135–855
            Ms = np.float64([[K * z, 0, -K * z * 55], [0, K * z, K * (960 * p - 960) - K * z * 135], [0, 0, 1]])
            panel = warp(sq, Ms, (W, top))
            out[:top] = panel
        return finish(out)
    if pl is not None and m > 0.001:
        Mp = plate_M(m, pl)
        img = warp(hf, S4 @ Mp @ Mh).astype(np.float32)
        msk = rrect_mask(Mp, pl["r"] * m / (1 + (pl["s"] - 1) * m)).astype(np.float32)[..., None] / 255     # visible radius grows 0 → r
        out = img * msk + BG * (1 - msk)
        return finish(out.astype(np.uint8))
    return finish(warp(hf, S4 @ Mh))

if "--test" in sys.argv:
    ts = [float(v) for v in sys.argv[sys.argv.index("--test") + 1].split(",")]
    cv2.imwrite(DST, np.hstack([cv2.resize(frame(t), (540, 960), interpolation=cv2.INTER_AREA) for t in ts])); sys.exit()
NF = int(round(END * FPS))
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                       "-color_primaries", "bt709", "-color_trc", "bt709", DST], stdin=subprocess.PIPE)
for i in range(NF):
    ff.stdin.write(frame(i / FPS).tobytes())
    if i % 150 == 0: print(f"{i}/{NF}", flush=True)
ff.stdin.close(); ff.wait(); print("frames", NF)
