# Talking-head pass: person mask (DeepLabV3-MobileNetV3, torchvision) → background softly defocused and dimmed,
# punch-ins per clip (alternating, to hide the jump cuts), tone curve + warm balance + vignette. Raw frames → ffmpeg.
#   PYTHONPATH=<pillow> python3 tools/grade.py out/base.mov out/graded.mov [--test t1,t2 out.jpg]
import sys, json, subprocess, cv2, numpy as np, torch
from torchvision.models.segmentation import deeplabv3_mobilenet_v3_large, DeepLabV3_MobileNet_V3_Large_Weights
torch.set_num_threads(4)
SRC, DST = sys.argv[1], sys.argv[2]
W, H, FPS = 1080, 1920, 30
clips = json.load(open("edl.json"))["clips"]
bounds = np.cumsum([0] + [b - a for a, b, _ in clips])
# (start scale, end scale) per clip; face anchor (x, y) stays put while the frame scales around it
ZOOM = [(1.42, 1.50), (1.00, 1.03), (1.13, 1.15), (1.00, 1.06), (1.13, 1.15), (1.00, 1.02), (1.14, 1.16), (1.00, 1.03),
        (1.12, 1.15), (1.00, 1.03), (1.13, 1.15), (1.00, 1.04), (1.13, 1.15), (1.00, 1.03), (1.20, 1.22), (1.00, 1.02)]
ANCHOR = [(540, 770)] + [(540, 790)] * (len(clips) - 1)
def tone_lut():
    x = np.arange(256) / 255.0
    y = x * 0.94                                                     # −0.1 stop
    y = np.where(y > 0.62, 0.62 + (y - 0.62) * 0.62, y)              # roll off the blown white walls
    y = y + 0.06 * np.sin(np.pi * (y - 0.08) / 0.84) * (y > 0.08) * (y < 0.92)   # gentle S: denser mids
    y = np.clip(y, 0, 1) ** 1.04
    return (y * 255).clip(0, 255).astype(np.uint8)
LUT = tone_lut()
FRAME = [0]
yy, xx = np.mgrid[0:H, 0:W]
VIG = 1 - 0.22 * np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.45) / (H * 0.62)) ** 2, 0, 1) ** 1.3
VIG = VIG[..., None].astype(np.float32)
model = deeplabv3_mobilenet_v3_large(weights=DeepLabV3_MobileNet_V3_Large_Weights.DEFAULT).eval()
MEAN = np.array([0.485, 0.456, 0.406], np.float32); STD = np.array([0.229, 0.224, 0.225], np.float32)
def person(f):
    s = cv2.resize(f, (288, 512), interpolation=cv2.INTER_AREA)[:, :, ::-1].astype(np.float32) / 255
    x = torch.from_numpy(((s - MEAN) / STD).transpose(2, 0, 1))[None]
    with torch.no_grad(): return model(x)["out"][0].softmax(0)[15].numpy()
def process(f, t, prev):
    k = min(int(np.searchsorted(bounds, t, side="right") - 1), len(clips) - 1)
    u = (t - bounds[k]) / max(1e-6, bounds[k + 1] - bounds[k]); z0, z1 = ZOOM[k]; z = z0 + (z1 - z0) * (u * u * (3 - 2 * u))
    ax, ay = ANCHOR[k]
    M = np.float32([[z, 0, ax - ax * z], [0, z, ay - ay * z]])
    f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    new_clip = prev is None or prev[1] != k
    if new_clip or FRAME[0] % 2 == 0:                                  # mask every other frame (held between), fresh on each cut
        m = person(f); m = m if new_clip else 0.6 * m + 0.4 * prev[0]  # temporal smoothing inside a clip only
    else:
        m = prev[0]
    FRAME[0] += 1
    mk = cv2.resize(m, (W // 4, H // 4)); mk = cv2.erode(mk, np.ones((4, 4), np.uint8)); mk = cv2.GaussianBlur(mk, (0, 0), 2.75)
    mk = np.clip((cv2.resize(mk, (W, H)) - 0.35) / 0.5, 0, 1)[..., None]
    g = cv2.LUT(f, LUT).astype(np.float32)
    g *= np.array([0.95, 1.0, 1.035], np.float32)                     # BGR: warmer
    lum = g.mean(axis=2, keepdims=True); g = lum + (g - lum) * 1.06    # +6 % saturation
    bg = cv2.resize(cv2.GaussianBlur(cv2.resize(g, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 1.75), (W, H)) * 0.74
    out = (g * mk + bg * (1 - mk)) * VIG
    return np.clip(out, 0, 255).astype(np.uint8), (m, k)
if "--test" in sys.argv:
    ts = [float(v) for v in sys.argv[sys.argv.index("--test") + 1].split(",")]; cap = cv2.VideoCapture(SRC); rows = []
    for t in ts:
        cap.set(cv2.CAP_PROP_POS_FRAMES, round(t * FPS)); ok, f = cap.read(); o, _ = process(f, t, None)
        rows.append(np.hstack([cv2.resize(f, (360, 640)), cv2.resize(o, (360, 640))]))
    cv2.imwrite(sys.argv[-1], np.vstack(rows) if len(rows) < 3 else np.hstack(rows)); sys.exit()
cap = cv2.VideoCapture(SRC)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "9", "-pix_fmt", "yuv420p", DST], stdin=subprocess.PIPE)
i, prev = 0, None
while True:
    ok, f = cap.read()
    if not ok: break
    o, prev = process(f, i / FPS, prev); ff.stdin.write(o.tobytes()); i += 1
    if i % 150 == 0: print(i, flush=True)
ff.stdin.close(); ff.wait(); print("frames", i)
