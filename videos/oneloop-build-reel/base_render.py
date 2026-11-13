# Picture: renders every shot of out/timeline.json into out/base.mp4 (no audio).
#   /usr/bin/python3 -P base_render.py          4K: 2160x3840, 30 fps (the master; the HD copy is downscaled from it)
#   SC=1 NO_UP=1 BASE_OUT=base_1080.mp4 /usr/bin/python3 -P base_render.py   1080x1920 preview from the 480p originals
# Sources: the AI-upscaled takes in $SRC_DIR/up/ (tools/upscale_realesr.py, x4, with up/offsets.json) when present,
# else the original 480p files. Each frame is placed with a sub-pixel affine transform (push-ins, punch-ins, split screen,
# circle PiP, freezes). All layout numbers below are in 1080x1920 units and scaled by SC.
import json, os, subprocess, time, numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
SC = float(os.environ.get("SC", 2)); W, H, FPS = int(1080 * SC), int(1920 * SC), 30
TL = json.load(open(os.path.join(HERE, "out", "timeline.json")))
SRC = os.path.dirname(TL["files"]["skit"]); UP = os.path.join(SRC, "up")
OFFS = json.load(open(os.path.join(UP, "offsets.json"))) if os.path.exists(os.path.join(UP, "offsets.json")) else {}
GRADE = {  # ffmpeg filters applied while decoding (the 480p originals get a light denoise first; the upscaled files are clean)
    "warm": "eq=contrast=1.05:saturation=1.10,colorbalance=rm=0.02:bm=-0.02",
    "cool": "eq=contrast=1.07:saturation=0.90,colorbalance=rs=-0.03:bs=0.04:rm=-0.02:bm=0.03:bh=0.02",
}
SPLIT_Y = 960 * SC                                  # split screen: the motion-graphics panel is above, the speaker below
PIP_C, PIP_R = (310 * SC, 1470 * SC), 260 * SC      # circle picture-in-picture (overlay.html cuts the same hole)
PIP_SIDE, PIP_FACE = 400, (192, 292)                # source square (original px) around Tarun's face: hair to chin with room

def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def zoom_at(keys, t):
    if not keys: return 1.0
    if t <= keys[0][0]: return keys[0][1]
    for (t0, z0), (t1, z1) in zip(keys, keys[1:]):
        if t <= t1: return z0 + (z1 - z0) * ease((t - t0) / max(1e-6, t1 - t0))
    return keys[-1][1]

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip().split(",")
    return int(out[0]), int(out[1])

def source(src):
    """(path, time offset, scale of the file relative to the original)"""
    orig = TL["files"][src]; up = os.path.join(UP, f"{src}.mp4")
    busy = lambda: os.path.exists(os.path.join(UP, f"{src}.part.mp4")) or subprocess.run(["pgrep", "-f", "upscale_realesr"], capture_output=True).returncode == 0
    while src in OFFS and not os.path.exists(up) and not os.environ.get("NO_UP") and busy():
        time.sleep(10)                                  # its upscale is still running: wait for it rather than fall back to 480p
    if src in OFFS and os.path.exists(up) and not os.environ.get("NO_UP"): return up, OFFS[src], probe(up)[0] / probe(orig)[0]
    return orig, 0.0, 1.0

def frames(src, t0, n, grade, transpose=False, single=False):
    """yields n PIL frames (streamed: 4x-upscaled frames are big), plus the frame size and the anchor scale"""
    path, off, k = source(src); w, h = probe(path)
    if transpose: w, h = h, w
    pre = "hqdn3d=1.2:1.2:5:5" if k == 1 and src != "broll" else ""
    vf = ",".join(x for x in ["fps=30", "transpose=2" if transpose else "", pre, GRADE.get(grade, GRADE["cool"])] if x)
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{max(0, t0 - off):.3f}", "-i", path, "-t", f"{(1 if single else n) / FPS + 0.3:.3f}",
           "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE); sz = w * h * 3

    def gen():
        last = None
        for i in range(n):
            if not (single and last is not None):
                buf = p.stdout.read(sz)
                if len(buf) == sz: last = Image.frombytes("RGB", (w, h), buf)
            if last is None: raise SystemExit(f"no frames from {src} at {t0}")
            yield last
        p.stdout.close(); p.kill(); p.wait()
    return gen(), w, h, k

def place(img, s, ox, oy, size=None):  # scale by s and put the source origin at (ox, oy)
    return img.transform(size or (W, H), Image.AFFINE, (1 / s, 0, -ox / s, 0, 1 / s, -oy / s), resample=Image.BICUBIC)

