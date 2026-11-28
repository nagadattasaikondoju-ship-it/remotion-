"""Deploy act reel: three phone takes → one continuous 1080×1920 video with cleaned dialogue.

Run: python3 scripts/build.py   (needs the DeepFilterNet3 *_dn.wav files in CLEAN, see README)
Story order (also the recording order):
  1. 17:10  at the laptop  — "…don't worry about it, it will look fine, you can deploy."
  2. 17:16  at the laptop  — "I can do it in five or six minutes." → they get to work
  3. 17:24  on the phone   — "…it's failing in deployment. Can you just change the developer, please?"
"""
import os
import subprocess

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
UP = "/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e"
CLEAN = "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/act"
OUT = os.path.join(ROOT, "renders")
TMP = os.path.join(OUT, "_tmp")
FPS, SR = 30, 48000
XF = 0.06  # audio crossfade at each cut (2 frames, no clicks)

# (video, cleaned audio, in, out) — every in/out sits in a pause, never inside a word
CLIPS = [
    (f"{UP}/254f1aeb-VID_20261016_171010029.mp4", "c1010_dn.wav", 0.40, 8.64),
    (f"{UP}/c997a793-VID_20261016_171607644.mp4", "c1016_dn.wav", 0.00, 3.60),
    (f"{UP}/ba428f5b-VID_20261016_172436560.mp4", "c1024_dn.wav", 0.60, 11.20),
]
# light, shared polish so the three takes match: phone-noise cleanup, a touch of contrast and colour, crisp detail
VF = ("fps=30,scale=1080:1920:flags=lanczos,hqdn3d=1.5:1.5:6:6,"
      "eq=contrast=1.04:saturation=1.06:gamma=0.99,unsharp=5:5:0.45:5:5:0")


def load(path, ss, dur):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ss}", "-t", f"{dur}", "-i", path, "-ac", "1", "-ar",
                        str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32).copy()


def lufs(x):  # EBU R128 integrated loudness (gated, so pauses don't count)
    err = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                          "-af", "ebur128", "-f", "null", "-"], input=x.astype(np.float32).tobytes(),
                         capture_output=True).stderr.decode()
    return float(err.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])


def pink(n, seed):
    X = np.fft.rfft(np.random.default_rng(seed).standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    X[1:] /= np.sqrt(f[1:])
    X[f < 60] = 0
    X[f > 6000] *= np.exp(-(f[f > 6000] - 6000) / 3000)
    y = np.fft.irfft(X, n)
    return y / np.sqrt(np.mean(y ** 2))


os.makedirs(TMP, exist_ok=True)
# ---------- picture ----------
parts = []
for k, (v, _, a, b) in enumerate(CLIPS):
    p = os.path.join(TMP, f"v{k}.mp4")
    n = round((b - a) * FPS)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{a}", "-i", v, "-an", "-vf", VF,
                    "-frames:v", str(n), "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p",
                    p], check=True)
    parts.append((p, n))
lst = os.path.join(TMP, "list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p, _ in parts))
pic = os.path.join(TMP, "pic.mp4")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", pic],
               check=True)

# ---------- dialogue: cleaned takes, levelled to each other, short crossfades at the cuts ----------
segs = []
for (_, wav, a, b), (_, n) in zip(CLIPS, parts):
    x = load(os.path.join(CLEAN, wav), a, n / FPS + XF)
    x = np.pad(x, (0, max(0, int((n / FPS + XF) * SR) - len(x))))
    segs.append(x)
ref = lufs(segs[0])
segs = [s * 10 ** ((ref - lufs(s)) / 20) for s in segs]
total = sum(n for _, n in parts) / FPS
N = int(round(total * SR))
voice = np.zeros(N + int(XF * SR), np.float32)
t = 0
xf = int(XF * SR)
for s, (_, n) in zip(segs, parts):
    i = int(round(t * SR))
    s = s.copy()
    s[:xf] *= np.sin(np.linspace(0, np.pi / 2, xf)) ** 2 if t > 0 else 1
    s[-xf:] *= np.cos(np.linspace(0, np.pi / 2, xf)) ** 2
    voice[i:i + len(s)] += s[: len(voice) - i]
    t += n / FPS
voice = voice[:N]
# barely-there clean outdoor air (45 dB under the voice), so the pauses never drop into dead digital silence
bed = pink(N, 3) * 10 ** ((ref - 45) / 20)
mix = voice + bed.astype(np.float32)
raw = os.path.join(TMP, "mix.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", raw],
               input=mix.astype(np.float32).tobytes(), check=True)
chain = ("highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1.4:g=2,deesser=i=0.35,"
         "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=2,"
         "loudnorm=I=-14:TP=-1.5:LRA=7,alimiter=limit=0.89:level=false")
aud = os.path.join(OUT, "deploy_act_audio.wav")
pre = os.path.join(TMP, "chain.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", chain, "-ar", str(SR), "-c:a", "pcm_f32le", pre],
               check=True)
# second pass: exact −14 LUFS integrated (one-pass loudnorm undershoots on a clip this short), ≤ −1 dBTP
meas = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", pre, "-af", "ebur128", "-f", "null", "-"],
                      capture_output=True, text=True).stderr
lufs = float(meas.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af",
                f"volume={-14.0 - lufs:.2f}dB,alimiter=limit=0.88:attack=3:release=50:level=false",
                "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s24le", aud], check=True)

# ---------- master + share ----------
master = os.path.join(OUT, "Deploy_Act_master_1080x1920.mp4")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", pic, "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v",
                "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", master], check=True)
share = os.path.join(OUT, "Deploy_Act_share.mp4")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", master, "-c:v", "libx264", "-preset", "slow", "-crf",
                "18", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                "-movflags", "+faststart", share], check=True)
for f in os.listdir(TMP):
    os.remove(os.path.join(TMP, f))
os.rmdir(TMP)
print(f"{total:.2f} s  cuts at", [round(sum(n for _, n in parts[:k]) / FPS, 2) for k in range(1, len(parts))])
