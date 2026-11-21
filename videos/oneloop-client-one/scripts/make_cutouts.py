"""Cut the speaker out (alpha WebM) for every behind-subject caption range → assets/cut/cutNN.webm

Run: python3 scripts/make_cutouts.py   (after build_html.py wrote assets/cut/ranges.json)
Uses `hyperframes remove-background` (u2net human segmentation, local). Ranges already cut (same frames) are reused; delete a file to force a re-cut.
"""
import json
import os
import subprocess

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CUT = os.path.join(ROOT, "assets", "cut")
FPS = 30
ranges = json.load(open(os.path.join(CUT, "ranges.json")))
for k, (a, b) in enumerate(ranges):
    out = os.path.join(CUT, f"cut_{a}_{b}.webm")  # named by frame range so unchanged ranges are reused
    if os.path.exists(out):
        continue
    seg = os.path.join(CUT, f"_seg{k:02d}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, "assets", "base.mp4"), "-vf",
                    f"trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS", "-an", "-c:v", "libx264", "-crf", "8",
                    "-pix_fmt", "yuv420p", seg], check=True)
    subprocess.run(["npx", "--yes", "hyperframes@0.8.78", "remove-background", seg, "-o", out, "--quality", "best"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(seg)
    print("cut-out", k, a, b, flush=True)
print("all cut-outs ready")
