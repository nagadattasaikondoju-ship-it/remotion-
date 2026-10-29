# Sound pass for the story reel: synthesised SFX on the cue sheet below + VO (+ optional music bed) → out/mix_raw.wav,
# with one stem per family in out/stems/ (whooshes, textures, risers, hits, vo, music) for a manual finish in the mixer.
# The Ultimate Editors library isn't in the repo yet, so every SFX here is synthesised (fallback; swap per cue later).
#   python3 sfx.py                    → VO + SFX
#   MUSIC=track.mp3 MUSIC_IN=12.0 python3 sfx.py → + music bed from 12.0 s into the track, ducked under the VO
import os, json, subprocess, numpy as np
from scipy.signal import stft, istft, fftconvolve
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
SR, DUR = 48000, 38.0
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

# ---------- sound designs (each returns (mono signal, sample index of its hit / peak)) ----------
def whoosh(d=0.55, peak=0.62, lo=250, hi=3800):
    env = lambda u: np.where(u < peak, (u / peak) ** 2.2, np.exp(-(u - peak) / (1 - peak) * 4))
    fc = lambda u: lo + (hi - lo) * np.where(u < peak, (u / peak) ** 1.6, 1 - 0.55 * (u - peak) / (1 - peak))
    x = shaped_noise(d, fc, lambda u: 0.35 * fc(u) + 150, env)
    return fade(norm(x), 0.005, 0.03), int(SR * d * peak)
def pop():
    t = tt(0.09); f = 380 + 700 * np.exp(-t / 0.012); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.028)
    x[:96] += rng.standard_normal(96) * 0.5 * np.linspace(1, 0, 96)
    return fade(norm(x)), 0
def tick(f=3600):
    t = tt(0.03); x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.004); return fade(norm(x), 0.0005), 0
def ui_click():
    t = tt(0.05); x = np.sin(2 * np.pi * 2300 * t) * np.exp(-t / 0.007) + 0.6 * np.sin(2 * np.pi * 1150 * t) * np.exp(-t / 0.012)
    x[:144] += rng.standard_normal(144) * 0.6 * np.linspace(1, 0, 144); return fade(norm(x), 0.0005), 0
def scifi_click():
    t = tt(0.12); f = 900 + 1800 * (1 - np.exp(-t / 0.02)); ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.35 * np.exp(-t / 0.02) + np.sin(ph * 1.5) * np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.04)
    return fade(verb(norm(x), 0.4, 0.18)), 0
def camera_click():
    x = np.zeros(int(SR * 0.16))
    for o, a in ((0, 1.0), (0.055, 0.7)):
        i = int(SR * o); b = rng.standard_normal(240) * np.exp(-np.arange(240) / 50) * a; x[i:i + 240] += b
        t = tt(0.025); x[i:i + len(t)] += 0.5 * a * np.sin(2 * np.pi * 160 * t) * np.exp(-t / 0.006)
    x = np.diff(x, prepend=0) * 0.6 + x * 0.4; return fade(norm(x), 0.0002), 0
def droplet():
    t = tt(0.14); f = 650 + 1500 * (1 - np.exp(-t / 0.025)); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035)
    return fade(verb(norm(x), 0.5, 0.25)), 0
def scifi_impact():
    t = tt(1.0); body = np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-t / 0.05)) / SR) * np.exp(-t / 0.22)
    metal = sum(np.sin(2 * np.pi * f * t + i) * np.exp(-t / dd) for i, (f, dd) in enumerate([(523, 0.35), (1371, 0.25), (2207, 0.18), (3301, 0.12)])) * 0.25
    crack = shaped_noise(1.0, lambda u: 2500 + 0 * u, lambda u: 2000 + 0 * u, lambda u: np.exp(-u * 40))
    return fade(verb(norm(body + metal + 0.5 * norm(crack)), 0.9, 0.25), 0.0005, 0.1), 0
def hit():
    t = tt(1.6); boom = np.sin(2 * np.pi * np.cumsum(30 + 85 * np.exp(-t / 0.06)) / SR) * np.exp(-t / 0.45)
    crack = shaped_noise(1.6, lambda u: 900 + 0 * u, lambda u: 1400 + 0 * u, lambda u: np.exp(-u * 30))
    return fade(verb(norm(boom + 0.35 * norm(crack)), 1.2, 0.2), 0.0005, 0.2), 0
def riser_bass(d):
    t = tt(d); u = t / d; f = 42 * (180 / 42) ** (u ** 1.4); ph = 2 * np.pi * np.cumsum(f) / SR
    tone = (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)) * u ** 2.2
    air = shaped_noise(d, lambda u: 400 + 5000 * u ** 1.8, lambda u: 300 + 1500 * u, lambda u: u ** 3)
    x = norm(tone) + 0.45 * norm(air); return fade(norm(x), 0.05, 0.004), len(x)
