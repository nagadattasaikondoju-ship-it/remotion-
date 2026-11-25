"""Offline, deterministic bed + SFX for the BRIDL360 key reel (14 s). Run: python3 scripts/synth_audio.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import sfx_lib as L
SR = L.SR
L.OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio")
TOTAL = 14.0
def note(m): return 440.0 * 2 ** ((m - 69) / 12)

def felt(f, dur=2.2, vel=1.0):
    """soft felt-piano-ish tone: a few decaying partials, muted attack"""
    n = int(dur * SR); t = L.t_axis(dur)
    x = np.zeros(n)
    for k, a, tau in ((1, 1.0, 0.9), (2, 0.35, 0.5), (3, 0.12, 0.3), (4, 0.05, 0.2)):
        x += a * np.sin(2 * np.pi * f * k * t + 0.3 * k) * np.exp(-t / tau)
    x *= L.env_ad(n, 0.012, 10.0)
    return L.filt(x, "lowpass", 2600) * vel

def pad(freqs, dur, lp=1400):
    t = L.t_axis(dur); x = np.zeros(len(t))
    for f in freqs:
        for d in (-0.6, 0.0, 0.55):
            x += np.sin(2 * np.pi * (f + d) * t + d)
    x = L.filt(x, "lowpass", lp)
    fade = np.clip(np.minimum(t / 1.2, (dur - t) / 1.2), 0, 1)
    return x * fade

def bed():
    buf = np.zeros(int((TOTAL + 1) * SR))
    # chord per section: Dmaj9 (key) -> Bm11 / Gmaj7 (city) -> D/A lift (end card)
    secs = [(0.0, 2.7, [50, 57, 62, 64, 66, 69]), (2.7, 6.0, [47, 54, 59, 62, 66, 69]),
            (6.0, 9.25, [43, 50, 55, 59, 62, 66]), (9.25, 14.0, [45, 52, 57, 62, 64, 69])]
    for s, e, ch in secs:
        L.place(buf, 0.10 * pad([note(m) for m in ch[:3]], e - s + 1.2), max(0, s - 0.3))
        # gentle arpeggio, 8th notes at 84 bpm
        step = 60 / 84 / 2
        k = 0; t = s
        while t < e - 0.05:
            m = ch[[0, 2, 4, 3, 5, 3, 4, 2][k % 8]] + 12
            L.place(buf, 0.16 * felt(note(m), 1.8, 0.75 + 0.25 * (k % 2 == 0)), t)
            t += step; k += 1
    # low root swell under the reveal
    L.place(buf, 0.18 * pad([note(38)], 4.0, lp=300), 2.4)
    buf = buf[: int(TOTAL * SR)]
    t = L.t_axis(TOTAL)
    buf *= np.clip(np.minimum(t / 0.25, (TOTAL - t) / 1.4), 0, 1)
    return L.filt(buf, "highpass", 40)

def key_lock():
    """two-stage metal latch: tiny scrape then a solid click with a short ring"""
    a = L.click(0.05, 3100) * 0.5
    n = int(0.35 * SR); t = L.t_axis(0.35)
    ring = (np.sin(2*np.pi*2350*t) + 0.6*np.sin(2*np.pi*3720*t) + 0.3*np.sin(2*np.pi*5210*t)) * np.exp(-t / 0.05)
    body = L.filt(L.rng.standard_normal(n), "bandpass", [600, 4000]) * L.env_ad(n, 0.0008, 0.012)
    b = 0.6 * ring * 0.4 + body
    out = np.zeros(int(0.45 * SR)); L.place(out, a, 0.0); L.place(out, b, 0.07)
    return out

def tick():
    n = int(0.12 * SR); t = L.t_axis(0.12)
    return np.sin(2*np.pi*1800*t) * np.exp(-t / 0.012) + 0.3 * L.filt(L.rng.standard_normal(n), "highpass", 4000) * np.exp(-t / 0.006)

L.save("bed.wav", bed(), 0.6)
L.save("key-lock.wav", key_lock(), 0.85)
L.save("riser.wav", L.filt(L.riser(1.0), "lowpass", 7000), 0.5)
L.save("whoosh-in.wav", L.whoosh(0.6, up=True, lo=300, hi=5000), 0.7)
L.save("whoosh-out.wav", L.whoosh(0.7, up=False, lo=250, hi=4500), 0.6)
L.save("tick.wav", tick(), 0.5)
L.save("impact.wav", L.filt(L.kick(0.9, heavy=False), "lowpass", 900), 0.75)
print("ok")
