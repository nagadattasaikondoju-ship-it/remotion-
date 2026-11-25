"""Measures where the reference's stock presenter is on each frame of his slide-in (40.0-42.5 s) on the base (BASE env), and writes the
offsets into brand.html (const GOFF), so segment G's clean-plate patch covers him exactly. Silhouette = difference from the clean
frame at 40.6 s, at 420x746, below y 330 and away from the grass tile; offset = best horizontal shift of the held silhouette (43.0 s)."""
import numpy as np, subprocess, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "40.0", "-i", os.environ["BASE"], "-t", "3.1", "-vf", "scale=420:746", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, 746, 420).astype(np.int16); clean = F[18]
def mask(i):
    d = np.abs(F[i] - clean) > 22; d[:330] = False; d[:515, :245] = False; d[738:] = False; d[:, 409:] = False; return d
M = mask(90); offs = []
for i in range(20, 75):
    d = mask(i); best = min(range(0, 280), key=lambda dx: int(((np.pad(M, ((0, 0), (dx, 0)))[:, :420] & np.ones_like(M)) ^ d).sum()))
    offs.append(best)
p = "brand.html"; s = open(p).read(); s = re.sub(r"const GOFF = \[[^\]]*\];", "const GOFF = " + json.dumps(offs) + ";", s); open(p, "w").write(s)
print("GOFF", offs)
