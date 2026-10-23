"""Render the graded, denoised 1080x1920 picture cut (no overlays, no audio) → assets/base.mp4.

Run: python3 scripts/build_cut.py [piece indices to re-render]
Each shot is rotated to portrait at native resolution, face-centred crop (zoom ≥ 1), chapter grade,
temporal denoise and a light sharpen; shots are concatenated frame-exactly.
"""
import hashlib
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import FPS, SCR, SEGS, SHOTS, SRC, START, LEN, TOTAL_F, SPEECH_F, F, J_LEN, WHIP  # noqa: E402

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
    """expand SHOTS into single-source pieces: (f0, f1, src, src_in, z0, z1, centre, fx)"""
    def anchor(s):
        return START[s[1]] if s[0] == "J" else F(s[1], s[2])
    bounds = [anchor(s) for s in SHOTS] + [SPEECH_F]
    out = []
    for k, s in enumerate(SHOTS):
        f0, f1 = bounds[k], bounds[k + 1]
        if s[0] == "B":
            _, _, _, src, sin, z, c = s
            out.append((f0, f1, src, sin, z, z, c, None))
            continue
        if s[0] == "J":  # carry the previous speaker's picture past their last word
            _, _, b, vsrc, voff = SEGS[s[1] - 1]
            last = out[-1]
            out.append((f0, f1, vsrc, round(voff + b, 3), last[5], last[5], last[6], None))
            continue
        zz = s[3] if isinstance(s[3], tuple) else (s[3], s[3])
        eye = s[4] if len(s) > 4 else EYE_Y
        # split across dialogue segments (picture follows the audio's source time)
        for i, (_, a, b, vsrc, voff) in enumerate(SEGS):
            g0, g1 = max(f0, START[i]), min(f1, START[i] + LEN[i])
            if g0 >= g1:
                continue
            sin = voff + a + (g0 - START[i]) / FPS
            za = zz[0] + (zz[1] - zz[0]) * (g0 - f0) / (f1 - f0)
            zb = zz[0] + (zz[1] - zz[0]) * (g1 - f0) / (f1 - f0)
            c = face_centre(vsrc, sin, sin + (g1 - g0) / FPS)
            c = (c[0], c[1], eye) if eye != EYE_Y else c
            out.append((g0, g1, vsrc, round(sin, 3), round(za, 4), round(zb, 4), c, None))
    # end hold: last clean frame of the selfie, very slow push, for the Part 2 lockup
    last = out[-1]
    out.append((SPEECH_F, TOTAL_F, last[2], 18.88, 1.0, 1.03, last[6], "freeze"))
    # whip: split the frames around the real camera whip into single frames with directional blur
    blur = dict(WHIP)
    res = []
    for p in out:
        f0, f1 = p[0], p[1]
        cuts = sorted({f0, f1} | {f for f in blur if f0 < f < f1} | {f + 1 for f in blur if f0 <= f < f1})
        for g0, g1 in zip(cuts, cuts[1:]):
            r = (g0 - f0) / (f1 - f0)
            r1 = (g1 - f0) / (f1 - f0)
            za, zb = p[4] + (p[5] - p[4]) * r, p[4] + (p[5] - p[4]) * r1
            sin = p[3] if p[7] == "freeze" else round(p[3] + (g0 - f0) / FPS, 3)
            fx = p[7] or (("blur", blur[g0]) if g0 in blur and g1 == g0 + 1 else None)
            res.append((g0, g1, p[2], sin, round(za, 4), round(zb, 4), p[6], fx))
    return res


def piece_file(p):
    key = json.dumps([p[1] - p[0]] + list(p[2:]) + [SRC[p[2]], GRADE[SRC[p[2]][2]]], default=str)
    return os.path.join(TMP, "s_" + hashlib.sha1(key.encode()).hexdigest()[:16] + ".mp4")


def render(p, out):
    f0, f1, src, sin, z0, z1, c, fx = p
    path, rot, grade, dn = SRC[src]
    n = f1 - f0
    cx, cy = c[:2] if c else (W / 2, H / 2)
    ey = (c[2] if len(c) > 2 else EYE_Y) if c else 0.5
    z = f"({z0}+({z1}-{z0})*n/{max(n - 1, 1)})"
    ow, oh = f"2*trunc({W}*{z}/2)", f"2*trunc({H}*{z}/2)"
    x = f"max(0,min(iw-{W},{cx}*iw/{W}-{W / 2}))"
    y = f"max(0,min(ih-{H},{cy}*ih/{H}-{H * ey}))"
    vf = ",".join(filter(None, [
        "transpose=2" if rot else None,
        f"fps={FPS}",
        f"trim=end_frame=1,loop=loop={n}:size=1:start=0,setpts=N/{FPS}/TB" if fx == "freeze" else None,
        dn,
        f"scale=w='{ow}':h='{oh}':eval=frame:flags=lanczos",
        f"crop={W}:{H}:x='{x}':y='{y}'",
        GRADE[grade],
        f"dblur=angle=8:radius={fx[1]}" if isinstance(fx, tuple) else None,
        "unsharp=5:5:0.45:5:5:0",
        "format=yuv420p",
    ]))
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{sin:.3f}", "-i", path, "-an", "-vf", vf, "-frames:v", str(n),
           "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p", out]
    subprocess.run(cmd, check=True)
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                              "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    if got != n:
        raise SystemExit(f"piece {src}@{sin:.2f}: {got} frames, wanted {n}")


if __name__ == "__main__":
    ps = pieces()
    files = []
    for i, p in enumerate(ps):
        f = piece_file(p)
        if not os.path.exists(f):
            render(p, f)
        files.append(f)
        print(f"p{i:02d} {p[0] / FPS:6.2f}-{p[1] / FPS:6.2f}  {p[2]:5s} @{p[3]:6.2f}  z {p[4]:.2f}->{p[5]:.2f}  c {p[6]}"
              f"  {p[7] or ''}", flush=True)
    lst = os.path.join(TMP, "list.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    tmp = os.path.join(ROOT, "assets", "_base_tmp.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", tmp], check=True)
    os.replace(tmp, os.path.join(ROOT, "assets", "base.mp4"))  # atomic: the cut-out job may be reading it
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_frames", "-of", "csv=p=0", os.path.join(ROOT, "assets", "base.mp4")],
                           capture_output=True, text=True).stdout)
    print("base.mp4", n, "frames (expected", TOTAL_F, ")", TOTAL_F / FPS, "s")