def riser_metal(d):
    t = tt(d); u = t / d; base = 220 * 4 ** (u ** 1.5); x = np.zeros_like(t)
    for r, a in ((1, 1), (2.76, 0.6), (5.4, 0.4), (8.93, 0.25)): x += a * np.sin(2 * np.pi * np.cumsum(base * r) / SR)
    x *= (0.6 + 0.4 * np.sin(2 * np.pi * np.cumsum(4 + 26 * u ** 2) / SR)) * u ** 2.5
    shim = shaped_noise(d, lambda u: 6000 + 3000 * u, lambda u: 1800 + 0 * u, lambda u: u ** 3)
    return fade(norm(verb(norm(x) + 0.3 * norm(shim), 0.6, 0.15)), 0.05, 0.004), len(t)
def shimmer():
    x = shaped_noise(0.7, lambda u: 5000 + 5000 * u, lambda u: 2500 + 0 * u, lambda u: np.sin(np.pi * u) ** 2)
    return fade(norm(x), 0.01, 0.05), int(SR * 0.35)
def pad(d):  # ambient bed: soft A-minor chord + air, slow swell (stands in for music in the no-VO proof beat)
    t = tt(d); x = np.zeros_like(t)
    for f, a in ((55, 0.9), (110, 0.7), (164.81, 0.45), (220, 0.35), (261.63, 0.3), (329.63, 0.22)):
        for det in (-0.6, 0.6): x += a * np.sin(2 * np.pi * (f + det) * t + rng.uniform(0, 6)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.7 * t + f))
    air = shaped_noise(d, lambda u: 1800 + 0 * u, lambda u: 1200 + 0 * u, lambda u: 0 * u + 1)
    x = norm(x) + 0.12 * norm(air); env = np.clip(t / 0.35, 0, 1) * np.clip((d - t) / 0.45, 0, 1)
    return norm(x * env), 0
def chime():
    x = np.zeros(int(SR * 1.6)); t = tt(1.4)
    for k, f in enumerate((1046.5, 1318.5, 1568.0)):
        s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / dd) for r, a, dd in ((1, 1, 0.6), (2.0, 0.35, 0.3), (3.0, 0.15, 0.15)))
        i = int(SR * 0.07 * k); x[i:i + len(t)] += s
    return fade(verb(norm(x), 1.0, 0.3), 0.001, 0.2), 0

# ---------- cue sheet (video time of the visual event = the sound's hit / peak point) ----------
FOOT_CUTS = [1.60, 3.20, 3.87, 4.64, 5.55, 6.85, 8.10, 9.50, 11.60, 12.75, 14.10, 15.75, 16.75, 17.40, 20.55, 21.30, 22.00, 23.30, 34.10]
CUES = []  # (family, time, design, level dBFS peak, pan −1…1 or None for auto-sweep, note)
for i, c in enumerate(FOOT_CUTS):
    CUES.append(("whooshes", c, ("whoosh", 0.42, 0.6, 400, 4200), -24, None, "short whoosh on the xfade, peak on the cut"))
for c, note in [(18.62, "footage dissolves into the logo"), (19.55, "logo punches out into the team"), (24.98, "circle reveal into the photo pile"),
                (28.44, "client wall pushes up"), (30.45, "analytics push in from the right"), (31.45, "second screenshot slides in"),
                (32.32, "analytics slide up off the footage"), (36.30, "into the end card")]:
    CUES.append(("whooshes", c, ("whoosh", 0.7, 0.62, 200, 3200), -16, None, note))
CUES.append(("whooshes", 11.20, ("whoosh", 0.3, 0.5, 900, 6000), -20, None, "copper strike across TRAFFIC PROBLEM"))
TEX = [(0.21, "pop", -15, "WE MADE"), (1.97, "pop", -14, "IN 2 MONTHS"), (10.79, "pop", -15, "TRAFFIC"), (10.99, "pop", -15, "PROBLEM"),
       (11.83, "pop", -15, "THEY HAVE"), (12.40, "droplet", -15, "the copper full stop drips"),
       (13.63, "scifi_click", -14, "AUDIT."), (15.83, "scifi_click", -14, "BUILD."), (16.85, "scifi_click", -14, "MARKET."), (17.77, "scifi_click", -14, "AUTOMATE."),
       (19.81, "ui_click", -15, "01 DEVELOPERS"), (20.59, "ui_click", -15, "02 DESIGNERS"), (21.43, "ui_click", -15, "03 MARKETERS"), (22.39, "ui_click", -15, "04 AI BUILDERS"),
       (23.45, "pop", -14, "ONE TEAM."), (24.23, "pop", -14, "ONE LOOP."), (25.71, "pop", -15, "BRANDS"),
       (26.47, "pop", -16, "HYDERABAD chip"), (27.35, "pop", -16, "DUBAI chip"), (27.89, "pop", -16, "AUSTRALIA chip"),
       (28.62, "pop", -12, "SUCCESSFUL CLIENTS"), (29.55, "shimmer", -18, "copper light sweep over the wall"),
       (30.67, "scifi_impact", -11, "8.43 tile lights up"), (31.67, "scifi_impact", -12, "6,406 tile lights up"),
       (32.62, "pop", -15, "WE'RE JUST"), (33.02, "pop", -14, "GETTING"), (33.26, "pop", -14, "STARTED."), (34.22, "pop", -15, "COME GROW WITH US"),
       (35.00, "scifi_impact", -13, "@ONELOOP.IN"), (36.62, "chime", -13, "logo snaps on the end card (success reward)")]
