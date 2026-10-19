"""Render the graded, denoised 1080x1920 picture cut (no overlays, no audio) → assets/base.mp4.

Run: python3 scripts/build_cut.py [piece indices to re-render]
Each shot is rotated to portrait at native resolution, face-centred crop (zoom ≥ 1), chapter grade,
temporal denoise and a light sharpen; shots are concatenated frame-exactly.
"""
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import FPS, SCR, SEGS, SHOTS, SRC, START, LEN, TOTAL_F, F  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TMP = os.path.join(SCR, "ol", "shots")
FT = os.path.join(SCR, "ol", "ft")
os.makedirs(TMP, exist_ok=True)
W, H = 1080, 1920
EYE_Y = 0.34  # face centre sits at 34% of frame height

GRADE = {
    "day": "eq=contrast=1.05:saturation=1.0:gamma=0.98,"
           "colorbalance=rs=0.02:bs=-0.02:rm=0.03:bm=-0.03:rh=0.05:gh=0.015:bh=-0.05,"
           "curves=all='0/0.02 0.5/0.5 1/0.96'",
    "broll": "eq=contrast=1.04:saturation=0.9:gamma=0.97,"
             "colorbalance=rm=0.03:bm=-0.03:rh=0.05:bh=-0.05,curves=all='0/0.02 0.6/0.58 1/0.93'",
    "dusk": "eq=contrast=1.10:saturation=1.08:gamma=1.20,"
            "colorbalance=bs=0.02:rm=0.04:bm=-0.03:rh=0.06:gh=0.02:bh=-0.05,"
            "curves=all='0/0 0.25/0.24 0.5/0.53 0.75/0.79 1/0.97'",
    "night": "eq=contrast=1.07:saturation=0.98:gamma=1.18,"
             "colorbalance=rs=-0.01:bs=0.02:rm=0.04:bm=-0.03:rh=0.05:gh=0.02:bh=-0.04,"
             "curves=all='0/0.02 0.5/0.5 1/0.97'",
    "phone": "eq=contrast=1.05:saturation=0.98:gamma=1.08,"
             "colorbalance=rs=-0.01:bs=0.02:rm=0.04:bm=-0.03:rh=0.05:gh=0.015:bh=-0.04",
}


def face_centre(src, t0, t1):
    """median face centre (rotated-frame px) over [t0, t1], rejecting off-cluster detections"""
    d = json.load(open(os.path.join(FT, f"{src}.json")))
    pts = np.array([[r[1], r[2]] for r in d if r[1] is not None], float)
    med = np.median(pts, 0)
    ok = lambda x, y: abs(x - med[0]) < 260 and abs(y - med[1]) < 320
    win = np.array([[r[1], r[2]] for r in d if r[1] is not None and t0 - 0.3 <= r[0] <= t1 + 0.3 and ok(r[1], r[2])])
    c = np.median(win, 0) if len(win) else med
    return round(float(c[0])), round(float(c[1]))


def pieces():
    """expand SHOTS into single-source pieces: (f0, f1, src, src_in, z0, z1, centre)"""
    bounds = [F(s[1], s[2]) for s in SHOTS] + [TOTAL_F]
    out = []
    for k, s in enumerate(SHOTS):
        f0, f1 = bounds[k], bounds[k + 1]
        if s[0] == "B":
            _, _, _, src, sin, z, c = s
            out.append((f0, f1, src, sin, z, z, c))
            continue
        zz = s[3] if isinstance(s[3], tuple) else (s[3], s[3])
        # split across dialogue segments (picture follows the audio's source time)
        for i, (_, a, b, vsrc, voff) in enumerate(SEGS):
            g0, g1 = max(f0, START[i]), min(f1, START[i] + LEN[i])
            if g0 >= g1:
                continue
            sin = voff + a + (g0 - START[i]) / FPS
            za = zz[0] + (zz[1] - zz[0]) * (g0 - f0) / (f1 - f0)
            zb = zz[0] + (zz[1] - zz[0]) * (g1 - f0) / (f1 - f0)
            c = face_centre(vsrc, sin, sin + (g1 - g0) / FPS)
            out.append((g0, g1, vsrc, round(sin, 3), round(za, 4), round(zb, 4), c))
    return out


def render(idx, p):
    f0, f1, src, sin, z0, z1, c = p
    path, rot, grade, dn = SRC[src]
    n = f1 - f0
    out = os.path.join(TMP, f"p{idx:02d}.mp4")
    cx, cy = c if c else (W / 2, H / 2)
    ey = EYE_Y if c else 0.5
    z = f"({z0}+({z1}-{z0})*n/{max(n - 1, 1)})"
    ow, oh = f"2*trunc({W}*{z}/2)", f"2*trunc({H}*{z}/2)"
    x = f"max(0,min(iw-{W},{cx}*iw/{W}-{W / 2}))"
    y = f"max(0,min(ih-{H},{cy}*ih/{H}-{H * ey}))"
    vf = ",".join(filter(None, [
        "transpose=2" if rot else None,
        f"fps={FPS}",
        dn,
        f"scale=w='{ow}':h='{oh}':eval=frame:flags=lanczos",
        f"crop={W}:{H}:x='{x}':y='{y}'",
        GRADE[grade],
        "unsharp=5:5:0.45:5:5:0",
        "format=yuv420p",
    ]))
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{sin:.3f}", "-i", path, "-an", "-vf", vf, "-frames:v", str(n),
           "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p", out]
    subprocess.run(cmd, check=True)
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                              "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    if got != n:
        raise SystemExit(f"piece {idx} {src}@{sin:.2f}: {got} frames, wanted {n}")


if __name__ == "__main__":
    ps = pieces()
    only = set(int(a) for a in sys.argv[1:])
    files = []
    for i, p in enumerate(ps):
        f = os.path.join(TMP, f"p{i:02d}.mp4")
        if not only or i in only or not os.path.exists(f):
            render(i, p)
        files.append(f)
        print(f"p{i:02d} {p[0] / FPS:6.2f}-{p[1] / FPS:6.2f}  {p[2]:5s} @{p[3]:6.2f}  z {p[4]:.2f}->{p[5]:.2f}  c {p[6]}",
              flush=True)
    lst = os.path.join(TMP, "list.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    os.path.join(ROOT, "assets", "base.mp4")], check=True)
    print("base.mp4", TOTAL_F, "frames", TOTAL_F / FPS, "s")
