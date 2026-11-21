# The score: a sunny ukulele groove composed in code for this reel (no licensed or downloaded music; it belongs to One Loop).
#   /usr/bin/python3 -P music.py -> out/music.wav (48 kHz stereo, reel length)
# 115 BPM, C major, I-V-vi-IV, light swing. One bar per shot, so every cut lands on a downbeat:
#   bar 1  handshake      ukulele + shaker
#   bar 2  meet the team  + bass + snaps
#   3-8    the roles      + kick, glockenspiel hook (layers staggered a bar apart: no startle)
#   9-10   the burst      + whistle doubling the hook, claps on the last beats
#   11     make them famous  drums drop out, F then G under the One Loop site
#   12     end card       lands on C: one strum, a glockenspiel sparkle, rings out
import json, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve
HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, "out", "edit.json"))); SR = 48000
BEAT, BAR, DUR = E["beat"], E["bar"], E["duration"]; N = int((DUR + 2.5) * SR)
L, R = np.zeros(N), np.zeros(N); rng = np.random.default_rng(7)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
SW = 0.57   # swing: the off-beat 8th sits at 57 % of the beat
def at8(bar, k): return bar * BAR + (k // 2) * BEAT + (k % 2) * SW * BEAT   # 8th-note k (0..7) of a bar, swung

def put(x, t, g=1.0, pan=0.0):
    i = int(t * SR); x = x[: max(0, N - i)]
    L[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 - pan)); R[i:i + len(x)] += x * g * np.sqrt(0.5 * (1 + pan))

def pluck(f, dur=1.4, bright=0.62, seed=0):   # Karplus-Strong nylon string (ukulele)
    n = int(dur * SR); p = max(2, int(SR / f)); r = np.random.default_rng(seed)
    buf = r.uniform(-1, 1, p); buf = np.convolve(buf, [0.5, 0.5], "same"); out = np.empty(n); k = 0
    for i in range(n):
        out[i] = buf[k]; nk = (k + 1) % p; buf[k] = 0.996 * (bright * buf[k] + (1 - bright) * buf[nk]); k = nk
    return out * np.exp(-np.arange(n) / SR * 1.6)

_pl = {}
def string(m, seed):
    key = (m, seed % 3)
    if key not in _pl: _pl[key] = pluck(hz(m), seed=seed % 3)
    return _pl[key]

UKE = {"C": [67, 60, 64, 72], "G": [67, 62, 67, 71], "Am": [69, 60, 64, 69], "F": [69, 60, 65, 69]}
ROOT = {"C": 36, "G": 43, "Am": 45, "F": 41}
def strum(ch, t, down=True, v=1.0, seed=0):
    notes = UKE[ch] if down else UKE[ch][::-1]
    for j, m in enumerate(notes): put(string(m, seed + j), t + j * 0.011, 0.24 * v * (1 if down else 0.7), -0.18)

def bass(m, t, dur):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m)
    x = 0.8 * np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt) + 0.08 * np.sin(6 * np.pi * f * tt)
    env = np.minimum(1, tt / 0.008) * np.exp(-tt * 2.2) * np.minimum(1, (dur - tt) / 0.04).clip(0)
    put(x * env, t, 0.30)

def kick(t, v=1.0):
    n = int(0.32 * SR); tt = np.arange(n) / SR; ph = 2 * np.pi * np.cumsum(48 + 70 * np.exp(-tt * 30)) / SR
    put(np.sin(ph) * np.exp(-tt * 11), t, 0.42 * v)

def noise_hit(t, lo, hi, dur, g, pan=0.0, decay=30):
    n = int(dur * SR); x = rng.uniform(-1, 1, n); x = sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
    put(x * np.exp(-np.arange(n) / SR * decay), t, g, pan)

def snap(t, v=1.0): noise_hit(t, 1800, 5200, 0.12, 0.22 * v, 0.1, 45); noise_hit(t + 0.009, 1400, 3200, 0.1, 0.12 * v, -0.1, 40)
def clap(t, v=1.0):
    for d in (0, 0.011, 0.022): noise_hit(t + d, 900, 4000, 0.16, 0.16 * v, 0.0, 28)
def shaker(t, v=1.0): noise_hit(t, 6000, 14000, 0.07, 0.07 * v, 0.35, 60)

def glock(m, t, v=1.0, dur=1.6):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 2.6) + 0.35 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 9) \
        + 0.12 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt * 18)
    put(x * np.minimum(1, tt / 0.002), t, 0.10 * v, 0.22)

def whistle(m, t, dur, v=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m) * (1 + 0.006 * np.sin(2 * np.pi * 5.6 * tt) * np.minimum(1, tt / 0.15))
    ph = 2 * np.pi * np.cumsum(f) / SR; breath = sosfilt(butter(2, [hz(m) * 0.9, hz(m) * 1.1], "band", fs=SR, output="sos"), rng.uniform(-1, 1, n))
    env = np.minimum(1, tt / 0.04) * np.minimum(1, np.clip(dur - tt, 0, None) / 0.06)
    put((np.sin(ph) + 0.15 * breath) * env, t, 0.075 * v, 0.0)

