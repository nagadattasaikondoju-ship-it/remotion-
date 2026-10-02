"""Offline, deterministic synthesis of the music bed and SFX for the reel.

Run: python3 scripts/synth_audio.py  (writes assets/audio/*.wav at 48 kHz)
"""
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
OUT = "."
rng = np.random.default_rng(7)


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def filt(x, kind, freq, order=4):
    sos = butter(order, freq, btype=kind, fs=SR, output="sos")
    return sosfilt(sos, x)


def env_ad(n, attack, decay_tau):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-np.maximum(t - attack, 0) / decay_tau)


def sweep(f0, f1, dur, curve="exp"):
    t = t_axis(dur)
    if curve == "exp":
        f = f0 * (f1 / f0) ** (t / dur)
    else:
        f = f0 + (f1 - f0) * (t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def norm(x, peak=0.89):
    m = np.max(np.abs(x)) or 1.0
    return x / m * peak


def save(name, x, peak=0.89):
    x = norm(x, peak)
    st = np.stack([x, x], axis=1).astype(np.float32)
    wavfile.write(os.path.join(OUT, name), SR, st)


# ---------- SFX ----------
def sub_drop(dur=1.4):
    x = sweep(110, 32, dur) * env_ad(int(dur * SR), 0.004, 0.45)
    return np.tanh(2.2 * x)


def vhs_tap(dur=0.35):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    crackle = noise * (rng.random(n) > 0.6)
    buzz = np.sign(np.sin(2 * np.pi * 60 * t_axis(dur))) * 0.3
    x = filt(crackle + buzz, "bandpass", [900, 7000]) * env_ad(n, 0.002, 0.08)
    # stutter gate
    gate = (np.floor(t_axis(dur) * 40) % 2 == 0).astype(float)
    return x * (0.4 + 0.6 * gate)


def whoosh(dur=0.55, up=True, lo=400, hi=6000):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    t = t_axis(dur)
    out = np.zeros(n)
    steps = 24
    for i in range(steps):
        s, e = i * n // steps, (i + 1) * n // steps
        p = i / (steps - 1)
        fc = lo * (hi / lo) ** (p if up else 1 - p)
        seg = filt(noise, "bandpass", [fc * 0.6, min(fc * 1.6, 20000)], order=2)[s:e]
        out[s:e] = seg
    shape = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.6
    return out * shape


def click(dur=0.06, f=2400):
    n = int(dur * SR)
    x = np.sin(2 * np.pi * f * t_axis(dur)) * env_ad(n, 0.0005, 0.008)
    x += filt(rng.standard_normal(n), "highpass", 3000) * env_ad(n, 0.0002, 0.003) * 0.6
    return x


def pop(dur=0.14):
    n = int(dur * SR)
    return sweep(900, 260, dur) * env_ad(n, 0.001, 0.035) + click(dur, 3200) * 0.3


def rising_ticks(dur=1.1):
    n = int(dur * SR)
    x = np.zeros(n)
    t = 0.0
    gap = 0.14
    k = 0
    while t < dur - 0.05:
        c = click(0.05, 1800 + 140 * k)
        i = int(t * SR)
        x[i:i + len(c)] += c[: n - i]
        t += gap
        gap = max(gap * 0.84, 0.035)
        k += 1
    return x


def down_slide(dur=0.9):
    n = int(dur * SR)
    s = sweep(880, 110, dur)
    s = np.tanh(3 * s) * 0.5 + 0.5 * s
    return filt(s, "lowpass", 3000) * env_ad(n, 0.01, 0.5)


def chime(dur=1.6):
    n = int(dur * SR)
    t = t_axis(dur)
    x = np.zeros(n)
    for i, f in enumerate([784, 988, 1175, 1568]):
        d = int(i * 0.07 * SR)
        tone = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)) * env_ad(n, 0.002, 0.45)
        x[d:] += tone[: n - d] * (0.9 - i * 0.12)
    return x


