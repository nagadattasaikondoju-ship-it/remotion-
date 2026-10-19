"""Dialogue edit + natural B-roll sound + restrained SFX → assets/audio/master.wav (48 kHz stereo, −14 LUFS).

Run: python3 scripts/build_audio.py
Dialogue comes from the DeepFilterNet-cleaned tracks (the WhatsApp phone recording replaces the noisy
camera audio for the 0658 section). No music bed — the post gets a quiet Instagram sound later.
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy.signal import butter, sosfilt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import BROLL, CLEAN, FPS, OVER, SEGS, START, TOTAL, T  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "assets", "audio")
os.makedirs(OUT, exist_ok=True)
SR = 48000
N = int(round(TOTAL * SR))
rng = np.random.default_rng(7)
CLEANED = {"0647": "0647_dn.wav", "AUD": "AUD_dn.wav", "0662": "0662_dn.wav", "VID": "VID_dn.wav"}


def load(path, ss=None, dur=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss}"] if ss is not None else []) + (
        ["-t", f"{dur}"] if dur is not None else []) + ["-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()


def save(path, x):
    x = np.atleast_2d(x)
    if x.shape[0] == 1:
        x = np.vstack([x, x])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_s24le", path], input=x.T.astype(np.float32).tobytes(), check=True)


def lufs(x):
    p = os.path.join(OUT, "_m.wav")
    save(p, x)
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    os.remove(p)
    return float(r.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])


def fade(x, ms_in=12, ms_out=12):
    a, b = int(ms_in * SR / 1000), int(ms_out * SR / 1000)
    x[:a] *= np.linspace(0, 1, a)
    x[-b:] *= np.linspace(1, 0, b)
    return x


def filt(x, kind, f, order=4):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output="sos"), x)


def env(n, a, tau):
    t = np.arange(n) / SR
    return np.clip(t / max(a, 1e-4), 0, 1) * np.exp(-np.maximum(t - a, 0) / tau)


def place(buf, x, t, gain_db):
    i = int(round(t * SR))
    x = x[: max(0, min(len(x), len(buf) - i))]
    buf[i:i + len(x)] += x * 10 ** (gain_db / 20)


# ---------------- dialogue ----------------
tracks = {k: load(os.path.join(CLEAN, f)) for k, f in CLEANED.items()}
pieces = {k: [] for k in tracks}
for i, (src, a, b, _, _) in enumerate(SEGS):
    x = tracks[src][int(a * SR):int(a * SR) + int(round((b - a) * FPS)) * SR // FPS].copy()
    pieces[src].append((i, x))
gain = {k: -20.0 - lufs(np.concatenate([x for _, x in v])) for k, v in pieces.items()}
voice = np.zeros(N, np.float32)
for src, v in pieces.items():
    for i, x in v:
        place(voice, fade(x * 10 ** (gain[src] / 20)), START[i] / FPS, 0)
raw = os.path.join(OUT, "_voice_raw.wav")
save(raw, voice)
chain = ("highpass=f=80,equalizer=f=220:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1.4:g=2.0,"
         "deesser=i=0.35,acompressor=threshold=-22dB:ratio=2.6:attack=8:release=140:makeup=2")
voice_p = os.path.join(OUT, "_voice_proc.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", chain, "-ar", str(SR), voice_p], check=True)
voice = load(voice_p)[:N]
voice = np.pad(voice, (0, N - len(voice)))
voice *= 10 ** ((-14.5 - lufs(voice)) / 20)

# ---------------- natural sound from the B-roll ----------------
nat = np.zeros(N, np.float32)
def natural(src, s_in, t0, t1, gdb, hp=150):
    x = load(os.path.join(BROLL, f"MVI_{src}.MP4"), s_in, t1 - t0)
    x = fade(filt(x, "highpass", hp), 40, 60)
    place(nat, x, t0, gdb - lufs(x))

natural("0436", 1.9, T(2, 1.50), T(2, 2.62), -31)          # footsteps, J-cut 0.3 s before the picture
natural("0431", 1.0, T(5, 9.90), T(6, 12.10), -33, 400)    # keys / trackpad under the build montage
natural("0446", 1.45, T(13, 8.20), T(13, 8.90), -30)       # real laptop lid closing

# ---------------- synthesized SFX (dry, short, restrained) ----------------
def t_axis(d):
    return np.arange(int(d * SR)) / SR


def paper():
    n = int(0.11 * SR)
    x = filt(rng.standard_normal(n), "bandpass", [900, 7000]) * env(n, 0.003, 0.03)
    return x * (1 + 0.6 * np.sin(2 * np.pi * 37 * np.arange(n) / SR))


def chime():
    t = t_axis(0.38)
    return (np.sin(2 * np.pi * 1318.5 * t) * env(len(t), 0.004, 0.09)
            + 0.8 * np.sin(2 * np.pi * 1760 * t) * np.where(t > 0.07, env(len(t), 0.004, 0.12), 0)
            + 0.15 * np.sin(2 * np.pi * 3520 * t) * env(len(t), 0.002, 0.04))


def sub():
    t = t_axis(0.55)
    f = 42 + 30 * np.exp(-t / 0.08)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.004, 0.16) + 0.08 * filt(
        rng.standard_normal(len(t)), "lowpass", 400) * env(len(t), 0.001, 0.03)


def tick():
    t = t_axis(0.05)
    return filt(filt(rng.standard_normal(len(t)), "bandpass", [1500, 5000]) * env(len(t), 0.0003, 0.004)
                + 0.6 * np.sin(2 * np.pi * 2200 * t) * env(len(t), 0.0005, 0.006), "lowpass", 4500)


def hit():
    t = t_axis(0.32)
    f = 70 + 60 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.09) + 0.2 * filt(
        rng.standard_normal(len(t)), "bandpass", [200, 1600]) * env(len(t), 0.001, 0.012)


def powerdown():
    t = t_axis(0.4)
    f = 820 * np.exp(-t / 0.12) + 120
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.12) * 0.7 + 0.3 * filt(
        rng.standard_normal(len(t)), "bandpass", [2000, 6000]) * env(len(t), 0.0003, 0.003)


def whoosh():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    lo = filt(x, "bandpass", [300, 1500]) * (1 - t / 0.3)
    hi = filt(x, "bandpass", [1500, 6000]) * (t / 0.3)
    return (lo + hi) * np.sin(np.pi * t / 0.3) ** 1.5


def riser():
    t = t_axis(0.7)
    shape = (t / 0.7) ** 2.2
    tone = sum(a * np.sin(2 * np.pi * f * t * (1 + 0.04 * t)) for f, a in ((220, 1), (329.6, 0.7), (440, 0.35)))
    return (tone + 0.4 * filt(rng.standard_normal(len(t)), "bandpass", [2000, 8000]) * shape) * shape


sfx = np.zeros(N, np.float32)
cues = []
def cue(name, fn, t, gdb):
    x = fn()
    x = x / (np.max(np.abs(x)) or 1)
    place(sfx, x, t, gdb)
    cues.append({"sfx": name, "t": round(t, 3), "peak_db": gdb})

p0, p1 = OVER["paper"]
for k, fr in enumerate([0, 6, 12, 17, 22, 26]):        # one flick per page of the match cut
    cue("paper flick", paper, p0 + fr / FPS, -30 if k < 5 else -27)
cue("payment chime", chime, T(7, 5.36), -24)              # after "₹1,500", never on top of it
cue("low sub impact", sub, T(8, 6.58), -20)
cue("clock tick", tick, T(9, 9.80), -30)                  # in the pause after "payments,"
cue("clock tick", tick, T(9, 12.40), -31)                 # after "the other.", into the black flash
cue("micro hit", hit, T(12, 4.22) - 0.01, -22)
cue("UI power-down", powerdown, OVER["notpub"][0] + 0.05, -27)
cue("air whoosh (real whip)", whoosh, T(13, 9.40), -24)
cue("micro riser", riser, TOTAL - 0.72, -26)

mix = voice + nat + sfx
pre = os.path.join(OUT, "_mix.wav")
save(pre, mix)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", "alimiter=limit=0.89:attack=3:release=40:level=false",
                "-ar", str(SR), "-c:a", "pcm_s24le", os.path.join(OUT, "master.wav")], check=True)
for f in ("_m.wav", "_voice_raw.wav", "_voice_proc.wav", "_mix.wav"):
    if os.path.exists(os.path.join(OUT, f)):
        os.remove(os.path.join(OUT, f))
json.dump(cues, open(os.path.join(OUT, "sfx_cues.json"), "w"), indent=1)
print("gain per source (dB):", {k: round(v, 1) for k, v in gain.items()})
print("voice LUFS", round(lufs(voice), 1), "| master LUFS", round(lufs(load(os.path.join(OUT, "master.wav"))), 1))
