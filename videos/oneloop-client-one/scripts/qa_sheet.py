"""Caption-coverage proof: one frame from the middle of every caption card of the final render → renders/caption_coverage.jpg

Run: python3 scripts/qa_sheet.py renders/<final>.mp4
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
video = sys.argv[1]
html = open(os.path.join(ROOT, "index.html")).read()
D = json.loads(re.search(r"const D = (\{.*?\});\n", html, re.S).group(1))
tmp = os.path.join(ROOT, "renders", "_qa")
os.makedirs(tmp, exist_ok=True)
font = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
files = []
for k, c in enumerate(D["caps"]):
    t = c["t0"] + 0.62 * (c["t1"] - c["t0"])
    out = os.path.join(tmp, f"{k:02d}.png")
    label = f"{k + 1}  {t:.2f}s  {c['mode']}"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-vf",
                    f"scale=216:384,drawtext=fontfile={font}:text='{label}':x=4:y=4:fontsize=13:fontcolor=white:"
                    f"box=1:boxcolor=black@0.7", out], check=True)
    files.append(out)
cols = 8
while len(files) % cols:
    pad = os.path.join(tmp, f"pad{len(files)}.png")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", "color=black:s=216x384", "-frames:v", "1",
                    pad], check=True)
    files.append(pad)
args = sum([["-i", f] for f in files], [])
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *args, "-filter_complex",
                f"xstack=inputs={len(files)}:grid={cols}x{len(files) // cols}",
                os.path.join(ROOT, "renders", "caption_coverage.jpg")], check=True)
for f in files:
    os.remove(f)
os.rmdir(tmp)
print("renders/caption_coverage.jpg", len(D["caps"]), "cards")
