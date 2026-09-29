"""Jump-cut the raw take into assets/cut.mp4 + assets/audio/voice.wav.

Run: python3 scripts/build_cut.py /path/to/VID_20260929_115222677_1.mp4

Cut points are in source *video* frames on a 30 fps grid (the phone's AAC track
starts 0.099 s after the video, so audio is re-based with first_pts=0 before
trimming). Every item boundary sits a few frames before the first word so the
cut, the list pop and the SFX all land together.
"""
import json
import os
import subprocess
import sys

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# (id, first frame, end frame exclusive, voice on?)
SEGMENTS = [
    ("hook", 50, 125, True),  # "Ten things you can tell Claude to add to your website"
    ("dark-mode", 130, 162, True),
    ("cookie-banner", 169, 202, True),
    ("back-to-top", 202, 233, True),  # contiguous with the cookie line, no cut
    ("mobile-menu", 237, 266, True),
    ("shortcuts", 269, 295, True),
    ("hover", 303, 323, True),
    ("scroll-bar", 326, 355, True),
    ("skeleton", 359, 391, True),
    ("faqs", 395, 437, True),  # "and" before "password" is dropped
    ("password", 448, 479, True),
    ("outro", 479, 524, False),  # silent smile hold under the CTA
]


def run(cmd):
    print(" ".join(cmd[:6]), "...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-3000:])
    return r


def main(src):
    n = len(SEGMENTS)
    vparts, aparts = [], []
    for i, (_, f0, f1, voice) in enumerate(SEGMENTS):
        t0, t1 = f0 / FPS, f1 / FPS
        d = t1 - t0
        vparts.append(f"[vs{i}]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS[v{i}]")
        if voice:
            aparts.append(
                f"[as{i}]atrim=start={t0:.6f}:end={t1:.6f},asetpts=PTS-STARTPTS,"
                f"afade=t=in:d=0.006,afade=t=out:st={d - 0.012:.6f}:d=0.012[a{i}]"
            )
        else:
            aparts.append(f"[as{i}]atrim=start={t0:.6f}:end={t1:.6f},asetpts=PTS-STARTPTS,volume=0[a{i}]")
    vsplit = "[0:v]fps=30,split=%d%s" % (n, "".join(f"[vs{i}]" for i in range(n)))
    asplit = "[0:a]aresample=48000:async=1:first_pts=0,aformat=channel_layouts=stereo,asplit=%d%s" % (
        n,
        "".join(f"[as{i}]" for i in range(n)),
    )
    concat_v = "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vout]"
    concat_a = "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[araw]"
    graph = ";".join([vsplit, asplit] + vparts + aparts + [concat_v, concat_a])

    raw_wav = os.path.join(HERE, "_voice_raw.wav")
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", graph,
        "-map", "[vout]", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-g", "15", "-movflags", "+faststart",
        os.path.join(ROOT, "assets", "cut.mp4"),
        "-map", "[araw]", "-c:a", "pcm_s16le", raw_wav,
    ])

    # Voice polish: rumble cut, light denoise, de-mud, presence + air, glue, -14 LUFS.
    chain = (
        "highpass=f=85,afftdn=nr=8:nf=-55,"
        "equalizer=f=250:t=q:w=1.1:g=-2.5,equalizer=f=3200:t=q:w=1.2:g=3,"
        "highshelf=f=9000:g=1.5,"
        "acompressor=threshold=-22dB:ratio=3:attack=4:release=90:makeup=2"
    )
    meas = run([
        "ffmpeg", "-hide_banner", "-i", raw_wav, "-af",
        chain + ",loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-",
    ]).stderr
    m = json.loads(meas[meas.rindex("{"): meas.rindex("}") + 1])
    ln = (
        f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    )
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", raw_wav, "-af", chain + "," + ln,
        "-ar", "48000", "-ac", "2", os.path.join(ROOT, "assets", "audio", "voice.wav"),
    ])
    os.remove(raw_wav)

    t, out = 0, []
    for sid, f0, f1, _ in SEGMENTS:
        out.append({"id": sid, "frame": t, "start": round(t / FPS, 4), "dur": round((f1 - f0) / FPS, 4)})
        t += f1 - f0
    print(json.dumps({"total": round(t / FPS, 4), "segments": out}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
