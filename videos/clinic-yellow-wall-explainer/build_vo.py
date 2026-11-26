# Lays the trimmed voice lines (vo/t<N>.wav) on the timeline (STARTS) and transcribes each for word timings -> vo/voice.wav, timeline.json
import json, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
STARTS = [0.25, 2.70, 4.30, 8.00, 10.90, 13.20, 16.50, 19.25, 22.00, 25.60, 29.60, 32.60]
DUR = 37.4; SR = 48000
texts = [l.rstrip("\n").split("\t")[2] for l in open("vo/lines.tsv")]
m = WhisperModel("small.en", device="cpu", compute_type="int8")
out = np.zeros(int(DUR * SR), np.float32); lines = []
for i, (t0, text) in enumerate(zip(STARTS, texts)):
    x, sr = sf.read(f"vo/t{i+1}.wav", dtype="float32"); x = x if x.ndim == 1 else x.mean(1)
    k = int(t0 * SR); out[k:k + len(x)] += x[:len(out) - k]
    segs, _ = m.transcribe(f"vo/t{i+1}.wav", word_timestamps=True, initial_prompt=text, language="en")
    heard = [(w.word.strip(), round(t0 + w.start, 3), round(t0 + w.end, 3)) for s in segs for w in s.words]
    # caption with the SCRIPT words (exact text), timed by the heard words in order
    sw = text.split(); words = []
    for j, w in enumerate(sw):
        h = heard[min(j * len(heard) // max(1, len(sw)), len(heard) - 1)] if len(heard) != len(sw) else heard[j]
        words.append({"w": w, "s": h[1], "e": h[2]})
    lines.append({"i": i + 1, "start": t0, "end": round(t0 + len(x) / SR, 3), "text": text, "words": words,
                  "heard": " ".join(h[0] for h in heard)})
    print(i + 1, len(heard), len(sw), "|", " ".join(h[0] for h in heard))
sf.write("vo/voice.wav", out, SR)
json.dump({"dur": DUR, "lines": lines}, open("timeline.json", "w"), indent=1)
