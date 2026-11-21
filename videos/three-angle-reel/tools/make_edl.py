# Cut list for the host take: drop every pause between Whisper words where the audio really goes quiet.
# Pads keep 60 ms after the last word and 50 ms before the next, so tails and breaths-in survive.
#   python3 tools/make_edl.py host48.wav whisper.json > edl.json
import sys, json, wave, numpy as np
w = wave.open(sys.argv[1]); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768
hop = sr // 100; n = len(x) // hop
db = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
db = np.convolve(db, np.ones(5) / 5, "same"); thr = np.percentile(db, 95) - 24
words = [wd for s in json.load(open(sys.argv[2]))["segments"] for wd in s["words"]]
MAIN0, MAIN1 = 2.93, 42.30                     # "Pick the age…" → "…DM us META." (the intro and the tail are cut elsewhere)
cuts = []
for a, b in zip(words, words[1:]):
    g0, g1 = a["end"], b["start"]
    if g1 - g0 < 0.24 or g1 < MAIN0 or g0 > MAIN1: continue
    i0, i1 = int((g0 - 0.12) * 100), int((g1 + 0.12) * 100)
    q = db[i0:i1] < thr; best = (0, 0); s = None
    for i, v in enumerate(list(q) + [False]):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s > best[1] - best[0]: best = (s, i)
            s = None
    if (best[1] - best[0]) / 100 >= 0.16:
        cuts.append(((i0 + best[0]) / 100 + 0.06, (i0 + best[1]) / 100 - 0.05))
clips, t = [], MAIN0
for c0, c1 in cuts:
    if c1 - c0 > 0.04: clips.append([round(t, 3), round(c0, 3)]); t = c1
clips.append([round(t, 3), MAIN1])
out = {"intro": [0.45, 2.50], "sample": [0.0, 10.767], "listen": [41.70, 45.20], "clips": clips}
print(json.dumps(out, indent=1))
print(len(clips), "clips", round(sum(b - a for a, b in clips), 2), "s (from", round(MAIN1 - MAIN0, 2), ")", file=sys.stderr)
