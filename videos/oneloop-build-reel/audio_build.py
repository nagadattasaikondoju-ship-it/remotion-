# Sound: dialogue track from the cleaned takes + two music beds composed in code (no downloadable CC0 music was reachable).
#   /usr/bin/python3 -P audio_build.py  ->  out/dialogue.wav, out/music.wav (48 kHz stereo, full reel length)
# Music map (Tarun's notes): playful plucks under the sketch -> tape-stop on the freeze -> calm documentary piano + pad under
# the explanation, a soft pulse under the three proofs, silence for the slam, a resolving chord for the logo and the CTA hold.
import json, os, numpy as np, soundfile as sf
from scipy.signal import lfilter
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000
TL = json.load(open(os.path.join(HERE, "out", "timeline.json")))
CLEAN = os.environ.get("CLEAN_DIR", "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/build/clean")
DUR = TL["duration"]; N = int(round(DUR * SR))
seg = {s["id"]: s for s in TL["segments"]}; S = lambda i: seg[i]["start"]; E = lambda i: seg[i]["start"] + seg[i]["dur"]

def lufs_gain(x, target):  # simple speech-gated RMS match (K-weighting is close enough between takes of one voice)
    b = 4800; fr = np.array([np.sqrt(np.mean(x[i:i + b] ** 2)) for i in range(0, len(x) - b, b)]); fr = fr[fr > fr.max() * 0.1]
    lvl = 20 * np.log10(np.sqrt(np.mean(fr ** 2)) + 1e-9); return 10 ** ((target - lvl) / 20)

def dialogue():
    out = np.zeros(N); cache = {}
    for a in TL["audio"]:
        if a["src"] not in cache:
            x, sr = sf.read(os.path.join(CLEAN, a["src"] + ".wav")); assert sr == SR
            cache[a["src"]] = x * lufs_gain(x, -20.0)
        x = cache[a["src"]][int(a["in"] * SR):int(a["out"] * SR)].copy(); f = int(0.012 * SR)
        x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
        i = int(round(a["start"] * SR)); x = x[:max(0, N - i)]; out[i:i + len(x)] += x
    return np.stack([out, out], 1)

# ---------- instruments ----------
def midi(n): return 440 * 2 ** ((n - 69) / 12)
def pluck(f, dur, bright=0.5, seed=0):  # Karplus-Strong plucked string (pizzicato-ish)
    n = int(dur * SR); p = max(2, int(SR / f)); rng = np.random.default_rng(seed)
    buf = rng.uniform(-1, 1, p); y = np.zeros(n); d = 0.5 * (0.985 + 0.013 * bright)   # averaging filter, loss < 1 (stable)
    for i in range(n):
        y[i] = buf[i % p]; buf[i % p] = d * (buf[i % p] + buf[(i + 1) % p])
    return y * np.exp(-np.arange(n) / SR * 2.5)
def piano(f, dur, vel=0.6):  # soft additive piano: inharmonic partials, fast attack, two-stage decay
    t = np.arange(int(dur * SR)) / SR; y = np.zeros_like(t)
    for k, a in enumerate([1, 0.45, 0.22, 0.12, 0.06, 0.03], 1):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k); y += a * np.sin(2 * np.pi * fk * t) * np.exp(-t * (0.9 + 0.7 * k))
    env = np.minimum(1, t / 0.006) * (0.7 * np.exp(-t * 2.2) + 0.3 * np.exp(-t * 0.5)); return y * env * vel
def pad(freqs, dur, attack=1.2, release=1.5):  # warm detuned-saw pad, low-passed
    t = np.arange(int(dur * SR)) / SR; y = np.zeros_like(t)
    for f in freqs:
        for d in (-0.12, 0, 0.11):
            ph = (f * 2 ** (d / 12) * t) % 1; y += (2 * ph - 1) * 0.25
    a = np.minimum(1, t / attack) * np.minimum(1, (dur - t) / release); y *= a
    k = np.exp(-2 * np.pi * 900 / SR); z = lfilter([1 - k], [1, -k], y)   # one-pole low-pass
    return z / max(1, len(freqs))
def kick(dur=0.35, vel=0.8):
    t = np.arange(int(dur * SR)) / SR; f = 45 + 90 * np.exp(-t * 30); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9) * vel
