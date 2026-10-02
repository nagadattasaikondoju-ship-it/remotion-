"""Offline, deterministic SFX + music bed (48 kHz stereo WAVs in assets/audio).

Run: python3 scripts/synth_sfx.py   (needs assets/audio/voice.wav first for the ducked bed)
"""
import os
import subprocess

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "audio")
rng = np.random.default_rng(7)


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def filt(x, kind, freq, order=4):
    return sosfilt(butter(order, freq, btype=kind, fs=SR, output="sos"), x)


def env(n, attack, tau):
    t = np.arange(n) / SR
    return np.clip(t / max(attack, 1e-4), 0, 1) * np.exp(-np.maximum(t - attack, 0) / tau)


def save(name, x, peak=0.89, stereo=True):
    x = x / (np.max(np.abs(x)) or 1.0) * peak
    fade = min(len(x), int(0.004 * SR))
    x[-fade:] *= np.linspace(1, 0, fade)
    data = np.stack([x, x], axis=1) if stereo else x
    wavfile.write(os.path.join(OUT, name), SR, data.astype(np.float32))


def impact(dur=0.9):
    """Pattern-interrupt hit: sub drop + noise burst + a bright tick."""
    t = t_axis(dur)
    f = 48 + 90 * np.exp(-t / 0.07)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.28)
    burst = filt(rng.standard_normal(len(t)), "lowpass", 5000) * env(len(t), 0.001, 0.09)
    tick = filt(rng.standard_normal(len(t)), "highpass", 3500) * env(len(t), 0.0003, 0.012)
    return sub + 0.5 * burst + 0.25 * tick


def whoosh(dur=0.45, up=True):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    hop = 480
    for i in range(0, n, hop):
        p = i / n
        c = 500 * (6000 / 500) ** (p if up else 1 - p)
        blk = filt(noise[max(0, i - 960): i + hop], "bandpass", [c * 0.6, c * 1.4], order=2)
        out[i: i + hop] = blk[-len(out[i: i + hop]):]
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5


def pop(dur=0.14):
    t = t_axis(dur)
    f = 380 + 620 * np.exp(-t / 0.018)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.0015, 0.035)
    click = filt(rng.standard_normal(len(t)), "bandpass", [3000, 9000]) * env(len(t), 0.0003, 0.003)
    return body + 0.35 * click


def tick(dur=0.05):
    t = t_axis(dur)
    return np.sin(2 * np.pi * 2600 * t) * env(len(t), 0.0005, 0.009) + 0.4 * filt(
        rng.standard_normal(len(t)), "highpass", 4000) * env(len(t), 0.0002, 0.002)


def tone(freq, dur, tau, attack=0.003, harm=(1.0, 0.35, 0.12)):
    t = t_axis(dur)
    x = sum(a * np.sin(2 * np.pi * freq * (k + 1) * t) for k, a in enumerate(harm))
    return x * env(len(t), attack, tau)


def ding(dur=0.5):
    """Success ding for the checklist: bright two-partial bell."""
    return tone(1568, dur, 0.16) + 0.6 * tone(2349, dur, 0.1, harm=(1.0,))


def missed(dur=0.7):
    """Sad descending 'missed call' beeps."""
    out = np.zeros(int(dur * SR))
    for i, (f, off) in enumerate(((620, 0.0), (520, 0.17), (415, 0.34))):
        seg = tone(f, 0.22, 0.09, harm=(1.0, 0.2))
        o = int(off * SR)
        out[o: o + len(seg)] += seg
    return out


def chime(dur=1.1):
    """CTA: rising 3-note arpeggio with a soft tail."""
    out = np.zeros(int(dur * SR))
    for f, off in ((784, 0.0), (988, 0.09), (1319, 0.18)):
        seg = tone(f, 0.9, 0.22, harm=(1.0, 0.3))
        o = int(off * SR)
        out[o: o + len(seg)] += seg[: len(out) - o]
    return out


