# Swap the reference ad's foreign people for Indian people (Pexels photos, free licence) and its brand for Dr. Sri Sushma's,
# keeping every original animation, caption and transition. Works on the AI-upscaled base (1080x1920, frame n = original n).
#   python3 composite.py BASE.mp4 OUT.mp4            full render (only the listed frames change; the rest pass through)
#   python3 composite.py BASE.mp4 --stills 170 290   QA stills -> out/stills/c_<n>.png
# Per shot: the new photo is cropped to the shot's framing, given a slow push-in like the original clip, then matched row by row
# to the original frame's colour statistics (that reproduces the ad's blue grade and its fades), and the original captions are
# lifted back on top with a colour/box mask, so text animation stays exactly as it was.
import os, sys, subprocess, json
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
PX = os.environ.get("PHOTOS", "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/ref4/px/full")
LOGO = os.environ.get("LOGO", os.path.join(HERE, "..", "sushma-jerry-reel", "out", "logo.png"))
W, H = 1080, 1920
K = H / 742                               # original pixel -> base pixel

def load(name):
    return cv2.cvtColor(cv2.imread(os.path.join(PX, name)), cv2.COLOR_BGR2RGB).astype(np.float32)

# shot table: frames, photo, crop focus (fx, fy in the photo, 0..1) + where that point lands on screen, zoom, region, text boxes
SHOTS = [
    dict(name="toothache", f=(154, 191), photo="3808804.jpg", focus=(0.42, 0.33), at=(540, 440), zoom=(1.0, 1.05),
         canvas_top=560, top=610, feather=120, text=[(0, 250, 1080, 640)]),
    dict(name="open mouth", f=(240, 325), photo="6502742.jpg", focus=(0.60, 0.58), at=(560, 720), zoom=(1.0, 1.06),
         canvas_top=480, top=520, feather=220, text=[(0, 230, 1080, 600)]),
    dict(name="bad taste", f=(359, 396), photo="4584059.jpg", focus=(0.50, 0.42), at=(540, 900), zoom=(1.0, 1.04),
         top=0, feather=1, text=[(0, 820, 1080, 1120)], skip_white=True),
    dict(name="odor", f=(397, 415), photo="4584059.jpg", focus=(0.52, 0.52), at=(640, 760), zoom=(1.55, 1.62), mirror=True,
         top=0, feather=1, text=[(0, 820, 1080, 1120)], skip_white=True),
    dict(name="good news", f=(781, 799), photo="6977987.jpg", focus=(0.50, 0.40), moving=True,
         text=[(0, 420, 1080, 960)]),
    dict(name="dentist", f=(834, 904), photo="8224633.jpg", focus=(0.60, 0.50), at=(560, 1000), zoom=(1.0, 1.06),
         top=0, feather=1, text=[(0, 800, 1080, 1100), (0, 1360, 1080, 1660)], skip_white=True),
]

def place(photo, sh, u, out_h=H, mirror=False):  # noqa: C901
    """Cover-crop the photo onto a W x out_h canvas so its focus point lands at sh['at'], zoom eased from z0 to z1."""
    if mirror: photo = photo[:, ::-1]
    ph, pw = photo.shape[:2]
    z0, z1 = sh["zoom"]; z = z0 + (z1 - z0) * (u * u * (3 - 2 * u))
    s = max(W / pw, out_h / ph) * z
    fx, fy = sh["focus"]; ax, ay = sh["at"]
    M = np.float32([[s, 0, ax - fx * pw * s], [0, s, ay - fy * ph * s]])
    # keep the canvas covered
    M[0, 2] = min(0, max(W - pw * s, M[0, 2])); M[1, 2] = min(0, max(out_h - ph * s, M[1, 2]))
    return cv2.warpAffine(photo, M, (W, out_h), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)

def text_mask(o, boxes):
    """Captions of the original frame: white Montserrat and the saturated blue condensed caps, inside the given boxes."""
    m = np.zeros(o.shape[:2], np.float32)
    if not boxes: return m
    r, g, b = o[..., 0], o[..., 1], o[..., 2]
    white = (np.minimum(np.minimum(r, g), b) > 214) & ((np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) < 45)
    blue = (b > 215) & (r < 75) & (g < 135) & (b - r > 160)      # the caption blue (~26,104,248), not the ad's lighter gradient
    t = (white | blue).astype(np.float32)
    for x0, y0, x1, y1 in boxes: m[y0:y1, x0:x1] = t[y0:y1, x0:x1]
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=1)
    return cv2.GaussianBlur(m, (0, 0), 1.0)

