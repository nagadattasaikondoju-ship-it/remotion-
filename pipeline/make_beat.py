"""Synthesise a royalty-free placeholder beat (100 BPM, A minor: Am-F-C-G).

Everything is generated from sine/noise so there are no licensing questions.
Swap in a real track by pointing `music.src` in src/short/config.ts at it.
Usage: python3 pipeline/make_beat.py public/media/music.wav [--seconds 48]
"""
import argparse

import numpy as np
import soundfile as sf

SR = 44100
BPM = 100
BEAT = 60 / BPM
rng = np.random.default_rng(7)


def env(n, attack, decay):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)


def lowpass(x, cutoff):
    # one-pole low-pass, good enough for taming pads/noise
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def kick():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    freq = 45 + 110 * np.exp(-t * 28)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    return np.sin(phase) * env(n, 0.002, 0.16) * 0.9


def clap():
    n = int(0.25 * SR)
    noise = rng.standard_normal(n)
    bp = noise - lowpass(noise, 900)       # crude high-pass
    bp = lowpass(bp, 5000)
    e = env(n, 0.001, 0.06)
    for d in (0.012, 0.024):               # the "clap" flutter
        k = int(d * SR)
        e[k:] += env(n - k, 0.001, 0.05) * 0.6
    return bp * e * 0.35


def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    noise = rng.standard_normal(n)
    hp = noise - lowpass(noise, 7000)
    return hp * env(n, 0.001, 0.07 if open_ else 0.015) * 0.18


def note(freq, dur, kind="bass"):
    n = int(dur * SR)
    t = np.arange(n) / SR
    if kind == "bass":
        x = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
        return x * env(n, 0.005, dur * 0.6) * 0.35
    # pad: three slightly detuned saws, filtered, slow attack
    x = sum(2 * ((f * t) % 1) - 1 for f in (freq * 0.997, freq, freq * 1.004)) / 3
    x = lowpass(x, 1400)
    a = np.clip(t / 0.4, 0, 1) * np.clip((dur - t) / 0.5, 0, 1)
    return x * a * 0.07


def hz(midi):
    return 440 * 2 ** ((midi - 69) / 12)


CHORDS = [  # (bass root, pad triad) in MIDI
    (45, (57, 60, 64)),  # Am
    (41, (57, 60, 65)),  # F
    (48, (55, 60, 64)),  # C
    (43, (55, 59, 62)),  # G
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float, default=48)
    a = ap.parse_args()

    total = int(a.seconds * SR)
    mix = np.zeros(total + SR)

    def put(sample, at):
        i = int(at * SR)
        if i < total:
            j = min(len(mix), i + len(sample))
            mix[i:j] += sample[: j - i]

    K, C, H, HO = kick(), clap(), hat(), hat(True)
    bar = 4 * BEAT
    bars = int(np.ceil(a.seconds / bar))
    for b in range(bars):
        t0 = b * bar
        root, triad = CHORDS[b % 4]
        for m in triad:
            put(note(hz(m), bar, "pad"), t0)
        for beat, length in ((0, 1.5), (1.5, 0.5), (2, 1.5), (3.5, 0.5)):
            put(note(hz(root), length * BEAT, "bass"), t0 + beat * BEAT)
        for k in (0, 2, 2.75):
            put(K, t0 + k * BEAT)
        for c in (1, 3):
            put(C, t0 + c * BEAT)
        for e in range(8):
            swing = 0.03 if e % 2 else 0
            put(HO if e == 7 else H, t0 + e * BEAT / 2 + swing)

    mix = mix[:total]
    fade = int(0.02 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)  # gentle glue/limiter
    mix *= 0.89 / np.max(np.abs(mix))
    stereo = np.stack([mix, np.roll(mix, int(0.004 * SR))], axis=1)  # a little width
    sf.write(a.out, stereo.astype(np.float32), SR)
    print(f"wrote {a.seconds:.0f}s beat -> {a.out}")


if __name__ == "__main__":
    main()
