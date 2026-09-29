"""Offline, deterministic SFX for the listicle (48 kHz stereo WAVs in assets/audio).

Run: python3 scripts/synth_sfx.py
"""
import os

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio")
rng = np.random.default_rng(11)


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def filt(x, kind, freq, order=4):
    return sosfilt(butter(order, freq, btype=kind, fs=SR, output="sos"), x)


def env(n, attack, tau):
    t = np.arange(n) / SR
    return np.clip(t / max(attack, 1e-4), 0, 1) * np.exp(-np.maximum(t - attack, 0) / tau)


def save(name, x, peak=0.89):
    x = x / (np.max(np.abs(x)) or 1.0) * peak
    fade = min(len(x), int(0.004 * SR))
    x[-fade:] *= np.linspace(1, 0, fade)
    wavfile.write(os.path.join(OUT, name), SR, np.stack([x, x], axis=1).astype(np.float32))


def pop(dur=0.14):
    """Crisp bubble pop: fast pitch drop + tiny bright transient."""
    t = t_axis(dur)
    f = 380 + 620 * np.exp(-t / 0.018)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.0015, 0.035)
    click = filt(rng.standard_normal(len(t)), "bandpass", [3000, 9000]) * env(len(t), 0.0003, 0.003)
    return body + 0.35 * click


def tick(dur=0.05):
    t = t_axis(dur)
    tone = np.sin(2 * np.pi * 2600 * t) * env(len(t), 0.0005, 0.009)
    grit = filt(rng.standard_normal(len(t)), "highpass", 4000) * env(len(t), 0.0002, 0.002)
    return tone + 0.4 * grit


def swish(dur=0.22):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    hop = 480
    for i in range(0, n, hop):  # sweep a band-pass upward in short blocks
        c = 1400 * (5200 / 1400) ** (i / n)
        blk = filt(noise[max(0, i - 960): i + hop], "bandpass", [c * 0.7, c * 1.3], order=2)
        out[i: i + hop] = blk[-len(out[i: i + hop]):]
    shape = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return out * shape


def click(dur=0.04):
    t = t_axis(dur)
    return (
        filt(rng.standard_normal(len(t)), "highpass", 2500) * env(len(t), 0.0002, 0.0025)
        + 0.6 * np.sin(2 * np.pi * 1800 * t) * env(len(t), 0.0005, 0.006)
    )


def chime(dur=1.2):
    t = t_axis(dur)
    x = np.zeros_like(t)
    for f, a, tau in [(1318.5, 1.0, 0.45), (1975.5, 0.6, 0.35), (2637, 0.25, 0.2), (659.3, 0.3, 0.6)]:
        x += a * np.sin(2 * np.pi * f * t) * env(len(t), 0.002, tau)
    return x * (1 + 0.04 * np.sin(2 * np.pi * 6 * t))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save("pop.wav", pop())
    save("tick.wav", tick(), 0.7)
    save("swish.wav", swish(), 0.7)
    save("click.wav", click(), 0.8)
    save("chime.wav", chime(), 0.8)
    print("wrote", sorted(f for f in os.listdir(OUT) if f.endswith(".wav")))
