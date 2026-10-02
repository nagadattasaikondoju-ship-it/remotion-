"""Jump-cut the raw take into assets/cut.mp4 + assets/audio/voice.wav and print the
output-timeline map (segment starts, frame-snapped) used by index.html.

Run: python3 scripts/build_cut.py /path/to/VID_20260930_224751298_compressed.mp4

All times are on the *video* timeline of the source (the phone's AAC track starts
0.094 s late; audio is re-based with first_pts=0 so both share one clock). Every cut
sits inside a pause, a few frames before the next word, so the picture cut, the
caption and the SFX all land on the same frame. Pauses > 0.4 s are removed and the
two ~0.3 s mid-sentence pauses are tightened to ~0.1 s.
"""
import json
import os
import subprocess
import sys

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# (id, source start s, source end s)
SEGMENTS = [
    ("hook-a", 1.95, 4.62),  # "How many customers are calling your business right now"
    ("hook-b", 4.74, 5.90),  # "and nobody's picking up?"
    ("miss-a", 6.22, 7.17),  # "That missed call could"
    ("miss-b", 7.33, 8.56),  # "be a missed customer."
    ("build", 8.74, 14.35),  # "We build AI voice agents ... respond instantly."
    ("does-a", 14.60, 15.80),  # "They can qualify leads"
    ("does-b", 15.96, 19.38),  # "book appointments ... even after hours."
    ("home", 19.64, 22.16),  # "Your business shouldn't stop answering when you go home."
    ("cta", 22.40, 24.70),  # "Comment VOICE and I'll send you the demo."  (+0.3 s hold)
]


def fr(t):
    return round(t * FPS)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-3000:])
    return r


def main(src):
    n = len(SEGMENTS)
    vparts, aparts = [], []
    for i, (_, s0, s1) in enumerate(SEGMENTS):
        f0, f1 = fr(s0), fr(s1)
        t0, t1 = f0 / FPS, f1 / FPS
        d = t1 - t0
        vparts.append(f"[vs{i}]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS[v{i}]")
        aparts.append(
            f"[as{i}]atrim=start={t0:.6f}:end={t1:.6f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:d=0.006,afade=t=out:st={d - 0.012:.6f}:d=0.012[a{i}]"
        )
    # light grade: a touch of contrast + saturation, scaled to 1.2x the final frame so punch-ins stay sharp
    vsplit = "[0:v]fps=30,scale=1296:2304:flags=lanczos,eq=contrast=1.07:saturation=1.12:gamma=0.98,split=%d%s" % (
        n, "".join(f"[vs{i}]" for i in range(n)))
    asplit = "[0:a]aresample=48000:async=1:first_pts=0,aformat=channel_layouts=stereo,asplit=%d%s" % (
        n, "".join(f"[as{i}]" for i in range(n)))
    concat_v = "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vout]"
    concat_a = "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[araw]"
    graph = ";".join([vsplit, asplit] + vparts + aparts + [concat_v, concat_a])

    raw_wav = os.path.join(HERE, "_voice_raw.wav")
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", graph,
        "-map", "[vout]", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "21",
        "-pix_fmt", "yuv420p", "-g", "15", "-movflags", "+faststart",
        os.path.join(ROOT, "assets", "cut.mp4"),
        "-map", "[araw]", "-c:a", "pcm_s16le", raw_wav,
    ])

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
    for sid, s0, s1 in SEGMENTS:
        out.append({"id": sid, "src": fr(s0) / FPS, "frame": t, "start": round(t / FPS, 4), "frames": fr(s1) - fr(s0)})
        t += fr(s1) - fr(s0)
    print(json.dumps({"total_frames": t, "total": round(t / FPS, 4), "segments": out}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
