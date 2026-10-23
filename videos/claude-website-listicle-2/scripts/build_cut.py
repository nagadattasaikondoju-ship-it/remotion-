"""Trim the raw take into assets/cut.mp4 + assets/audio/voice.wav.

Run: python3 scripts/build_cut.py /path/to/VID_20261014_110328767_1_1.mp4

One continuous range: from just before "10 things" to ~1.3 s after the final
"first" (the natural pauses between items are only 0.27-0.4 s, so they stay).

Reframe: the presenter is shifted down 200 px so the face sits in the centre /
lower part of the frame and the headline, checklist and browser card get clean
wall. The new top band is the plain wall (source rows 100-160, which no frame's
hair ever reaches) stretched and blurred; the bottom 200 px (hands/shirt) are
cropped. Audio is re-based (the phone's AAC starts 0.079 s late) and cleaned.
"""
import json
import os
import subprocess
import sys

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
F0, F1 = 48, 897  # source frames on a 30 fps grid: 1.600 s -> 29.900 s
SHIFT = 200       # px the presenter moves down
STRIP = (100, 160)  # clean wall rows used for the top band


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-3000:])
    return r


def main(src):
    t0, t1 = F0 / FPS, F1 / FPS
    top_h = STRIP[1] + SHIFT
    body_h = 1920 - top_h
    vf = (
        f"[0:v]fps=30,trim=start_frame={F0}:end_frame={F1},setpts=PTS-STARTPTS,split[a][b];"
        f"[a]crop=1080:{STRIP[1] - STRIP[0]}:0:{STRIP[0]},scale=1080:{top_h}:flags=bicubic,gblur=sigma=6:sigmaV=18[top];"
        f"[b]crop=1080:{body_h}:0:{STRIP[1]}[body];"
        f"[top][body]vstack,eq=contrast=1.05:saturation=1.08:gamma=0.98[v]"
    )
    af = (
        f"[0:a]aresample=48000:async=1:first_pts=0,aformat=channel_layouts=stereo,"
        f"atrim=start={t0:.6f}:end={t1:.6f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
        f"afade=t=out:st={t1 - t0 - 0.3:.6f}:d=0.3[a]"
    )
    raw = os.path.join(HERE, "_voice_raw.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", vf + ";" + af,
         "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
         "-g", "15", "-movflags", "+faststart", os.path.join(ROOT, "assets", "cut.mp4"),
         "-map", "[a]", "-c:a", "pcm_s16le", raw])
    chain = ("highpass=f=85,afftdn=nr=8:nf=-55,equalizer=f=250:t=q:w=1.1:g=-2.5,"
             "equalizer=f=3200:t=q:w=1.2:g=2.5,highshelf=f=9000:g=1.5,"
             "acompressor=threshold=-22dB:ratio=3:attack=4:release=90:makeup=2")
    meas = run(["ffmpeg", "-hide_banner", "-i", raw, "-af",
                chain + ",loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"]).stderr
    m = json.loads(meas[meas.rindex("{"): meas.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", chain + "," + ln, "-ar", "48000", "-ac", "2",
         os.path.join(ROOT, "assets", "audio", "voice.wav")])
    os.remove(raw)
    print(json.dumps({"frames": F1 - F0, "duration": round((F1 - F0) / FPS, 4), "src_start": t0}))


if __name__ == "__main__":
    main(sys.argv[1])
