# Build the footage track (base.mp4, 1080×1920, 60 fps, no audio) from the screenplay's shot list.
# Every shot: source in-point, its slot on the timeline, optional rotation, then fill-crop to 9:16, light HD sharpen, shared grade.
# The one graphics-only slot (client logo wall) is black here; overlay.html draws it.
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
UP = "/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e"
DR = os.environ.get("DRIVE", "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/ol/drive")
BR = os.path.join(HERE, "..", "oneloop-day-brolls", "out")
SRC = {
    "scrum": (f"{BR}/BROLL_06_scrum_meet.mp4", ""), "testing": (f"{BR}/BROLL_09_testing_what_we_built_DRAFT-small-artifacts.mp4", ""),
    "arrive": (f"{BR}/BROLL_04_checking_in_DRAFT-small-artifacts.mp4", ""),
    "emails": (f"{BR}/BROLL_05_checking_emails.mp4", ""), "coding": (f"{BR}/BROLL_07_heads_down_coding.mp4", ""),
    "bugcheck": (f"{BR}/BROLL_08_bro_check_this_bug.mp4", ""),
    "m0424": (f"{DR}/MVI_0424.mp4", "transpose=2,"), "m0425": (f"{DR}/MVI_0425.mp4", "transpose=2,"),
    "m0431": (f"{DR}/MVI_0431.mp4", "transpose=2,"), "m0432": (f"{DR}/MVI_0432.mp4", "transpose=2,"),
    "m0440": (f"{DR}/MVI_0440.mp4", "transpose=2,"),
    "bts": (f"{UP}/7863d88a-IMG_0075_2.MOV", ""),                       # rotation flag → ffmpeg auto-rotates upright
    "night": (f"{DR}/brand/softcore_20min_edit.mp4", "eq=gamma=1.35:saturation=1.2,"), "olreel": (f"{DR}/brand/one_loop_reel_2.mp4", ""),
}
# (timeline start, timeline end, source key, source in-point, source duration) — source dur ≠ slot dur → speed change.
# Video time = VO time − 1.05 s throughout (one continuous VO, no gap). Plain cuts.
SHOTS = [  # one shot per spoken line where possible, 1–2.6 s each, each picked to show what the line says
    (0.00, 1.60, "testing", 0.40, 1.60),    # "We made ₹95,000…": the team testing what they built
    (1.60, 3.31, "scrum", 0.00, 1.31),      # "…in two months": whiteboard scrum
    (3.31, 4.70, "arrive", 0.00, 1.39),     # "A few friends in Hyderabad": two of them arriving at the office
    (4.70, 5.70, "night", 3.55, 0.91),      # "Late nights": the city at night
    (5.70, 6.95, "m0432", 4.60, 1.25),      # "Back-to-back calls": on a call
    (6.95, 8.20, "bts", 0.20, 1.25),        # "Building for brands…": the shoot crew
    (8.20, 9.55, "bts", 3.00, 1.35),        # "…that had never heard of us": shooting for a brand
    (9.55, 11.75, "m0425", 4.20, 2.20),     # "Most brands don't have a traffic problem": thinking at the laptop
    (11.75, 12.80, "olreel", 21.00, 1.55),  # "They have a leak": the notification pile
    (12.80, 14.15, "m0424", 1.00, 1.35),    # "So we start with an audit": opening the laptop
    (14.15, 15.80, "emails", 0.00, 1.65),   # "find what's holding them back"
    (15.80, 16.85, "coding", 0.00, 1.05),   # "build the fix"
    (16.85, 19.75, "m0431", 1.00, 2.90),    # "market it and automate" (8.43× proof) → "That's OneLoop" (logo over the shot)
    (19.75, 21.40, "m0440", 5.00, 1.65),    # "Developers, designers"
    (21.40, 23.40, "m0424", 4.00, 2.00),    # "marketers and AI builders"
    (23.40, 24.75, "bugcheck", 0.30, 1.35), # "One team, one loop"
    (24.75, 28.45, None, 0, 0),             # 21+ brands: the client logo wall (overlay, full frame)
    (28.45, 30.50, "m0440", 1.70, 2.05),    # "We're just getting started" (6,406 proof)
    (30.50, 34.50, "bts", 10.20, 3.00),     # "Come grow with us" → end card over the shot
]
FPS, DUR = 60, 34.5
SEG = os.path.join(HERE, "out", "seg"); os.makedirs(SEG, exist_ok=True)
GRADE = "eq=contrast=1.05:saturation=1.06:gamma=0.98,unsharp=5:5:0.55:5:5:0.0"
parts = []
for i, (a, b, key, s0, sd) in enumerate(SHOTS):
    out = os.path.join(SEG, f"s{i:02d}.mp4"); n = round(b * FPS) - round(a * FPS)
    if key is None:
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r={FPS}:d={n / FPS + 0.1}",
               "-frames:v", str(n), "-c:v", "libx264", "-crf", "10", "-pix_fmt", "yuv420p", out]
    else:
        src, pre = SRC[key]; speed = sd / (b - a)
        vf = (f"{pre}setpts=(PTS-STARTPTS)/{speed:.5f},fps={FPS},tpad=stop_duration=1:stop_mode=clone,"
              f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,{GRADE}")
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{s0}", "-t", f"{sd + 0.3}", "-i", src, "-an", "-vf", vf,
               "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p", out]
    subprocess.run(cmd, check=True); parts.append(out)
    print(f"s{i:02d} {a:6.2f}-{b:6.2f} {key or '(graphics)':9s} {n} frames")
lst = os.path.join(SEG, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", os.path.join(HERE, "out", "base.mp4")], check=True)
print("base.mp4 done")
