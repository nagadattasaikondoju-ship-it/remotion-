"""Teammate's voiceover (WhatsApp voice note, 25 Nov) -> vo/voice.wav on the reel's beats, plus vo/times.json for the place-name pops.
Each of the 14 script lines (vo/lines.tsv: start, slot end) is cut from vo/team_vo.wav at the quietest 10 ms between lines
(word times from faster-whisper small.en in vo/team_words.json), lightly cleaned, and placed at its start; sped up only if it
overruns its slot (atempo, <= 1.12). Levelled to -17.3 LUFS (assemble.sh lifts the voice +3.5 dB to the reference VO's level)."""
import json, subprocess, numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SR = 48000; DUR = 49.7667
LINES = [(0, 15), (16, 25), (26, 36), (37, 46), (47, 53), (54, 62), (63, 67), (68, 70), (71, 72), (73, 79), (80, 89), (90, 96), (97, 110), (111, 117)]
W = json.load(open("vo/team_words.json"))
slots = [tuple(map(float, l.split("\t")[:2])) for l in open("vo/lines.tsv").read().strip().split("\n")]
# 17-26 s: the reference VO was slow here and the picture's beats ("Growth" 22.96, "Value" 24.46) follow it, so lines 5 and 6 are split
# into phrases anchored on the reference's own words, eased 10 % slower; otherwise the teammate's faster read left ~1.6 s holes
SPLIT = {4: [((47, 50), 17.92, 1.0), ((51, 53), 19.66, 0.9)], 5: [((54, 57), 21.66, 0.9), ((58, 62), 23.90, 0.9)]}
PH = []   # (first word, last word, start, slot end, forced tempo or None)
for k, (ij, (st, en)) in enumerate(zip(LINES, slots)):
    if k in SPLIT:
        parts = SPLIT[k]
        for m, ((i, j), t0, tp) in enumerate(parts): PH.append((i, j, t0, parts[m + 1][1] if m + 1 < len(parts) else en, tp))
    else: PH.append((ij[0], ij[1], st, en, None))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "vo/team_vo.wav", "-af", "highpass=f=80,afftdn=nf=-42:nr=10", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
a = np.frombuffer(raw, np.float32).copy()
def quiet(t0, t1):   # quietest 10 ms in [t0, t1]
    i0, i1 = int(t0 * SR), max(int(t1 * SR), int(t0 * SR) + 480); hop = 480
    e = [np.sqrt((a[i:i + hop] ** 2).mean()) for i in range(i0, i1 - hop + 1, hop // 4)]
    return (i0 + int(np.argmin(e)) * hop // 4 + hop // 2) / SR
cuts = []
for k, (i, j, *_) in enumerate(PH):
    s = W[i]["s"]; e = W[j]["e"]
    prev_e = W[PH[k - 1][1]]["e"] if k else 0; next_s = W[PH[k + 1][0]]["s"] if k + 1 < len(PH) else len(a) / SR
    c0 = quiet(max(prev_e - .02, s - .16), s + .02) if k else max(0, s - .10)
    c1 = quiet(e - .02, min(next_s + .02, e + .16)) if k + 1 < len(PH) else min(len(a) / SR, e + .25)
    cuts.append((c0, c1))
out = np.zeros(int(DUR * SR) + SR, np.float32); times = {}
for k, ((c0, c1), (i0, j0, st, en, forced)) in enumerate(zip(cuts, PH)):
    seg = a[int(c0 * SR):int(c1 * SR)].copy(); f = int(.012 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    tempo = 1.0
    if len(seg) / SR > en - st + .05: tempo = min(1.12, (len(seg) / SR) / (en - st))
    if forced: tempo = forced
    if tempo != 1.0:
        seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.4f}", "-f", "f32le", "-"],
                                           input=seg.tobytes(), capture_output=True).stdout, np.float32)
    p = int(st * SR); out[p:p + len(seg)] += seg
    for i in range(i0, j0 + 1):
        key = {68: "tKom", 69: "tGac", 70: "tSad", 71: "tFive"}.get(i)
        if key: times[key] = round(st + (W[i]["s"] - c0) / tempo, 3)
    print(f"phrase {k + 1:2d}: {c0:6.2f}-{c1:6.2f} ({c1 - c0:4.2f} s) -> {st:6.2f} slot {en - st:4.2f} tempo {tempo:.3f}")
out = out[:int(DUR * SR)]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_f32le", "vo/_raw.wav"], input=out.tobytes())
def lufs(f):
    J = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(json.loads(J[J.rindex("{"):J.rindex("}") + 1])["input_i"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "vo/_raw.wav", "-af", "equalizer=f=3200:t=q:w=1.3:g=1.5,acompressor=threshold=-26dB:ratio=2.2:attack=8:release=120", "-c:a", "pcm_f32le", "vo/_c.wav"])
g = -17.3 - lufs("vo/_c.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "vo/_c.wav", "-af", f"volume={g:.2f}dB,alimiter=limit=0.94:level=0:attack=2:release=40", "-c:a", "pcm_s16le", "vo/voice.wav"])
os.remove("vo/_raw.wav"); os.remove("vo/_c.wav"); print(f"voice {lufs('vo/voice.wav'):.1f} LUFS")
json.dump(times, open("vo/times.json", "w")); print("times", times)