def match_rows(n, o, keep, sigma=110):
    """Give the new layer the original frame's per-row mean and spread (per channel), smoothed along y."""
    w = (1 - keep)[..., None]
    def stats(a):
        s = (a * w).sum(1) / np.maximum(w.sum(1), 1)
        v = ((a - s[:, None]) ** 2 * w).sum(1) / np.maximum(w.sum(1), 1)
        return cv2.GaussianBlur(s, (1, 0), sigma), cv2.GaussianBlur(np.sqrt(v), (1, 0), sigma)
    mo, so = stats(o); mn, sn = stats(n)
    ratio = np.clip(so / np.maximum(sn, 1), 0.2, 1.25)
    return np.clip((n - mn[:, None]) * ratio[:, None] + mo[:, None], 0, 255)

_cache = {}
def photo(name):
    if name not in _cache: _cache[name] = load(name)
    return _cache[name]

def region_mask(sh):
    m = np.ones((H, W), np.float32)
    t = sh.get("top", 0); fe = sh.get("feather", 1)
    if t > 0:
        y = np.arange(H)[:, None]; m = np.clip((y - t) / fe, 0, 1) * np.ones((1, W), np.float32)
    return m

def moving_mask(o, clean):
    """Where the original's sliding photo is (vs the clean background of the same shot), softened like its own edges."""
    d = np.abs(o - clean).max(2)
    m = (d > 38).astype(np.float32)
    m[:int(300 * K)] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    return cv2.GaussianBlur(m, (0, 0), 6)

def composite(n, o, base_clean=None):
    for sh in SHOTS:
        a, b = sh["f"]
        if not (a <= n <= b): continue
        if sh.get("skip_white") and o.mean() > 232: return o            # the white flash frames stay as they are
        u = (n - a) / max(1, b - a)
        if sh.get("moving"):
            # The original is a cut-out (woman + red tooth) that pops in big from the bottom-left, settles by frame 789 and
            # slides out left from 795. Clear the rows under the caption to the clean blue (each row's colour at the right edge),
            # then pop the new woman in the same way as a soft oval cut-out, and put the caption back on top.
            tm = text_mask(o, sh["text"])
            plate = o.copy(); y0 = int(300 * K)
            plate[y0:] = o[y0:, 860:1060].mean(1, keepdims=True)
            # fill each row from the clean right edge, but keep the original's left-right shading measured just above
            ref = cv2.GaussianBlur(o[300:360].mean(0)[None], (0, 0), 60)[0]; shade = ref - ref[860:1060].mean(0)   # clean rows above the caption
            plate[y0:] = o[y0:, 860:1060].mean(1, keepdims=True) + shade[None]
            r = np.linspace(0, 1, 240)[:, None, None]; z0 = y0 - 120
            plate[z0:z0 + 240] = o[z0:z0 + 240] * (1 - r) + plate[z0:z0 + 240] * r
            ease = lambda x: 1 - (1 - min(1, max(0, x))) ** 3
            e = ease((n - 781) / 8.0); xo = -760 * (min(1, max(0, (n - 795) / 4.0)) ** 2)
            s = 0.62 * (1 + 0.9 * (1 - e))
            cx = 60 + (300 - 60) * e + xo; cy = 1700 + (1150 - 1700) * e
            p = photo(sh["photo"]); ph, pw = p.shape[:2]; fx, fy = sh["focus"]
            M = np.float32([[s, 0, cx - fx * pw * s], [0, s, cy - 80 * s / 0.62 - fy * ph * s]])
            newl = cv2.warpAffine(p, M, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REFLECT)
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            rx, ry = 340 * s / 0.62, 430 * s / 0.62
            m = np.clip((1 - np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)) / 0.18, 0, 1)
            m = m * np.clip((yy - (y0 - 40)) / 80, 0, 1)
            newl = newl * 0.94 + np.array([12, 18, 40], np.float32) * 0.06 + 6      # a touch of the ad's cool lift
            out = plate * (1 - m[..., None]) + newl * m[..., None]
            return out * (1 - tm[..., None]) + o * tm[..., None]
        ct = sh.get("canvas_top", 0)
        newl = np.empty((H, W, 3), np.float32)
        newl[ct:] = place(photo(sh["photo"]), sh, u, out_h=H - ct, mirror=sh.get("mirror", False)); newl[:ct] = newl[ct]
        tm = text_mask(o, sh["text"])
        newl = match_rows(newl, o, tm)
        rm = region_mask(sh)[..., None]
        out = o * (1 - rm) + newl * rm
        return out * (1 - tm[..., None]) + o * tm[..., None]
    return o

# ---- end card: the other clinic's name, logo and number become Dr. Sri Sushma's -------------------------------------------
CARD = (1031, 1136)
FD = os.path.join(HERE, "fonts")
def font(n, s): return ImageFont.truetype(os.path.join(FD, n), s)

