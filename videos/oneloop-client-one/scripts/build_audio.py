"""Dialogue restoration + edit, clean ambience beds, natural B-roll sound, designed SFX + flash-cut SFX
→ assets/audio/master.wav (48 kHz stereo, −14.5 LUFS integrated, ≤ −1 dBTP).

Run: python3 scripts/build_audio.py
- Dialogue: DeepFilterNet3 at full suppression (the WhatsApp phone take replaces the noisy 0658 camera audio).
- Tarun's two phone recordings are tonally matched to Prahalad's camera-mic voice (long-term spectrum match,
  1/3-octave, ±6 dB, 70 %), then everyone shares one gentle chain and one loudness target.
- Under the dialogue: a very quiet synthesized outdoor bed per location (air / distant traffic / night insects),
  constant-power crossfaded at each location cut and ducked under speech, so cuts never drop into dead silence.
- No music bed: the post gets a quiet Instagram sound later.
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy.signal import butter, sosfilt, welch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import (AMBIENCE, BROLL, CLEAN, FLASHCUTS, FPS, MATCH_PAGES, OVER, SEGS, START, LEN, TOTAL, VOICE, WHIP_CUT,  # noqa
                 T)

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "assets", "audio")
TMP = os.path.join(OUT, "_tmp")
os.makedirs(TMP, exist_ok=True)
SR = 48000
N = int(round(TOTAL * SR))
rng = np.random.default_rng(7)
CLEANED = {"0647": "0647_dn.wav", "AUD": "AUD_dn.wav", "0662": "0662_dn.wav", "VID": "VID_dn.wav"}


def load(path, ss=None, dur=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss}"] if ss is not None else []) + (
        ["-t", f"{dur}"] if dur is not None else []) + ["-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()


def save(path, x, stereo=True):
    x = np.atleast_2d(x)
    if stereo and x.shape[0] == 1:
        x = np.vstack([x, x])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(x.shape[0]), "-i", "-",
                    "-c:a", "pcm_s24le", path], input=x.T.astype(np.float32).tobytes(), check=True)


def lufs(x):
    """integrated loudness of a mono signal (measured as mono, i.e. one channel)"""
    p = os.path.join(TMP, "_m.wav")
    save(p, x, stereo=False)
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(r.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])


def ffx(x, af):
    a, b = os.path.join(TMP, "_a.wav"), os.path.join(TMP, "_b.wav")
    save(a, x, stereo=False)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", af, "-ar", str(SR), b], check=True)
    y = load(b)
    return np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)]


def fade(x, ms_in=20, ms_out=20):
    a, b = int(ms_in * SR / 1000), int(ms_out * SR / 1000)
    x[:a] *= np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    x[-b:] *= np.cos(np.linspace(0, np.pi / 2, b)) ** 2
    return x


def filt(x, kind, f, order=4):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output="sos"), x)


def env(n, a, tau):
    t = np.arange(n) / SR
    return np.clip(t / max(a, 1e-4), 0, 1) * np.exp(-np.maximum(t - a, 0) / tau)


def place(buf, x, t, gain_db):
    i = int(round(t * SR))
    x = x[: max(0, min(len(x), len(buf) - i))]
    buf[i:i + len(x)] += x * 10 ** (gain_db / 20)


# ================= dialogue =================
tracks = {k: load(os.path.join(CLEAN, f)) for k, f in CLEANED.items()}
segs = []
for i, (src, a, b, _, _) in enumerate(SEGS):
    n = LEN[i] * SR // FPS
    segs.append(tracks[src][int(a * SR):int(a * SR) + n].copy())

# per-group loudness, then long-term-spectrum match to Prahalad's camera-mic voice
groups = sorted(set(VOICE))
gx = {g: np.concatenate([segs[i] for i in range(len(SEGS)) if VOICE[i] == g]) for g in groups}
gain = {g: -20.0 - lufs(gx[g]) for g in groups}


def ltas(x):
    h = 2048
    m = len(x) // h
    fr = x[:m * h].reshape(m, h)
    speech = fr[20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9) > -38].ravel()
    f, p = welch(speech, SR, nperseg=4096)
    return f, 10 * np.log10(p + 1e-14)


bands = [100 * 2 ** (k / 3) for k in range(0, 21)]  # 100 Hz … 10 kHz, 1/3 octave
f_ref, p_ref = ltas(gx["P_cam"] * 10 ** (gain["P_cam"] / 20))
match = {}
for g in groups:
    if g == "P_cam":
        continue
    f, p = ltas(gx[g] * 10 ** (gain[g] / 20))
    # broad tonal correction only (mic / phone colouration), not voice timbre: cubic fit over log-frequency
    sel = (f > 90) & (f < 11000)
    lf = np.log2(f[sel])
    poly = np.polyfit(lf, p_ref[sel] - p[sel], 3)
    entries = []
    for fc in bands:
        d = float(np.polyval(poly, np.log2(fc)))
        d = np.clip(0.7 * d, -4, 3 if fc < 250 else 4)
        if g.startswith("T_") and fc >= 1200:  # Tarun: add body, never trade away presence/clarity
            d = max(d, 0.0)
        entries.append((round(fc), round(float(d), 1)))
    match[g] = entries

eq = []
for i, x in enumerate(segs):
    g = VOICE[i]
    x = x * 10 ** (gain[g] / 20)
    if g in match:
        x = ffx(x, "firequalizer=gain_entry='" + ";".join(f"entry({f},{d})" for f, d in match[g]) + "'")
    eq.append(x)
# re-level each speaker group after the tonal match so Prahalad and Tarun sit at the same loudness
post = {g: -20.0 - lufs(np.concatenate([eq[i] for i in range(len(SEGS)) if VOICE[i] == g])) for g in groups}
voice = np.zeros(N, np.float32)
for i, x in enumerate(eq):
    place(voice, fade(x * 10 ** (post[VOICE[i]] / 20)), START[i] / FPS, 0)
chain = ("highpass=f=75:poles=2,equalizer=f=240:t=q:w=1.1:g=-1.2,equalizer=f=3400:t=q:w=1.3:g=1.8,"
         "deesser=i=0.3,acompressor=threshold=-24dB:ratio=2.4:attack=10:release=150:makeup=2")
voice = ffx(voice, chain)
voice *= 10 ** ((-17.5 - lufs(voice)) / 20)  # mono -17.5 LUFS → about -14.5 LUFS on the stereo master

# speech envelope for ducking the beds
h = SR // 50
e = np.sqrt(np.convolve(voice ** 2, np.ones(h) / h, "same"))
speech = np.clip((20 * np.log10(e + 1e-9) + 45) / 15, 0, 1)
speech = np.convolve(speech, np.ones(SR // 8) / (SR // 8), "same")


# ================= ambience beds (synthesized, clean, very low) =================
def pink(n):
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    X[1:] /= np.sqrt(f[1:])
    X[0] = 0
    return np.fft.irfft(X, n)


def crickets(n, f0, period, level):
    out = np.zeros(n)
    t = 0.0
    while t < n / SR:
        for k in range(3):
            i = int((t + k * 0.045) * SR)
            m = int(0.018 * SR)
            if i + m < n:
                tt = np.arange(m) / SR
                out[i:i + m] += np.sin(2 * np.pi * f0 * tt) * np.sin(np.pi * tt / 0.018) ** 2
        t += period * (0.8 + 0.4 * rng.random())
    return out * level


def bed(kind, n):
    air = pink(n)
    if kind == "day":
        x = filt(air, "bandpass", [180, 6500]) + 0.9 * filt(pink(n), "lowpass", 260) * (
            1 + 0.35 * np.sin(2 * np.pi * 0.07 * np.arange(n) / SR))
    elif kind == "dusk":
        x = filt(air, "bandpass", [150, 5000]) + 0.6 * filt(pink(n), "lowpass", 240)
    elif kind in ("night", "night2"):
        x = filt(air, "bandpass", [120, 3200]) + 0.4 * filt(pink(n), "lowpass", 200)
        x = x / np.std(x) + crickets(n, 4350 if kind == "night" else 4650, 0.85, 0.12) + crickets(n, 3900, 1.3, 0.07)
    else:  # street at night (selfie walk)
        x = filt(air, "bandpass", [140, 4200]) + 0.8 * filt(pink(n), "lowpass", 300)
    return x / np.std(x)


LEVEL = {"day": -46, "dusk": -47, "night": -48, "night2": -48, "street": -46}
amb = np.zeros(N)
xf = int(0.2 * SR)  # 6-frame constant-power crossfade at each location cut
for k, (t0, kind) in enumerate(AMBIENCE):
    a = max(0, int(t0 * SR) - xf // 2)
    b = N if k + 1 == len(AMBIENCE) else min(N, int(AMBIENCE[k + 1][0] * SR) + xf // 2)
    x = bed(kind, b - a)
    x *= 10 ** ((LEVEL[kind] - lufs(x.astype(np.float32))) / 20)
    w = np.ones(b - a)
    if k > 0:
        w[:xf] = np.sin(np.linspace(0, np.pi / 2, xf))
    if k + 1 < len(AMBIENCE):
        w[-xf:] = np.cos(np.linspace(0, np.pi / 2, xf))
    amb[a:b] += x * w
amb *= 10 ** (-4 * speech / 20)  # duck 4 dB under speech
amb[:int(0.15 * SR)] *= np.linspace(0, 1, int(0.15 * SR))

# ================= natural sound from the B-roll =================
nat = np.zeros(N, np.float32)


def natural(src, s_in, t0, t1, level, hp=150):
    x = load(os.path.join(BROLL, f"MVI_{src}.MP4"), s_in, t1 - t0)
    x = fade(filt(x, "highpass", hp), 40, 60)
    place(nat, x, t0, level - lufs(x))


natural("0436", 1.9, T(2, 1.50), T(2, 2.62), -34)          # footsteps, J-cut 0.3 s before the picture
natural("0431", 1.0, T(4, 9.90), T(5, 12.22), -36, 400)    # keys / trackpad under the build montage
natural("0446", 1.45, T(12, 8.20), T(12, 8.90), -33)       # real laptop lid closing


# ================= designed SFX moments + flash-cut SFX =================
def t_axis(d):
    return np.arange(int(d * SR)) / SR


def paper_flick():
    n = int(0.09 * SR)
    x = filt(rng.standard_normal(n), "bandpass", [1200, 7500]) * env(n, 0.002, 0.022)
    return x * (1 + 0.5 * np.sin(2 * np.pi * 41 * np.arange(n) / SR))


def paper_tap():  # card settling onto paper: soft low tap + short paper texture
    t = t_axis(0.16)
    return (0.8 * np.sin(2 * np.pi * (180 + 90 * np.exp(-t / 0.01)) * t) * env(len(t), 0.002, 0.03)
            + 0.5 * filt(rng.standard_normal(len(t)), "bandpass", [800, 5000]) * env(len(t), 0.001, 0.015))


def air_whoosh(d=0.32, lo=250, hi=3500):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    y = filt(x, "bandpass", [lo, 1200]) * (1 - t / d) + filt(x, "bandpass", [1200, hi]) * (t / d)
    return y * np.sin(np.pi * t / d) ** 2


def notify():  # muted phone notification: two soft sine notes, rounded
    t = t_axis(0.42)
    a = np.sin(2 * np.pi * 1046.5 * t) * env(len(t), 0.006, 0.08)
    b = np.sin(2 * np.pi * 1568 * t) * np.where(t > 0.09, env(len(t), 0.006, 0.12), 0)
    return filt(a + 0.8 * b, "lowpass", 5000)


def low_impact():
    t = t_axis(0.7)
    f = 40 + 34 * np.exp(-t / 0.09)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.006, 0.2) + 0.05 * filt(
        rng.standard_normal(len(t)), "lowpass", 300) * env(len(t), 0.002, 0.04)


def power_down():  # quiet browser-tab close / UI power-down
    t = t_axis(0.38)
    f = 700 * np.exp(-t / 0.11) + 140
    click = filt(rng.standard_normal(len(t)), "bandpass", [2500, 6000]) * env(len(t), 0.0003, 0.003)
    return 0.7 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.003, 0.1) + 0.35 * click


FLASH_PRE = 0.07  # the flash SFX's airy lead-in; its snap lands on the cut frame


def flash_snap(level):  # flash cut: short airy lift into a bright shutter-like snap + a quick shimmer tail
    t = t_axis(FLASH_PRE + 0.32)
    n, k = len(t), int(FLASH_PRE * SR)
    lift = np.zeros(n)
    lift[:k] = filt(rng.standard_normal(k), "bandpass", [2200, 9000]) * (np.arange(k) / k) ** 2.2 * 0.45
    tail = np.zeros(n)
    tail[k:] = (filt(rng.standard_normal(n - k), "highpass", 2800) * env(n - k, 0.0008, 0.0045)
                + 0.35 * filt(rng.standard_normal(n - k), "bandpass", [4500, 12000]) * env(n - k, 0.003, 0.06))
    j = k + int(0.022 * SR)  # second, softer shutter blade
    tail[j:] += 0.35 * filt(rng.standard_normal(n - j), "highpass", 3500) * env(n - j, 0.0005, 0.003)
    x = filt(lift + tail, "lowpass", 14000)
    if level == 3:  # speaker changes get a faint low body under the snap
        tt = t[k:] - t[k]
        x[k:] += 0.22 * np.sin(2 * np.pi * (68 + 40 * np.exp(-tt / 0.02)) * tt) * env(n - k, 0.002, 0.05)
    return x


PAPER_PRE = 0.035


def paper_cut():  # quick paper swipe ending in a crisp snip on the cut
    t = t_axis(PAPER_PRE + 0.12)
    n, k = len(t), int(PAPER_PRE * SR)
    fibre = 1 + 0.8 * np.abs(filt(rng.standard_normal(n), "lowpass", 180)) / 0.05
    swipe = filt(rng.standard_normal(n), "bandpass", [900, 6500]) * fibre
    shape = np.where(np.arange(n) < k, (np.arange(n) / k) ** 1.5, np.exp(-(np.arange(n) - k) / (0.03 * SR)))
    snip = np.zeros(n)
    snip[k:] = filt(rng.standard_normal(n - k), "highpass", 3000) * env(n - k, 0.0004, 0.0025) * 2.2
    return swipe * shape / np.max(np.abs(swipe * shape)) + snip


def micro_riser():
    t = t_axis(0.7)
    s = (t / 0.7) ** 2
    tone = sum(a * np.sin(2 * np.pi * f * t * (1 + 0.05 * t)) for f, a in ((261.6, 1), (392, 0.6), (523.3, 0.3)))
    return (tone + 0.35 * filt(rng.standard_normal(len(t)), "bandpass", [2500, 8000]) * s) * s * np.where(
        t > 0.66, np.cos(np.pi / 2 * (t - 0.66) / 0.04), 1)


sfx = np.zeros(N, np.float32)
cues = []


def cue(moment, name, fn, t, peak_db):
    x = fn()
    x = x / (np.max(np.abs(x)) or 1)
    place(sfx, x, t, peak_db)
    cues.append({"moment": moment, "sfx": name, "t": round(t, 3), "peak_db": peak_db})


p0 = OVER["paper"][0]
for k, fr in enumerate(MATCH_PAGES[:-1]):
    cue(1, "paper page flick (texture)", paper_flick, p0 + fr / FPS, -40)
cue(1, "premium paper tap (logo card settles)", paper_tap, p0 + MATCH_PAGES[-1] / FPS, -29)
cue(3, "muted phone notification (₹1,500 proof)", notify, OVER["pay"][0] + 0.04, -28)
cue(4, "single low impact / sub drop (nothing happened)", low_impact, T(7, 6.58), -23)
cue(5, "quiet browser-tab close (site held offline)", power_down, OVER["notpub"][0] + 0.03, -29)
cue(6, "directional air whip (real camera whip)", lambda: air_whoosh(0.3, 400, 6000), WHIP_CUT / FPS - 0.15, -25)
cue(7, "short hopeful micro-riser (Part 2)", micro_riser, OVER["end"][0] - 0.7, -30)
# flash-cut pass: one SFX on every change to the next clip or speaker. Its peak follows what is already playing
# at the cut (voice + natural sound + ambience): over speech it sits ~15-20 dB under the voice in RMS (a short
# bright transient still reads), in a pause it drops so it never jumps out of the silence; peaks capped at -11 dBFS
OFFSET = {("flash", 3): 6, ("flash", 2): 4, ("flash", 1): 2, ("paper", 2): 4, ("paper", 1): 3}
under = voice + nat + amb.astype(np.float32)


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(np.square(x, dtype=np.float64))) + 1e-9)


for t, kind, lvl, what in FLASHCUTS:
    fn, pre = (lambda: flash_snap(lvl), FLASH_PRE) if kind == "flash" else (paper_cut, PAPER_PRE)
    local = rms_db(under[int((t - 0.25) * SR):int((t + 0.25) * SR)])
    peak = float(np.clip(local + OFFSET[kind, lvl], -24, -11))
    cue(kind, f"{'flash snap' if kind == 'flash' else 'paper cut'} L{lvl} ({what})", fn, t - pre, round(peak, 1))

mix = voice + nat + sfx + amb.astype(np.float32)
pre = os.path.join(TMP, "_mix.wav")
save(pre, mix)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", "alimiter=limit=0.89:attack=3:release=40:level=false",
                "-ar", str(SR), "-c:a", "pcm_s24le", os.path.join(OUT, "master.wav")], check=True)
save(os.path.join(OUT, "voice_only.wav"), voice)
for f in os.listdir(TMP):
    os.remove(os.path.join(TMP, f))
os.rmdir(TMP)
json.dump({"sfx": cues, "voice_gain_db": gain, "match_eq": match}, open(os.path.join(OUT, "sfx_cues.json"), "w"),
          indent=1, ensure_ascii=False)
print("group gains:", {k: round(v, 1) for k, v in gain.items()})
for g, m in match.items():
    print(g, " ".join(f"{f}:{d:+.1f}" for f, d in m))
print("SFX moments:", len({c["moment"] for c in cues}), "| flash/paper cuts:", sum(isinstance(c["moment"], str) for c in cues))