def tock(dur=0.09):
    t = t_axis(dur)
    return np.sin(2 * np.pi * 900 * t) * env(len(t), 0.0008, 0.012) + 0.3 * filt(
        rng.standard_normal(len(t)), "bandpass", [1500, 4000]) * env(len(t), 0.0003, 0.004)


# ---------------------------------------------------------------- music bed
def music(dur=21.0667, bpm=104):
    """Warm minimal groove (Am-F-C-G): soft kick, hats, sub bass, pad and a plucky arp."""
    beat = 60 / bpm
    n = int(dur * SR)
    mix = np.zeros(n)
    prog = [(220.0, [220.0, 261.63, 329.63]), (174.61, [174.61, 220.0, 261.63]),
            (261.63, [261.63, 329.63, 392.0]), (196.0, [196.0, 246.94, 293.66])]

    def add(sig, at):
        o = int(at * SR)
        if o < n:
            m = min(len(sig), n - o)
            mix[o: o + m] += sig[:m]

    bars = int(dur / (beat * 4)) + 1
    for bar in range(bars):
        root, chord = prog[bar % 4]
        t0 = bar * beat * 4
        # pad
        pt = t_axis(beat * 4)
        pad = sum(np.sin(2 * np.pi * f * pt) + 0.4 * np.sin(2 * np.pi * f * 2.003 * pt) for f in chord)
        pad = filt(pad, "lowpass", 1800) * np.minimum(1, pt / 0.4) * np.minimum(1, (beat * 4 - pt) / 0.3) * 0.16
        add(pad, t0)
        # sub bass on 1 and the "and" of 2
        for off, ln in ((0, beat * 1.4), (beat * 2.5, beat * 1.2)):
            bt = t_axis(ln)
            b = (np.sin(2 * np.pi * root / 2 * bt) + 0.3 * np.sin(2 * np.pi * root * bt)) * env(len(bt), 0.01, 0.35)
            add(b * 0.5, t0 + off)
        # kick on every beat (soft), hats on the off-beats
        for k in range(4):
            kt = t_axis(0.28)
            kf = 46 + 80 * np.exp(-kt / 0.035)
            kick = np.sin(2 * np.pi * np.cumsum(kf) / SR) * env(len(kt), 0.001, 0.09)
            add(kick * 0.55, t0 + k * beat)
            ht = t_axis(0.05)
            hat = filt(rng.standard_normal(len(ht)), "highpass", 7000) * env(len(ht), 0.0005, 0.012)
            add(hat * 0.16, t0 + k * beat + beat / 2)
        # 8th-note arp pluck
        for k in range(8):
            f = chord[[0, 1, 2, 1, 2, 1, 2, 1][k]] * 2
            add(tone(f, 0.3, 0.07, harm=(1.0, 0.25)) * 0.07, t0 + k * beat / 2)
    mix *= np.minimum(1, np.arange(n) / (0.15 * SR))
    mix[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))
    return mix


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save("impact.wav", impact(), 0.95)
    save("whoosh.wav", whoosh(0.4, True), 0.75)
    save("whoosh-down.wav", whoosh(0.35, False), 0.7)
    save("pop.wav", pop(), 0.89)
    save("tick.wav", tick(), 0.7)
    save("ding.wav", ding(), 0.8)
    save("missed.wav", missed(), 0.8)
    save("chime.wav", chime(), 0.85)
    save("tock.wav", tock(), 0.7)
    m = music()
    save("_music_raw.wav", m, 0.9)
    voice = os.path.join(OUT, "voice.wav")
    raw = os.path.join(OUT, "_music_raw.wav")
    # duck the bed under the voice (sidechain), then sit it ~-24 LUFS under the -14 LUFS voice
    r = subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-i", voice, "-filter_complex",
        "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=9:attack=8:release=260:makeup=1[d];"
        "[d]loudnorm=I=-27:TP=-3:LRA=7[bed]",
        "-map", "[bed]", "-ar", "48000", "-ac", "2", os.path.join(OUT, "bed.wav")], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])
    os.remove(raw)
    print("wrote", sorted(f for f in os.listdir(OUT) if f.endswith(".wav")))