def white_logo(width):
    im = Image.open(LOGO).convert("RGB"); a = np.asarray(im).astype(np.float32)
    # blue badge on white: ink = how far from white, mostly in the red channel (blue has little red); drop the soft grey shadow
    ink = np.clip((235 - a[..., 0]) / 140, 0, 1) * (a[..., 2] - a[..., 0] > 25)
    rgba = np.zeros(a.shape[:2] + (4,), np.uint8); rgba[..., :3] = 255; rgba[..., 3] = (ink * 255).astype(np.uint8)
    lg = Image.fromarray(rgba); bb = lg.getbbox(); lg = lg.crop(bb)
    return lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)

def build_card(final):
    """final: the original's settled end card (float RGB). Returns the rebranded card."""
    img = final.copy()
    # wipe the old logo/name, the CALL line and the phone number: rebuild those rows from the clean blue at both sides
    for y0, y1, x0, x1 in [(int(195 * K), int(300 * K), 0, W), (int(352 * K), int(392 * K), 0, W), (int(560 * K), int(615 * K), int(97 * K), W)]:
        L = img[y0:y1, :max(1, x0 + 40)].mean(1) if x0 > 0 else img[y0:y1, :40].mean(1)
        R = img[y0:y1, -40:].mean(1)
        t = np.linspace(0, 1, W)[None, :, None]
        fill = L[:, None] * (1 - t) + R[:, None] * t
        img[y0:y1, x0:x1] = fill[:, x0:x1]
        img[y0:y1] = cv2.GaussianBlur(img[y0:y1], (0, 0), 2)
    pil = Image.fromarray(img.astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(pil)
    lg = white_logo(300); pil.alpha_composite(lg, ((W - lg.width) // 2, int(222 * K) - lg.height // 2 - 70))
    def ctext(y, s, f, fill=(255, 255, 255, 255), track=0):
        w = sum(f.getlength(c) for c in s) + track * (len(s) - 1); x = (W - w) / 2
        for c in s: d.text((x, y), c, font=f, fill=fill, anchor="lm"); x += f.getlength(c) + track
    ctext(int(268 * K), "Dr. Sri Sushma", font("Poppins-Bold.ttf", 60))
    ctext(int(290 * K), "MULTISPECIALITY DENTAL CLINIC", font("Montserrat-SemiBold.ttf", 28), track=2)
    ctext(int(372 * K), "CALL DR. SRI SUSHMA", font("Montserrat-Medium.ttf", 44))
    f = font("Montserrat-Medium.ttf", 56)
    num = "+91 79958 15454"; x = int(103 * K)
    d.text((x, int(588 * K)), num, font=f, fill=(255, 255, 255, 255), anchor="lm")
    return np.asarray(pil.convert("RGB")).astype(np.float32)

def card_frame(o, white, card_old, card_new):
    """The card fades in from the white flash: estimate how far each frame is along white -> card and apply it to the new card."""
    d = (card_old - white).reshape(-1); e = (o - white).reshape(-1)
    a = float(np.clip((d * e).sum() / max((d * d).sum(), 1), 0, 1.05))
    return white + a * (card_new - white)

# ---- driver ---------------------------------------------------------------------------------------------------------------
def frames(path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)

def main():
    base = sys.argv[1]
    stills = [int(x) for x in sys.argv[sys.argv.index("--stills") + 1:]] if "--stills" in sys.argv else None
    need = set(stills or [])
    clean_gn = None; card_old = card_new = None; white = None
    if stills:
        os.makedirs(os.path.join(HERE, "out", "stills"), exist_ok=True)
    else:
        out = sys.argv[2]
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                                "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    # first pass for the reference frames: the good-news background before the photo slides in, the settled end card
    for n, o in enumerate(frames(base)):
        if n == 781: clean_gn = o
        if n == 1100: card_old = o; break
    card_new = build_card(card_old); white = np.full_like(card_old, 255.0)
    for n, o in enumerate(frames(base)):
        if stills is not None and n not in need: continue
        if CARD[0] <= n <= CARD[1]: r = card_frame(o, white, card_old, card_new)
        else: r = composite(n, o, clean_gn)
        r = np.clip(r, 0, 255).astype(np.uint8)
        if stills is not None: Image.fromarray(r).save(os.path.join(HERE, "out", "stills", f"c_{n}.png"))
        else: enc.stdin.write(r.tobytes())
        if stills is not None and n >= max(need): break
    if stills is None:
        enc.stdin.close(); enc.wait()

if __name__ == "__main__": main()