for t0, d, lv, note in TEX: CUES.append(("textures", t0, (d,), lv, 0.0, note))
for j in range(8): CUES.append(("textures", 24.85 + j * 0.45 + 0.06, ("camera_click",), -17, 0.0, f"photo card {j + 1} lands"))
for t0 in sorted({round(28.62 + k * 0.055, 3) for k in range(9)}): CUES.append(("textures", t0, ("ui_click",), -19, 0.0, "logo cards pop (one per diagonal)"))
for a, b, n_, note in [(1.05, 1.75, 12, "₹95,000 counter"), (24.75, 25.45, 10, "25+ counter"), (28.45, 29.05, 10, "21+ counter"),
                        (30.50, 31.05, 9, "8.43× counter"), (31.50, 32.05, 9, "6,406 counter")]:
    for k in range(n_): CUES.append(("textures", a + (b - a) * (1 - (1 - k / n_) ** 2), ("tick",), -24, 0.0, note))
RIS = [(9.85, 12.15, "riser_bass", -13, "sharp bass riser into A LEAK"), (17.80, 18.93, "riser_metal", -14, "metallic riser into the logo snap"),
       (27.00, 28.45, "riser_bass", -12, "sharp bass riser into the client wall"), (35.25, 36.62, "riser_metal", -14, "metallic riser into the end card")]
for a, b, d, lv, note in RIS: CUES.append(("risers", b, (d, b - a), lv, 0.0, note))
for t0, lv, note in [(1.05, -9, "₹95,000 lands (hook impact)"), (12.15, -10, "A LEAK"), (18.93, -9, "the X snaps into the logo"),
                     (28.45, -8, "client wall lands"), (36.62, -10, "end-card logo")]:
    CUES.append(("hits", t0, ("hit",), lv, 0.0, note))

if not os.environ.get("MUSIC"):
    CUES.append(("beds", 28.20, ("pad", 4.45), -13, 0.0, "ambient bed under the no-VO proof beat (replaced by the music bed)"))
DESIGNS = dict(pad=pad, whoosh=whoosh, pop=pop, tick=tick, ui_click=ui_click, scifi_click=scifi_click, camera_click=camera_click, droplet=droplet,
               scifi_impact=scifi_impact, hit=hit, riser_bass=riser_bass, riser_metal=riser_metal, shimmer=shimmer, chime=chime)
FAM = ["beds", "whooshes", "textures", "risers", "hits"]
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
# music bed: ~16 dB under the voice, ducked a further 6 dB while the VO talks, lifted in the no-VO proof beat (28.45–32.45)
music = os.environ.get("MUSIC")
if music:
    m = read(music, 2)[int(float(os.environ.get("MUSIC_IN", "0")) * SR):][:N]; m = np.pad(m, ((0, N - len(m)), (0, 0)))
    rms = lambda s: np.sqrt(np.mean(s ** 2) + 1e-12)
    voiced = np.abs(vo) > 0.02; g0 = rms(vo[voiced]) / rms(m) * db(-16)
    env = np.convolve(np.abs(vo), np.ones(int(SR * 0.05)) / (SR * 0.05), "same") > 0.01
    k = np.exp(-1 / (SR * 0.25)); duck = np.zeros(N); s = 0.0
    for i in range(0, N, 480):  # 10 ms control rate: fast attack, 250 ms release
        tgt = 1.0 if env[i:i + 480].any() else 0.0; s = tgt if tgt > s else s * k ** 480; duck[i:i + 480] = s
    gain = g0 * db(-6 * duck) * (1 + (db(6) - 1) * np.clip(np.minimum((np.arange(N) / SR - 28.3) / 0.3, (32.6 - np.arange(N) / SR) / 0.3), 0, 1))
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
