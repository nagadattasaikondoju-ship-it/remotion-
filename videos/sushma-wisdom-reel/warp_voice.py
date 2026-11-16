# Fit the new narration to the original speaker's word timing, so every kinetic caption still lands on its spoken word.
#   python3 warp_voice.py REF_WORDS.json NEW_WORDS.json OFFS.json LINES.tsv LINE_DIR OUT.wav
# REF_WORDS: Whisper word timestamps of the reference audio. NEW_WORDS + OFFS: Whisper on the new lines laid end to end
# (OFFS = each line's [start, end] in that file). Each line is cut at its matched words (difflib on the word lists) and each piece
# is time-stretched gently (atempo, 0.85-1.2x, never overlapping the previous piece) to start where the original word started.
import json, sys, re, difflib, subprocess
import numpy as np, soundfile as sf
ref_p, new_p, offs_p, lines_p, ldir, out_p = sys.argv[1:7]
SR = 48000; DUR = 37.9
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower().replace("odour", "odor").replace("dr.", "doctor"))
ref = [(norm(w["word"]), w["start"], w["end"]) for s in json.load(open(ref_p))["segments"] for w in s["words"]]
new = [(norm(w["word"]), w["start"], w["end"]) for s in json.load(open(new_p))["segments"] for w in s["words"]]
offs = json.load(open(offs_p))
lines = [l.rstrip("\n").split("\t") for l in open(lines_p)]
out = np.zeros(int(DUR * SR), np.float32)

def stretch(x, sr, factor):
    """Play x so it lasts factor times as long (factor < 1 = faster)."""
    tempo = float(np.clip(1 / factor, 0.85, 1.2))
    if abs(tempo - 1) < 0.02 or len(x) < sr * 0.12: return x
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.4f}",
                        "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True)
    return np.frombuffer(r.stdout, np.float32)

def put(x, t):
    k = int(t * SR); n = min(len(x), len(out) - k)
    if n <= 0: return
    f = min(n, int(0.012 * SR)); x = x[:n].copy(); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    out[k:k + n] += x

for i, (a, b, text) in enumerate(lines):
    a, b = float(a), float(b)
    o0, o1 = offs[i]
    nw = [(w, s - o0, e - o0) for w, s, e in new if o0 - 0.05 <= s <= o1]
    rw = [(w, s, e) for w, s, e in ref if a - 0.15 <= s < b]
    x, sr = sf.read(f"{ldir}/l{i + 1}.wav"); x = x if x.ndim == 1 else x.mean(1)
    if sr != SR:
        x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f64le", "-ar", str(sr), "-ac", "1", "-i", "-", "-ar", str(SR),
                                          "-f", "f32le", "-"], input=x.astype(np.float64).tobytes(), capture_output=True).stdout, np.float32)
    sm = difflib.SequenceMatcher(a=[w for w, _, _ in nw], b=[w for w, _, _ in rw], autojunk=False)
    anchors = []
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): anchors.append((nw[blk.a + k][1], rw[blk.b + k][1]))
    if not anchors: anchors = [(nw[0][1] if nw else 0.0, a)]
    # keep anchors increasing on both sides
    clean = []
    for n_, r_ in anchors:
        if not clean or (n_ > clean[-1][0] + 0.06 and r_ > clean[-1][1] + 0.06): clean.append((n_, r_))
    anchors = clean
    speech_end = (nw[-1][2] if nw else len(x) / SR) + 0.12
    if len(anchors) <= 2:   # short line, or one whose words differ (the new clinic name): place it whole, fitted to its window
        s0 = max(0.0, (nw[0][1] if nw else 0.0) - 0.06); seg = x[int(s0 * SR):int(speech_end * SR)]
        start = anchors[0][1] - (anchors[0][0] - s0)
        put(stretch(seg, SR, min(1.0, (b - start) / max(0.05, len(seg) / SR))), start)
        print(f"line {i + 1:2d}: placed whole at {start:.2f}  {text[:50]}"); continue
    n0, r0 = anchors[0]; lead = x[:int(n0 * SR)]
    lead = lead[max(0, len(lead) - int(0.25 * SR)):]
    put(lead, r0 - len(lead) / SR)
    last_end = r0
    for j, (n_, r_) in enumerate(anchors):
        n_next = anchors[j + 1][0] if j + 1 < len(anchors) else speech_end
        r_next = anchors[j + 1][1] if j + 1 < len(anchors) else r_ + (speech_end - n_)
        start = max(r_, last_end)
        seg = stretch(x[int(n_ * SR):int(n_next * SR)], SR, max(0.05, r_next - start) / max(0.05, n_next - n_))
        put(seg, start); last_end = start + len(seg) / SR
    print(f"line {i + 1:2d}: {len(anchors)} anchors of {len(nw)} words  {text[:50]}")
sf.write(out_p, out, SR)
