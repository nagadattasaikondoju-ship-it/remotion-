# Picture: renders every shot of out/timeline.json into out/base.mp4 (1080x1920, 30 fps, no audio).
# Each source frame is placed with a sub-pixel affine transform (smooth push-ins, punch-ins, split screen, circle PiP, freezes).
#   /usr/bin/python3 -P base_render.py
import json, os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
TL = json.load(open(os.path.join(HERE, "out", "timeline.json")))
GRADE = {  # ffmpeg filters applied while decoding (WhatsApp-compressed 480p sources: light denoise first)
    "warm": "hqdn3d=1.2:1.2:5:5,eq=contrast=1.05:saturation=1.10,colorbalance=rm=0.02:bm=-0.02",
    "cool": "hqdn3d=1.2:1.2:5:5,eq=contrast=1.07:saturation=0.90,colorbalance=rs=-0.03:bs=0.04:rm=-0.02:bm=0.03:bh=0.02",
}
SPLIT_Y = 960                  # split screen: the motion-graphics panel is above, the speaker below
PIP_C, PIP_R = (250, 1590), 196  # circle picture-in-picture (overlay.html cuts the same hole)

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

def frames(src, t0, n, grade, transpose=False, single=False):
    path = TL["files"][src]; w, h = probe(path)
    if transpose: w, h = h, w
    vf = ",".join(x for x in ["fps=30", "transpose=2" if transpose else "", GRADE.get(grade, GRADE["cool"])] if x)
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t0:.3f}", "-i", path, "-t", f"{(1 if single else n) / FPS + 0.3:.3f}",
           "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    fs = [np.frombuffer(raw[i:i + w * h * 3], np.uint8).reshape(h, w, 3) for i in range(0, len(raw) - w * h * 3 + 1, w * h * 3)]
    if not fs: raise SystemExit(f"no frames from {src} at {t0}")
    if single: fs = fs[:1]
    while len(fs) < n: fs.append(fs[-1])
    return [Image.fromarray(f) for f in fs[:n]], w, h

def place(img, s, ox, oy, size=(W, H)):  # scale by s and put the source origin at (ox, oy)
    return img.transform(size, Image.AFFINE, (1 / s, 0, -ox / s, 0, 1 / s, -oy / s), resample=Image.BICUBIC)

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
    out.paste(part.crop((0, SPLIT_Y, W, H)), (0, SPLIT_Y)); return out

_mask = None
def pip_frame(img, w, h, anchor):
    global _mask
    side = 250; ax, ay = anchor; x0, y0 = ax - side / 2, ay + 22 - side / 2
    s = 2 * PIP_R / side; out = Image.new("RGB", (W, H))
    sq = place(img, s, -x0 * s, -y0 * s, (2 * PIP_R, 2 * PIP_R))
    if _mask is None:
        m = Image.new("L", (8 * PIP_R, 8 * PIP_R)); ImageDraw.Draw(m).ellipse((0, 0, 8 * PIP_R - 1, 8 * PIP_R - 1), fill=255)
        _mask = m.resize((2 * PIP_R, 2 * PIP_R), Image.LANCZOS)
    out.paste(sq, (PIP_C[0] - PIP_R, PIP_C[1] - PIP_R), _mask); return out

def main():
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-vf", "unsharp=5:5:0.55:5:5:0,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "12",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", os.path.join(HERE, "out", "base.mp4")],
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
        imgs, w, h = frames(sg["src"], sg["in"], n, grade, transpose=sg["src"] == "broll", single=single)
        for k in range(n):
            t = k / FPS; img = imgs[0] if single else imgs[k]; z = zoom_at(sg["zoom"], t)
            if sg["layout"] in ("full", "cover"): fr = full_frame(img, w, h, sg["anchor"], z, sg.get("centre", 0))
            elif sg["layout"] == "split": fr = split_frame(img, w, h, sg["anchor"], z)
            else: fr = pip_frame(img, w, h, sg["anchor"])
            if sg["grade"] == "freeze":   # the freeze: drained colour, a step darker (record-scratch moment)
                fr = ImageEnhance.Brightness(ImageEnhance.Color(fr).enhance(0.25)).enhance(0.78)
            if sg["grade"] == "hold":     # CTA hold: the speaker sinks back so the call to action reads
                fr = ImageEnhance.Brightness(fr.filter(ImageFilter.GaussianBlur(6))).enhance(0.42)
            enc.stdin.write(fr.tobytes())
        total += n; print(f"{sg['id']:5s} {n:4d} frames", flush=True)
    enc.stdin.close(); enc.wait(); print(f"out/base.mp4: {total} frames ({total / FPS:.2f} s)")

if __name__ == "__main__": main()
