# Sound pass for the story reel: six synthesised SFX on the cue sheet below + VO (+ optional music bed) → out/mix_raw.wav,
# with one stem per family in out/stems/ (whooshes, textures, risers, hits, vo, music) for a manual finish in the mixer.
# The Ultimate Editors library isn't in the repo yet, so every SFX here is synthesised (fallback; swap per cue later).
#   python3 sfx.py                    → VO + SFX
#   MUSIC=track.mp3 MUSIC_IN=12.0 python3 sfx.py → + music bed from 12.0 s into the track, ducked under the VO
import os, json, subprocess, numpy as np
from scipy.signal import stft, istft, fftconvolve
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
SR, DUR = 48000, 34.5
N = int(SR * DUR)
rng = np.random.default_rng(7)
db = lambda x: 10 ** (x / 20)
tt = lambda d: np.arange(int(SR * d)) / SR

def norm(x): return x / (np.max(np.abs(x)) + 1e-9)
def shaped_noise(d, fc, bw, env):
    """noise through a moving gaussian band: fc(u), bw(u), env(u) are functions of u ∈ [0, 1] over the sound"""
    n = rng.standard_normal(int(SR * d) + 1024); f, t, Z = stft(n, SR, nperseg=1024)
    u = np.clip(t / d, 0, 1); F = f[:, None]
    Z *= np.exp(-0.5 * ((F - fc(u)[None]) / bw(u)[None]) ** 2) * env(u)[None]
    return istft(Z, SR, nperseg=1024)[1][: int(SR * d)]
def verb(x, d=0.7, mix=0.22):
    ir = rng.standard_normal(int(SR * d)) * np.exp(-tt(d) / (d / 5)); ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - mix) + mix * fftconvolve(x, ir)[: len(x)]
def fade(x, a=0.002, b=0.01):
    x = x.copy(); na, nb = int(SR * a), int(SR * b)
    if na: x[:na] *= np.linspace(0, 1, na)
    if nb: x[-nb:] *= np.linspace(1, 0, nb)
    return x

# ---------- minimal set: warm, low, no high-frequency clicks (they read as cheap next to a voice) ----------
def impact(weight=1.0):
    """deep cinematic impact: soft-attack sub drop + low body thump + a short dark room"""
    t = tt(1.8); sub = np.sin(2 * np.pi * np.cumsum(36 + 30 * np.exp(-t / 0.08)) / SR) * np.exp(-t / (0.55 * weight))
    body = shaped_noise(1.8, lambda u: 160 + 0 * u, lambda u: 90 + 0 * u, lambda u: np.exp(-u * 1.8 / 0.07))
    x = norm(sub) + 0.35 * norm(body); x[: int(SR * 0.004)] *= np.linspace(0, 1, int(SR * 0.004))
    return fade(verb(norm(x), 1.4, 0.18), 0.0005, 0.3), 0
def soft_impact():
    """subtle proof hit: short airy lift into a light low thump"""
    lift = shaped_noise(0.30, lambda u: 700 + 1500 * u, lambda u: 500 + 0 * u, lambda u: u ** 3) * 0.25
    t = tt(0.9); thump = np.sin(2 * np.pi * np.cumsum(55 + 40 * np.exp(-t / 0.04)) / SR) * np.exp(-t / 0.18)
    x = np.concatenate([lift, np.zeros(len(thump))]); x[len(lift):] += norm(thump)
    return fade(verb(norm(x), 0.8, 0.15), 0.01, 0.2), len(lift)
def swell(d=0.9):
    """reverse-style swell that ends on its hit point"""
    x = shaped_noise(d, lambda u: 250 + 1400 * u ** 2, lambda u: 200 + 600 * u, lambda u: u ** 2.5)
    t = tt(d); x = norm(x) + 0.3 * np.sin(2 * np.pi * 55 * t) * (t / d) ** 3
    return fade(norm(x), 0.05, 0.01), len(t)
def soft_riser(d):
    x = shaped_noise(d, lambda u: 300 + 3500 * u ** 1.6, lambda u: 250 + 900 * u, lambda u: u ** 2.8)
    t = tt(d); x = norm(x) + 0.35 * np.sin(2 * np.pi * np.cumsum(50 + 70 * (t / d) ** 2) / SR) * (t / d) ** 2
    return fade(norm(x), 0.08, 0.01), len(t)
def sting():
    """end-card sting: warm low hit + a soft major chord that blooms and decays"""
    t = tt(2.2); x = np.zeros_like(t)
    for f, a in ((130.81, 0.8), (196.0, 0.6), (261.63, 0.5), (329.63, 0.35), (392.0, 0.3), (587.33, 0.18)):
        x += a * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t / 0.9) * (1 - np.exp(-t / 0.015))
    h, _ = impact(0.7); n = min(len(h), len(x)); x[:n] += 1.2 * norm(h[:n]) * np.max(np.abs(x))
    return fade(verb(norm(x), 1.6, 0.3), 0.001, 0.4), 0