def full_frame(img, w, h, anchor, z, centre=0.0):
    s0 = W / w; s = s0 * z
    ax, ay = anchor if anchor else (w / 2, h / 2)
    tx, ty = ax * s0, ay * s0                             # where the anchor sits at z = 1
    k = centre * min(1, max(0, (z - 1) / 0.6))            # punch-ins pull the anchor (a face) toward the centre as they zoom
    tx, ty = tx + (W / 2 - tx) * k, ty + (H * 0.36 - ty) * k
    ox, oy = tx - ax * s, ty - ay * s
    ox = min(0, max(W - w * s, ox)); oy = min(0, max(H - h * s, oy))  # never show past the frame edge
    return place(img, s, ox, oy)

def split_frame(img, w, h, anchor, z):
    bh = h / 2; y0 = min(h - bh, max(0, anchor[1] - 0.42 * bh))   # the face sits a little above the middle of the lower half
    s0 = W / w; s = s0 * z; cx, cy = w / 2, y0 + bh / 2
    ox, oy = W / 2 - cx * s, (SPLIT_Y + (H - SPLIT_Y) / 2) - cy * s
    ox = min(0, max(W - w * s, ox))
    out = Image.new("RGB", (W, H)); part = place(img, s, ox, oy)
    out.paste(part.crop((0, int(SPLIT_Y), W, H)), (0, int(SPLIT_Y))); return out

_mask = None
def pip_frame(img, w, h, k):
    """Tarun's whole head (hair to chin) in the circle: a PIP_SIDE square of the original frame around his face"""
    global _mask
    side = PIP_SIDE * k; x0 = min(w - side, max(0, PIP_FACE[0] * k - side / 2)); y0 = min(h - side, max(0, PIP_FACE[1] * k - side / 2))
    d = int(round(2 * PIP_R)); s = d / side; out = Image.new("RGB", (W, H))
    sq = place(img, s, -x0 * s, -y0 * s, (d, d))
    if _mask is None:
        m = Image.new("L", (4 * d, 4 * d)); ImageDraw.Draw(m).ellipse((0, 0, 4 * d - 1, 4 * d - 1), fill=255)
        _mask = m.resize((d, d), Image.LANCZOS)
    out.paste(sq, (int(round(PIP_C[0] - d / 2)), int(round(PIP_C[1] - d / 2))), _mask); return out

def main():
    name = os.environ.get("BASE_OUT", "base.mp4")
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-vf", "unsharp=5:5:0.35:5:5:0,noise=c0s=3:c0f=t,format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "14", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", os.path.join(HERE, "out", name)],
                           stdin=subprocess.PIPE)
    total = 0
    for sg in TL["segments"]:
        f0, f1 = round(sg["start"] * FPS), round((sg["start"] + sg["dur"]) * FPS); n = f1 - f0
        if sg["kind"] == "black":
            blank = np.zeros((H, W, 3), np.uint8).tobytes()
            for _ in range(n): enc.stdin.write(blank)
            total += n; continue
        single = sg["kind"] == "freeze"
        grade = "warm" if sg["grade"] in ("warm", "freeze") else "cool"
        imgs, w, h, k = frames(sg["src"], sg["in"], n, grade, transpose=sg["src"] == "broll", single=single)
        anchor = [a * k for a in sg["anchor"]] if sg["anchor"] else None
        held = None
        for i, img in enumerate(imgs):
            t = i / FPS; z = zoom_at(sg["zoom"], t)
            if sg["layout"] in ("full", "cover"): fr = full_frame(img, w, h, anchor, z, sg.get("centre", 0))
            elif sg["layout"] == "split": fr = split_frame(img, w, h, anchor, z)
            else: fr = pip_frame(img, w, h, k)
            if sg["grade"] == "freeze":   # the freeze: drained colour, a step darker (record-scratch moment)
                fr = ImageEnhance.Brightness(ImageEnhance.Color(fr).enhance(0.25)).enhance(0.78)
            if sg["grade"] == "hold":     # CTA hold: the speaker sinks back so the call to action reads (blurred once, it's a still)
                if held is None or abs(z - held[0]) > 0.004:
                    held = (z, ImageEnhance.Brightness(fr.filter(ImageFilter.GaussianBlur(6 * SC))).enhance(0.42))
                fr = held[1]
            enc.stdin.write(fr.tobytes())
        total += n; print(f"{sg['id']:5s} {n:4d} frames  ({os.path.basename(source(sg['src'])[0])})", flush=True)
    enc.stdin.close(); enc.wait(); print(f"out/{name}: {W}x{H}, {total} frames ({total / FPS:.2f} s)")

if __name__ == "__main__": main()
