"""Offline, deterministic 30s Apple-style bed (120 BPM) + a few SFX for the iPhone Duo reel.
Run: python3 scripts/synth_music.py  -> assets/audio/*.wav
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import sfx_lib as L

SR = L.SR
L.OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "audio")
BEAT = 0.5  # 120 BPM
TOTAL = 30.5

def pluck(f, dur=0.35):
    n = int(dur * SR); t = L.t_axis(dur)
    x = np.sin(2*np.pi*f*t) + 0.4*np.sin(2*np.pi*2*f*t) + 0.15*np.sin(2*np.pi*3*f*t)
    return x * L.env_ad(n, 0.003, 0.12)

def pad(freqs, dur):
    t = L.t_axis(dur); x = np.zeros(len(t))
    for f in freqs:
        for d in (-0.35, 0.0, 0.35):
            x += np.sin(2*np.pi*(f+d)*t)
    x = L.filt(x, "lowpass", 1800)
    fade = np.minimum(1, np.minimum(t/0.8, (dur-t)/0.8))
    return x * np.clip(fade, 0, 1)

def clap(dur=0.18):
    n = int(dur*SR); noise = L.rng.standard_normal(n)
    x = L.filt(noise, "bandpass", [900, 5000]) * L.env_ad(n, 0.001, 0.05)
    return x

def hat(dur=0.05):
    n = int(dur*SR)
    return L.filt(L.rng.standard_normal(n), "highpass", 8000) * L.env_ad(n, 0.0005, 0.012)

def build():
    n = int(TOTAL*SR); x = np.zeros(n)
    # sections: intro 0-3 (pad + ticks), build 3-7, main 7-26 (full), outro 26-30 (pad + final hit)
    chords = [[110, 164.8, 220, 329.6], [98, 146.8, 196, 293.7], [130.8, 196, 261.6, 329.6], [87.3, 130.8, 174.6, 261.6]]
    for i, t0 in enumerate(np.arange(0, 30, 4.0)):
        L.place(x, pad(chords[i % 4], 4.2) * 0.07, t0)
    arp = [440, 523.3, 659.3, 880, 659.3, 523.3, 440, 392]
    for k in range(int(30/0.25)):
        t = k*0.25
        if 3 <= t < 26:
            L.place(x, pluck(arp[k % 8]) * 0.10, t)
    for b in range(int(30/BEAT)):
        t = b*BEAT
        if 7 <= t < 26:
            L.place(x, L.kick(0.4, heavy=False) * 0.55, t)
            if b % 2 == 1: L.place(x, clap() * 0.35, t)
            L.place(x, hat() * 0.25, t + BEAT/2)
        elif 3 <= t < 7:
            L.place(x, hat() * 0.2, t + BEAT/2)
            if b % 2 == 0: L.place(x, L.kick(0.4, heavy=False) * 0.35, t)
    # final hit
    L.place(x, L.kick(0.8) * 0.8, 26.0)
    L.place(x, pad([55, 110, 164.8, 220], 4.5) * 0.12, 26.0)
    # fade out the last 0.8s
    t = np.arange(n)/SR
    x *= np.clip((30.2 - t)/0.8, 0, 1)
    return L.filt(x, "highpass", 30)

if __name__ == "__main__":
    os.makedirs(L.OUT, exist_ok=True)
    L.save("music.wav", build(), 0.85)
    L.save("whoosh.wav", L.whoosh(0.6), 0.6)
    L.save("impact.wav", L.kick(0.9), 0.9)
    L.save("riser.wav", L.riser(2.0), 0.55)
    L.save("tick.wav", L.click(0.05, 3000), 0.4)
    L.save("shimmer.wav", L.chime(1.8), 0.4)
    print(sorted(os.listdir(L.OUT)))