# chords per bar (bar 11 splits F | G, bar 12 lands on C)
CH = ["C", "G", "Am", "F", "C", "G", "Am", "F", "C", "G", None, "C"]
# glockenspiel hook: 4 bars, (8th index, MIDI)
HOOK = [[(0, 76), (2, 79), (3, 81), (4, 79), (6, 76)],
        [(0, 74), (2, 74), (3, 76), (4, 74), (6, 71)],
        [(0, 72), (2, 76), (3, 79), (4, 81), (6, 79)],
        [(0, 77), (2, 76), (3, 74), (4, 72), (5, 74), (6, 76)]]
ISLAND = [(0, True), (2, True), (3, False), (5, False), (6, True), (7, False)]   # D . D U . U D U

for b in range(12):
    t0 = b * BAR
    if b == 10:   # "now let's make them famous": F then G, no drums, a shaker swell into the end card
        for k, ch in ((0, "F"), (4, "G")):
            strum(ch, at8(b, k), True, 0.9, seed=b * 9 + k); strum(ch, at8(b, k + 2), True, 0.7, seed=b * 9 + k + 2); strum(ch, at8(b, k + 3), False, 0.7, seed=b * 9 + k + 3)
            bass(ROOT[ch], at8(b, k), 2 * BEAT * 0.95)
        for k in range(8): shaker(at8(b, k), 0.4 + 0.12 * k)
        glock(81, at8(b, 0), 0.6); glock(79, at8(b, 4), 0.6); glock(83, at8(b, 7), 0.5)
        continue
    if b == 11:   # the end card: land on C and let it ring
        strum("C", t0, True, 1.1, seed=99); bass(36, t0, BAR * 0.98); kick(t0, 0.6)
        for j, m in enumerate((72, 76, 79, 84)): glock(m, t0 + 0.09 * j + 0.05, 0.9, 2.4)
        strum("C", at8(b, 4), True, 0.55, seed=98)
        continue
    ch = CH[b]
    for k, down in ISLAND: strum(ch, at8(b, k), down, 1.0, seed=b * 8 + k)
    for k in range(8): shaker(at8(b, k), (0.8 if b == 0 else 1.0) * (1.0 if k % 2 == 0 else 0.7))
    if b == 0: bass(ROOT[ch], t0, 1.5 * BEAT); bass(ROOT[ch] + 7, t0 + 2 * BEAT, 1.0 * BEAT)   # a soft bass already under the hook (no +10 dB jump at bar 2)
    if b >= 1:   # bass: root on 1, fifth-ish on 3, a pickup 8th into the next bar
        bass(ROOT[ch], t0, 1.5 * BEAT); bass(ROOT[ch] + 7, t0 + 2 * BEAT, 1.0 * BEAT); bass(ROOT[ch] + 12, at8(b, 7), 0.45 * BEAT)
        snap(t0 + BEAT, 0.9); snap(t0 + 3 * BEAT, 0.9)
    if b >= 2:   # kick enters a bar after the bass
        kick(t0); kick(t0 + 2 * BEAT, 0.8)
        if b >= 8: kick(t0 + BEAT, 0.6); kick(t0 + 3 * BEAT, 0.6)   # the burst: four on the floor
    if b >= 3:   # glockenspiel hook enters a bar after the kick
        for k, m in HOOK[(b - 3) % 4]: glock(m, at8(b, k), 1.0)
    if b >= 8:   # the burst: a whistle doubles the hook an octave down
        notes = HOOK[(b - 3) % 4]
        for (k, m), nxt in zip(notes, notes[1:] + [(8, None)]):
            whistle(m - 12, at8(b, k), max(0.12, at8(b, nxt[0]) - at8(b, k) - 0.03) if nxt[0] < 8 else BEAT * 0.9)
    if b == 9:
        for k in (5, 6, 7): clap(at8(b, k), 0.8)

# room + gentle glue, then trim to the reel with a short tail fade
ir_n = int(0.9 * SR); ir = rng.uniform(-1, 1, ir_n) * np.exp(-np.arange(ir_n) / SR * 6.5); ir /= np.sqrt((ir ** 2).sum())
wetL, wetR = fftconvolve(L, ir)[:N], fftconvolve(R, ir[::-1])[:N]
mix = np.stack([L + 0.16 * wetL, R + 0.16 * wetR], 1)
mix = np.tanh(mix * 1.6) / 1.6
n = int(DUR * SR); mix = mix[:n]; fade = int(0.35 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
mix *= 0.89 / np.abs(mix).max()
sf.write(os.path.join(HERE, "out", "music.wav"), mix.astype(np.float32), SR, subtype="FLOAT")
print(f"out/music.wav: {n / SR:.2f} s")
