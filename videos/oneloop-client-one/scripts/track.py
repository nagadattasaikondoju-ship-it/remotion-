"""Measure the finished picture cut (assets/base.mp4) for caption placement → assets/track.json

Run: python3 scripts/track.py
- faces: per-frame face box (cx, cy, w) on every A-roll piece, outlier-rejected and smoothed, so
  behind-subject captions sit just behind the head and can follow a moving speaker with damping.
- planes: per-frame partial-affine motion (2x3 matrix from the shot's first frame) of the background on the B-roll
  shots, so environment captions stay pinned to the wall / pavement / facade while the camera moves.
"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import FPS, TOTAL_F  # noqa: E402
import build_cut  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
W, H = 1080, 1920
S = 2  # analyse at half resolution


def frames():
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "assets", "base.mp4"), "-vf",
                          f"scale={W // S}:{H // S}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    n = (W // S) * (H // S)
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(H // S, W // S)


pieces = build_cut.pieces()
kind = np.array([""] * TOTAL_F, object)
piece_of = np.zeros(TOTAL_F, int)
for k, p in enumerate(pieces):
    kind[p[0]:p[1]] = "A" if p[6] is not None and p[4] >= 1.0 and p[2] in ("0647", "0658", "0662", "VID") else "B"
    piece_of[p[0]:p[1]] = k

cc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = [None] * TOTAL_F
F = list(frames())
assert len(F) == TOTAL_F, (len(F), TOTAL_F)
for i, g in enumerate(F):
    if kind[i] != "A" or i % 2:
        continue
    fs = cc.detectMultiScale(cv2.equalizeHist(g), 1.1, 5, minSize=(40, 40))
    if len(fs):
        x, y, w, h = max(fs, key=lambda r: r[2] * r[3])
        faces[i] = [(x + w / 2) * S, (y + h / 2) * S, w * S]

# per piece: reject outliers, interpolate, smooth
out_faces = {}
for k, p in enumerate(pieces):
    idx = [i for i in range(p[0], p[1]) if faces[i] is not None]
    if kind[p[0]] != "A" or not idx:
        continue
    arr = np.array([faces[i] for i in idx])
    med = np.median(arr, 0)
    ok = (np.abs(arr[:, 0] - med[0]) < 0.5 * med[2] + 60) & (np.abs(arr[:, 1] - med[1]) < 0.5 * med[2] + 60) & (
        np.abs(arr[:, 2] - med[2]) < 0.35 * med[2])
    idx = [i for i, o in zip(idx, ok) if o]
    arr = arr[ok]
    if not len(idx):
        continue
    rng = np.arange(p[0], p[1])
    cols = [np.interp(rng, idx, arr[:, c]) for c in range(3)]
    ker = np.ones(9) / 9
    sm = [np.convolve(np.pad(c, 4, mode="edge"), ker, "valid") for c in cols]
    for j, i in enumerate(rng):
        out_faces[int(i)] = [round(float(sm[0][j]), 1), round(float(sm[1][j]), 1), round(float(sm[2][j]), 1)]

# planar motion on every B-roll piece (whole-frame background; captions pick their own pieces)
planes = {}
for k, p in enumerate(pieces):
    if kind[p[0]] != "B" or p[1] - p[0] < 3:
        continue
    acc = np.eye(3)
    seq = [[1.0, 0.0, 0.0, 0.0, 1.0, 0.0]]
    prev = F[p[0]]
    pts = cv2.goodFeaturesToTrack(prev, 400, 0.01, 8)
    for i in range(p[0] + 1, p[1]):
        cur = F[i]
        m = None
        if pts is not None and len(pts) > 12:
            nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, pts, None, winSize=(21, 21), maxLevel=3)
            good = st.ravel() == 1
            if good.sum() > 12:
                m, _ = cv2.estimateAffinePartial2D(pts[good], nxt[good], method=cv2.RANSAC, ransacReprojThreshold=2.0)
        if m is not None:
            acc = np.vstack([m, [0, 0, 1]]) @ acc
        # 2x3 matrix mapping first-frame full-res coords → this frame
        seq.append([round(float(acc[0, 0]), 5), round(float(acc[0, 1]), 5), round(float(acc[0, 2]) * S, 2),
                    round(float(acc[1, 0]), 5), round(float(acc[1, 1]), 5), round(float(acc[1, 2]) * S, 2)])
        prev = cur
        pts = cv2.goodFeaturesToTrack(prev, 400, 0.01, 8)
    planes[str(k)] = {"f0": p[0], "f1": p[1], "src": p[2], "m": seq}

json.dump({"faces": out_faces, "planes": planes,
           "pieces": [[p[0], p[1], p[2], p[3]] for p in pieces]},
          open(os.path.join(ROOT, "assets", "track.json"), "w"))
print("faces", len(out_faces), "frames; planes", {k: (v["src"], len(v["m"]), v["m"][-1]) for k, v in planes.items()})
