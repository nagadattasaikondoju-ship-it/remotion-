# Picture: every shot of out/edit.json + the caption frames (out/ov, from `node render.mjs overlay`) -> out/video.mp4
# (1080x1920, 60 fps, no audio). This is the only encode of the footage: the MASTER is this file untouched.
#   /usr/bin/python3 -P base.py
# Sony originals are stored landscape (1920x1080, 59.94 fps): transpose=2 makes them upright at exactly 1080x1920, so every
# kennel shot is shown pixel for pixel (no zoom, no crop, no sharpening). Grades are ffmpeg filters applied while decoding.
# Zoom keys other than 1.0 still work (affine transform), but v2 uses none: a push-in enlarges the picture and softens it.
import json, os, subprocess, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, "out", "edit.json"))); FPS = E["fps"]; W, H = 1080, 1920
GRADE = {
    # the "Maximus" intro: a dark, red-lit hero portrait like the reference's Doberman (crushed blacks, warm red highlights, vignette)
    "maximus": "eq=contrast=1.16:saturation=0.72:gamma=1.06,"
               "colorbalance=rs=0.09:gs=-0.03:bs=-0.07:rm=0.11:gm=-0.02:bm=-0.06:rh=0.05:bh=-0.04",
    # the hook is the reference's own shot: leave its look alone
    "ref": "null",
    # the cute shots: bright, soft and warm
    "cute": "eq=brightness=0.025:contrast=1.04:saturation=1.10:gamma=1.03,colorbalance=rm=0.025:bm=-0.02:rh=0.015",
}

def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def zoom_at(keys, t):
    if t <= keys[0][0]: return keys[0][1]
    for (t0, z0), (t1, z1) in zip(keys, keys[1:]):
        if t <= t1: return z0 + (z1 - z0) * ease((t - t0) / max(1e-6, t1 - t0))
    return keys[-1][1]

def frames(sh, n):
    sp = sh.get("speed", 1.0); slow = f"setpts=(PTS-STARTPTS)/{sp}" if sp != 1.0 else ""
    vf = ",".join(x for x in ["transpose=2" if sh["rotate"] else "", sh.get("pre", ""), slow, f"fps={FPS}", GRADE[sh["grade"]]] if x)
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{sh['in']:.3f}", "-i", sh["src"], "-t", f"{n / FPS * sh.get('speed', 1.0) + 0.2:.3f}",
                          "-vf", vf + f",scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) == W * H * 3: last = Image.frombytes("RGB", (W, H), b)
        if last is None: raise SystemExit(f"no frames: {sh['src']}")
        yield last
    p.kill(); p.wait()

_spot = {}
def spotlight(img, ax, ay):  # "maximus": the face stays lit, the rest of the frame falls to near-black (the reference's studio look)
    if (ax, ay) not in _spot:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); d = np.sqrt(((xx - ax) / 520) ** 2 + ((yy - ay) / 720) ** 2)
        _spot[(ax, ay)] = (0.16 + 0.84 * np.clip(1.35 - d, 0, 1) ** 1.6)[..., None]
    return Image.fromarray((np.asarray(img, np.float32) * _spot[(ax, ay)]).astype(np.uint8))

def main():
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "8", "-tune", "film",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", os.path.join(HERE, "out", "video.mp4")],
                           stdin=subprocess.PIPE)
    total = 0; OV = os.path.join(HERE, "out", "ov"); f0 = 0
    for sh in E["shots"]:
        n = round((sh["start"] + sh["dur"]) * FPS) - round(sh["start"] * FPS); ax, ay = sh["anchor"]
        for k, img in enumerate(frames(sh, n)):
            z = zoom_at(sh["zoom"], k / FPS)
            ox = min(0, max(W - W * z, ax - ax * z)); oy = min(0, max(H - H * z, ay - ay * z))   # zoom about the anchor, never past an edge
            fr = img.transform((W, H), Image.AFFINE, (1 / z, 0, -ox / z, 0, 1 / z, -oy / z), resample=Image.BICUBIC) if abs(z - 1) > 1e-4 else img
            if sh["grade"] == "maximus": fr = spotlight(fr, ax, ay)
            ov = Image.open(os.path.join(OV, f"{f0 + k:05d}.png"))   # captions + emoji for this frame
            if ov.getbbox(): fr = Image.alpha_composite(fr.convert("RGBA"), ov.convert("RGBA")).convert("RGB")
            enc.stdin.write(fr.tobytes())
        f0 += n; total += n; print(f"{sh['id']} {n} frames", flush=True)
    enc.stdin.close(); enc.wait(); print(f"out/video.mp4: {total} frames ({total / FPS:.3f} s)")

if __name__ == "__main__": main()
