# Build the footage track (base.mp4, 1080×1920, 60 fps, no audio) from the screenplay's shot list.
# Every shot: source in-point, its slot on the timeline, optional rotation, then fill-crop to 9:16, light HD sharpen, shared grade.
# Shots carry XF/2 s handles on both sides and are joined with XF-second xfade transitions centred on each cut, so every
# cut keeps its time on the timeline. Graphics-only slots (logo, montage, client wall, analytics, end card) are black;
# overlay.html draws them and their own transitions.
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
UP = "/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e"
DR = os.environ.get("DRIVE", "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/ol/drive")
BR = os.path.join(HERE, "..", "oneloop-day-brolls", "out")
SRC = {
    "scrum": (f"{BR}/BROLL_06_scrum_meet.mp4", ""), "testing": (f"{BR}/BROLL_09_testing_what_we_built_DRAFT-small-artifacts.mp4", ""),
    "gate": (f"{BR}/BROLL_02_gate_open.mp4", ""), "door": (f"{BR}/BROLL_03_door_open.mp4", ""),
    "emails": (f"{BR}/BROLL_05_checking_emails.mp4", ""), "coding": (f"{BR}/BROLL_07_heads_down_coding.mp4", ""),
    "bugcheck": (f"{BR}/BROLL_08_bro_check_this_bug.mp4", ""),
    "m0424": (f"{DR}/MVI_0424.mp4", "transpose=2,"), "m0425": (f"{DR}/MVI_0425.mp4", "transpose=2,"),
    "m0431": (f"{DR}/MVI_0431.mp4", "transpose=2,"), "m0432": (f"{DR}/MVI_0432.mp4", "transpose=2,"),
    "m0440": (f"{DR}/MVI_0440.mp4", "transpose=2,"),
    "bts": (f"{UP}/7863d88a-IMG_0075_2.MOV", ""),                       # rotation flag → ffmpeg auto-rotates upright
    "night": (f"{DR}/brand/softcore_20min_edit.mp4", "eq=gamma=1.35:saturation=1.2,"), "olreel": (f"{DR}/brand/one_loop_reel_2.mp4", ""),
    "trufit": (f"{DR}/brand/be_tru_fit_3.mp4", ""), "futuro": (f"{DR}/brand/IMG_1121.mp4", ""),
}
# (timeline start, timeline end, source key, source in-point, source duration) — source dur ≠ slot dur → speed change.
# Footage runs a little into the graphics slots (18.70, 25.15, 32.25, 36.45) so the overlay can transition over moving picture.
SHOTS = [
    (0.00, 1.60, "testing", 0.40, 1.60), (1.60, 3.20, "scrum", 0.00, 1.30),
    (3.20, 3.87, "gate", 0.00, 0.666), (3.87, 4.64, "door", 0.00, 0.766),
    (4.64, 5.55, "night", 3.55, 0.91), (5.55, 6.85, "m0432", 4.20, 1.30),
    (6.85, 8.10, "bts", 1.00, 1.25), (8.10, 9.50, "bts", 3.00, 1.40),
    (9.50, 11.60, "m0425", 4.20, 2.10), (11.60, 12.75, "olreel", 21.00, 1.70),
    (12.75, 14.10, "m0424", 1.00, 1.35), (14.10, 15.75, "emails", 0.00, 1.65),
    (15.75, 16.75, "coding", 0.00, 1.00), (16.75, 17.40, "bts", 0.00, 0.65),
    (17.40, 18.70, "m0431", 1.00, 1.30), (18.70, 19.60, None, 0, 0),
    (19.60, 20.55, "m0440", 4.90, 0.95), (20.55, 21.30, "trufit", 12.65, 0.75),
    (21.30, 22.00, "futuro", 0.00, 0.70), (22.00, 23.30, "m0424", 4.00, 1.30),
    (23.30, 25.15, "bugcheck", 0.20, 1.85), (25.15, 32.25, None, 0, 0),
    (32.25, 34.10, "m0440", 1.70, 1.85), (34.10, 36.45, "bts", 10.20, 1.71), (36.45, 38.00, None, 0, 0),
]
# transition into shot i (i ≥ 1); the ones touching a black graphics slot sit under the overlay
XFT = [None, "smoothleft", "zoomin", "smoothleft", "hblur", "smoothup", "zoomin", "smoothleft", "hblur", "smoothdown",
       "zoomin", "smoothleft", "smoothup", "smoothleft", "hblur", "fade", "fade", "smoothleft", "smoothup", "zoomin",
       "smoothleft", "fade", "fade", "smoothup", "fade"]
XF, FPS, DUR = 0.24, 60, 38.0
H = XF / 2
SEG = os.path.join(HERE, "out", "seg"); os.makedirs(SEG, exist_ok=True)
GRADE = "eq=contrast=1.05:saturation=1.06:gamma=0.98,unsharp=5:5:0.55:5:5:0.0"
parts = []
for i, (a, b, key, s0, sd) in enumerate(SHOTS):
    out = os.path.join(SEG, f"s{i:02d}.mp4")
    ha, hb = (H if i > 0 else 0), (H if i < len(SHOTS) - 1 else 0)
    n = round((b - a + ha + hb) * FPS)
    if key is None:
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r={FPS}:d={n / FPS + 0.1}",
               "-frames:v", str(n), "-c:v", "libx264", "-crf", "10", "-pix_fmt", "yuv420p", out]
    else:
        src, pre = SRC[key]; speed = sd / (b - a)
        start = s0 - ha * speed; pad = max(0.0, -start) / speed; start = max(0.0, start)  # no source before 0 → hold the first frame
        vf = (f"{pre}setpts=(PTS-STARTPTS)/{speed:.5f},fps={FPS},tpad=start_duration={pad:.4f}:start_mode=clone:stop_duration=1:stop_mode=clone,"
              f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,{GRADE}")
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{start:.4f}", "-t", f"{(n / FPS) * speed + 0.3:.4f}", "-i", src, "-an", "-vf", vf,
               "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p", out]
    subprocess.run(cmd, check=True); parts.append(out)
    print(f"s{i:02d} {a:6.2f}-{b:6.2f} {key or '(graphics)':9s} {n} frames  in: {XFT[i] or '-'}")
# xfade chain: transition i is centred on the cut at SHOTS[i][0]
inputs = sum((["-i", p] for p in parts), [])
fc, last = [], "[0:v]"
for i in range(1, len(parts)):
    lab = f"[x{i}]" if i < len(parts) - 1 else "[v]"
    fc.append(f"{last}[{i}:v]xfade=transition={XFT[i]}:duration={XF}:offset={SHOTS[i][0] - H:.4f}{lab}"); last = lab
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]",
                "-frames:v", str(round(DUR * FPS)), "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p",
                os.path.join(HERE, "out", "base.mp4")], check=True)
print("base.mp4 done")
