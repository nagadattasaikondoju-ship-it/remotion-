"""Offline, deterministic SFX + a quiet electronic bed (48 kHz stereo WAVs in assets/audio).

Run after build_cut.py (the bed is side-chain ducked under assets/audio/voice.wav):
    python3 scripts/synth_sfx.py
"""
import os
import subprocess

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "audio")
DUR = 28.3
rng = np.random.default_rng(21)


def t_axis(d):
    return np.arange(int(d * SR)) / SR


def filt(x, kind, f, order=4):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output="sos"), x)


def env(n, a, tau):
    t = np.arange(n) / SR
    return np.clip(t / max(a, 1e-4), 0, 1) * np.exp(-np.maximum(t - a, 0) / tau)


def save(name, x, peak=0.89):
    x = x / (np.max(np.abs(x)) or 1.0) * peak
    f = min(len(x), int(0.004 * SR))
    x[-f:] *= np.linspace(1, 0, f)
    wavfile.write(os.path.join(OUT, name), SR, np.stack([x, x], 1).astype(np.float32))


def tone(f, d, tau, a=0.003, harm=(1.0, 0.3)):
    t = t_axis(d)
    return sum(h * np.sin(2 * np.pi * f * (k + 1) * t) for k, h in enumerate(harm)) * env(len(t), a, tau)


def tick():  # soft checklist tick
    t = t_axis(0.06)
    return np.sin(2 * np.pi * 2100 * t) * env(len(t), 0.0006, 0.012) + 0.25 * filt(
        rng.standard_normal(len(t)), "highpass", 5000) * env(len(t), 0.0002, 0.002)


def click():  # small UI click
    t = t_axis(0.05)
    return filt(rng.standard_normal(len(t)), "bandpass", [1800, 6500]) * env(len(t), 0.0002, 0.0035) + 0.5 * np.sin(
        2 * np.pi * 1300 * t) * env(len(t), 0.0004, 0.006)


def pop():
    t = t_axis(0.14)
    f = 360 + 560 * np.exp(-t / 0.02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.0015, 0.035)


def whoosh(d=0.42):
    n = int(d * SR)
    noise, out, hop = rng.standard_normal(n), np.zeros(n), 480
    for i in range(0, n, hop):
        c = 500 * (6000 / 500) ** (i / n)
        blk = filt(noise[max(0, i - 960): i + hop], "bandpass", [c * 0.6, c * 1.4], order=2)
        out[i: i + hop] = blk[-len(out[i: i + hop]):]
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5


def riser(d=1.45):  # subtle rising sweep into item one
    t = t_axis(d)
    f = 180 * (1400 / 180) ** (t / d)
    tonal = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35
    noise = rng.standard_normal(len(t))
    out, hop = np.zeros(len(t)), 480
    for i in range(0, len(t), hop):
        c = 600 * (7000 / 600) ** (i / len(t))
        blk = filt(noise[max(0, i - 960): i + hop], "bandpass", [c * 0.7, c * 1.3], order=2)
        out[i: i + hop] = blk[-len(out[i: i + hop]):]
    shape = (t / d) ** 2.2
    shape[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))
    return (tonal + out) * shape


def impact(d=0.8):
    t = t_axis(d)
    f = 50 + 85 * np.exp(-t / 0.06)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.25) + 0.35 * filt(
        rng.standard_normal(len(t)), "lowpass", 4500) * env(len(t), 0.001, 0.07)


def chime(d=1.1):
    out = np.zeros(int(d * SR))
    for f, off in ((784, 0.0), (988, 0.08), (1319, 0.16)):
        s = tone(f, 0.9, 0.22)
        o = int(off * SR)
        out[o: o + len(s)] += s[: len(out) - o]
    return out


def done():  # final checkmark
    return tone(1175, 0.4, 0.12) + 0.7 * tone(1760, 0.4, 0.09, harm=(1.0,))


def bed(d=DUR, bpm=112):
    """Minimal electronic groove: soft kick, offbeat hats, sub, filtered plucks (Am-F-C-G)."""
    beat, n = 60 / bpm, int(d * SR)
    mix = np.zeros(n)
    prog = [(110.0, [440.0, 523.25, 659.25]), (87.31, [349.23, 440.0, 523.25]),
            (130.81, [523.25, 659.25, 783.99]), (98.0, [392.0, 493.88, 587.33])]

    def add(s, at):
        o = int(at * SR)
        if o < n:
            m = min(len(s), n - o)
            mix[o: o + m] += s[:m]

    for bar in range(int(d / (beat * 4)) + 1):
        root, ch = prog[bar % 4]
        t0 = bar * beat * 4
        for k in range(4):
            kt = t_axis(0.25)
            kf = 48 + 70 * np.exp(-kt / 0.03)
            add(np.sin(2 * np.pi * np.cumsum(kf) / SR) * env(len(kt), 0.001, 0.08) * 0.5, t0 + k * beat)
            ht = t_axis(0.04)
            add(filt(rng.standard_normal(len(ht)), "highpass", 8000) * env(len(ht), 0.0004, 0.01) * 0.12,
                t0 + k * beat + beat / 2)
        bt = t_axis(beat * 3.8)
        add((np.sin(2 * np.pi * root * bt) * 0.45) * np.minimum(1, bt / 0.02) * np.exp(-bt / 1.6), t0)
        for k in range(8):
            f = ch[[0, 2, 1, 2, 0, 2, 1, 2][k]]
            pt = t_axis(0.22)
            saw = 2 * ((f * pt) % 1) - 1
            add(filt(saw, "lowpass", 2200) * env(len(pt), 0.002, 0.06) * 0.08, t0 + k * beat / 2)
    mix *= np.minimum(1, np.arange(n) / (0.4 * SR))
    mix[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))
    return mix


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save("tick.wav", tick(), 0.6)
    save("click.wav", click(), 0.7)
    save("pop.wav", pop(), 0.8)
    save("whoosh.wav", whoosh(), 0.7)
    save("riser.wav", riser(), 0.8)
    save("impact.wav", impact(), 0.95)
    save("chime.wav", chime(), 0.85)
    save("done.wav", done(), 0.8)
    save("_bed_raw.wav", bed(), 0.9)
    raw, voice = os.path.join(OUT, "_bed_raw.wav"), os.path.join(OUT, "voice.wav")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-i", voice, "-filter_complex",
                        "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=10:attack=8:release=300:makeup=1[d];"
                        "[d]loudnorm=I=-28:TP=-4:LRA=7[b]", "-map", "[b]", "-ar", "48000", "-ac", "2",
                        os.path.join(OUT, "bed.wav")], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])
    os.remove(raw)
    print("wrote", sorted(f for f in os.listdir(OUT) if f.endswith(".wav")))