def tape_stop(dur=0.7):
    n = int(dur * SR)
    t = t_axis(dur)
    f = 220 * (1 - t / dur) ** 2 + 20
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    x = filt(saw, "lowpass", 1400) * (1 - t / dur) ** 0.5
    return x


def glitch(dur=0.4):
    n = int(dur * SR)
    t = t_axis(dur)
    sq = np.sign(np.sin(2 * np.pi * 180 * t)) * 0.5
    bits = np.round(rng.standard_normal(n) * 3) / 3
    gate = (np.floor(t * 55) % 3 != 0).astype(float)
    return (sq + filt(bits, "highpass", 1500)) * gate * env_ad(n, 0.001, 0.15)


def kick(dur=0.6, heavy=True):
    n = int(dur * SR)
    x = sweep(160 if heavy else 120, 42, 0.12)
    x = np.concatenate([x, np.sin(2 * np.pi * 42 * t_axis(dur - 0.12))])
    x = np.tanh(3.0 * x[:n]) * env_ad(n, 0.001, 0.22 if heavy else 0.12)
    x += filt(rng.standard_normal(n), "highpass", 2500) * env_ad(n, 0.0002, 0.006) * 0.5
    return x


def riser(dur=1.4):
    n = int(dur * SR)
    t = t_axis(dur)
    noise = whoosh(dur, up=True, lo=300, hi=9000)
    tone = sweep(120, 900, dur) * 0.4
    return (noise + tone) * (t / dur) ** 2


def swipe_down(dur=0.35):
    return whoosh(dur, up=False, lo=500, hi=9000)


# ---------- MUSIC BED ----------
def music_bed(total=36.0, bpm=120):
    n = int(total * SR)
    t = t_axis(total)
    beat = 60 / bpm
    x = np.zeros(n)
    # drone pad: detuned low saws, heavily low-passed
    pad = np.zeros(n)
    for f in (55.0, 55.4, 82.4, 110.2):
        pad += 2 * ((f * t) % 1) - 1
    pad = filt(pad, "lowpass", 380) * 0.10
    x += pad
    # bass pulse on every beat, hats on off-8ths from bar 3
    for i in range(int(total / beat)):
        s = int(i * beat * SR)
        k = kick(0.45, heavy=False) * (0.55 if i % 2 else 0.8)
        seg = min(len(k), n - s)
        x[s:s + seg] += k[:seg]
        if i * beat >= 4.0:
            h_s = int((i * beat + beat / 2) * SR)
            hn = int(0.04 * SR)
            if h_s + hn < n:
                x[h_s:h_s + hn] += filt(rng.standard_normal(hn), "highpass", 7000) * env_ad(hn, 0.0005, 0.012) * 0.35
    # sidechain-ish pump on the pad from the kick pattern
    pump = 0.65 + 0.35 * ((t % beat) / beat) ** 0.5
    x = x * pump
    return filt(x, "highpass", 28)


def place(buf, clip, at):
    s = int(at * SR)
    e = min(len(buf), s + len(clip))
    if e > s:
        buf[s:e] += clip[: e - s]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save("sub-drop.wav", sub_drop())
    save("vhs-tap.wav", vhs_tap(), 0.6)
    save("whoosh.wav", whoosh(), 0.7)
    save("paper-swoosh.wav", filt(whoosh(0.5, lo=1500, hi=9000), "highpass", 1200), 0.55)
    save("ui-click.wav", click(), 0.6)
    save("ui-pop.wav", pop(), 0.6)
    save("rising-ticks.wav", rising_ticks(), 0.55)
    save("down-slide.wav", down_slide(), 0.6)
    save("chime.wav", chime(), 0.55)
    save("tape-stop.wav", tape_stop(), 0.7)
    save("glitch.wav", glitch(), 0.5)
    save("kick-hit.wav", kick(), 0.95)
    save("riser.wav", riser(), 0.6)
    save("swipe-down.wav", swipe_down(), 0.7)
    save("music-bed.wav", music_bed(), 0.8)
    print("wrote", sorted(os.listdir(OUT)))