# ---------- cue sheet (video time of the visual event = the sound's hit point) ----------
# Six sounds in the whole reel, each on a moment that matters; the voice carries everything else (music when supplied).
CUES = [  # (family, time, design, level dBFS peak, pan, note)
    ("hits", 1.05, ("impact",), -11, 0.0, "₹95,000 lands (hook impact)"),
    ("textures", 17.00, ("soft_impact",), -17, 0.0, "8.43× return on ad spend appears"),
    ("risers", 18.93, ("soft_riser", 0.9), -19, 0.0, "soft riser into the logo snap"),
    ("hits", 18.93, ("soft_impact",), -15, 0.0, "the X snaps into the One Loop logo"),
    ("whooshes", 24.75, ("swell", 0.9), -18, 0.0, "swell into 21+ brands / logo wall"),
    ("textures", 28.47, ("soft_impact",), -17, 0.0, "6,406 conversions appears"),
    ("hits", 33.05, ("sting",), -14, 0.0, "end-card logo sting"),
]

DESIGNS = dict(impact=impact, soft_impact=soft_impact, swell=swell, soft_riser=soft_riser, sting=sting)
FAM = ["whooshes", "textures", "risers", "hits"]
stems = {f: np.zeros((N, 2)) for f in FAM}
cache = {}
for fam, t0, spec, lv, pan, note in CUES:
    if spec not in cache: cache[spec] = DESIGNS[spec[0]](*spec[1:])
    x, hp = cache[spec]; x = x * db(lv); i0 = int(round(t0 * SR)) - hp
    if pan is None:  # whoosh travels across the stereo field, centre on its peak
        p = np.clip((np.arange(len(x)) - hp) / (len(x) * 0.6), -0.7, 0.7)
    else: p = np.full(len(x), pan)
    L, R = x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)
    a, b = max(0, i0), min(N, i0 + len(x)); stems[fam][a:b, 0] += L[a - i0:b - i0]; stems[fam][a:b, 1] += R[a - i0:b - i0]

def read(path, ch):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).astype(np.float64)
vo = read(os.path.join(OUT, "vo_raw.wav"), 1)[:N, 0]; vo = np.pad(vo, (0, N - len(vo)))
stems["vo"] = np.stack([vo, vo], 1) * db(-3)  # mono VO, equal-power centre
# music bed: ~16 dB under the voice, ducked a further 6 dB while the VO talks
music = os.environ.get("MUSIC")
if music:
    m = read(music, 2)[int(float(os.environ.get("MUSIC_IN", "0")) * SR):][:N]; m = np.pad(m, ((0, N - len(m)), (0, 0)))
    rms = lambda s: np.sqrt(np.mean(s ** 2) + 1e-12)
    voiced = np.abs(vo) > 0.02; g0 = rms(vo[voiced]) / rms(m) * db(-16)
    env = np.convolve(np.abs(vo), np.ones(int(SR * 0.05)) / (SR * 0.05), "same") > 0.01
    k = np.exp(-1 / (SR * 0.25)); duck = np.zeros(N); s = 0.0
    for i in range(0, N, 480):  # 10 ms control rate: fast attack, 250 ms release
        tgt = 1.0 if env[i:i + 480].any() else 0.0; s = tgt if tgt > s else s * k ** 480; duck[i:i + 480] = s
    gain = g0 * db(-6 * duck)
    gain *= np.clip((DUR - np.arange(N) / SR) / 1.2, 0, 1) * np.clip(np.arange(N) / SR / 0.15, 0, 1)
    stems["music"] = m * gain[:, None]
mix = sum(stems.values())
os.makedirs(os.path.join(OUT, "stems"), exist_ok=True)
def write(path, x):
    pcm = (np.clip(x, -1, 1) * 8388607).astype(np.int32)
    b = np.stack([(pcm >> s) & 0xFF for s in (0, 8, 16)], -1).astype(np.uint8).reshape(-1)
    p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s24le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", path], input=b.tobytes())
for k, v in stems.items(): write(os.path.join(OUT, "stems", f"{k}.wav"), v)
write(os.path.join(OUT, "mix_raw.wav"), mix)
print(f"{len(CUES)} cues · stems: {', '.join(stems)} · mix peak {20 * np.log10(np.max(np.abs(mix))):.1f} dBFS")
# cue sheet for the hand-off
with open(os.path.join(OUT, "CUES.md"), "w") as f:
    f.write("| Time | Track | Sound | Level (dBFS peak) | Moment |\n|---|---|---|---|---|\n")
    for fam, t0, spec, lv, pan, note in sorted(CUES, key=lambda c: c[1]):
        if spec[0] == "tick" and "counter" in note and abs(t0 - min(c[1] for c in CUES if c[5] == note)) > 1e-6: continue
        f.write(f"| {int(t0 // 60):02d}:{t0 % 60:05.2f} | {fam} | {spec[0]}{'' if len(spec) == 1 else ' ' + str(round(spec[1], 2)) + ' s'} | {lv} | {note} |\n")