def tick(vel=0.25, seed=1):
    rng = np.random.default_rng(seed); n = int(0.05 * SR); x = rng.normal(0, 1, n) * np.exp(-np.arange(n) / SR * 90)
    return np.diff(np.concatenate([[0], x])) * vel
def add(buf, x, at, gain=1.0, pan=0.0):
    i = int(at * SR); x = x[:max(0, len(buf) - i)]
    if i < 0 or not len(x): return
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4); buf[i:i + len(x), 0] += x * gain * l * 1.41; buf[i:i + len(x), 1] += x * gain * r * 1.41

def music():
    m = np.zeros((N, 2))
    # --- playful sketch bed: 116 BPM, C major, bouncy pizzicato bass + staccato motif, from the sketch's first line to the freeze
    t0, t1, bpm = S("a1"), S("frz"), 116; beat = 60 / bpm
    bass = [36, 43, 41, 43, 36, 43, 38, 43]; motif = [72, None, 76, 79, 77, None, 74, 76, 72, None, 79, 77, 76, 74, 72, None]
    k = 0; t = t0
    while t < t1 - 0.05:
        add(m, pluck(midi(bass[k % 8] + 12), 0.5, 0.3, k), t, 0.55, -0.2)
        nn = motif[(2 * k) % 16]; nn2 = motif[(2 * k + 1) % 16]
        if nn: add(m, pluck(midi(nn), 0.3, 0.75, 100 + k), t, 0.30, 0.35)
        if nn2: add(m, pluck(midi(nn2), 0.3, 0.75, 200 + k), t + beat / 2, 0.26, 0.35)
        add(m, tick(0.10, k), t + beat / 2, 1.0, 0.1); k += 1; t += beat
    # tape-stop on the freeze: the last 0.45 s of the bed slows to a halt (the classic "record stop")
    i0, i1 = int((t1 - 0.45) * SR), int(t1 * SR); seg_ = m[i0:i1].copy(); n = len(seg_)
    pos = np.cumsum(np.linspace(1, 0, n)); pos = pos / pos[-1] * (n - 1)
    for c in range(2): m[i0:i1, c] = np.interp(pos, np.arange(n), seg_[:, c]) * np.linspace(1, 0.2, n)
    m[i1:int((t1 + 0.6) * SR)] = 0
    # --- documentary bed: 72 BPM, A minor (Am F C G), piano arpeggio + pad, from Tarun's first word to the slam
    d0, d1, bpm2 = S("frz") + 0.6, S("t7b"), 72; b2 = 60 / bpm2
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    bar = 0; t = d0
    while t < d1:
        ch = chords[bar % 4]; L = min(4 * b2, d1 - t)
        add(m, pad([midi(n - 12) for n in ch], L + 0.6, 0.8, 0.8), t, 0.16)
        add(m, piano(midi(ch[0] - 12), 3.0, 0.5), t, 0.55, -0.15)
        for j, n in enumerate([0, 1, 2, 1, 2, 1, 0, 1]):  # eighth-note arpeggio
            tt = t + j * b2 / 2
            if tt < d1 - 0.1: add(m, piano(midi(ch[n] + 12), 1.6, 0.32 + 0.06 * (j == 0)), tt, 0.5, 0.25)
        bar += 1; t += 4 * b2
    # soft pulse under the proofs (one kick per beat, locked to the first proof's cut)
    p0, p1 = S("t4b"), E("t6"); t = p0
    while t < p1 - 0.05: add(m, kick(0.35, 0.55), t, 0.9); t += b2
    # the slam: music drops out (SFX carry it); the logo lands on a resolving C major chord that rings into the CTA
    m[int(d1 * SR):int(S("t9") * SR)] *= 0
    lg = S("t9") + 0.68
    add(m, pad([midi(n) for n in (48, 55, 64, 67)], DUR - lg, 0.4, 1.2), lg, 0.22)
    for j, n in enumerate([60, 64, 67, 72]): add(m, piano(midi(n), 4.0, 0.45), lg + j * 0.11, 0.6, -0.2 + 0.13 * j)
    m[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))[:, None] ** 2
    return m / (np.abs(m).max() + 1e-9) * 0.7

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    sf.write(os.path.join(HERE, "out", "dialogue.wav"), dialogue(), SR, subtype="PCM_24")
    sf.write(os.path.join(HERE, "out", "music.wav"), music(), SR, subtype="PCM_24")
    print("out/dialogue.wav, out/music.wav", f"{DUR:.2f}s")
