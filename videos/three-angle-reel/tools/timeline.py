# Output timeline shared by tools/base.py (picture) and index.html (captions + graphics):
#   intro (host, full screen) → split (sample clip on top, host listening below) → main (host, full screen, pauses cut).
# Every Whisper word is mapped to its time in the finished reel.  python3 tools/timeline.py <host whisper> <sample whisper>
import sys, json
e = json.load(open("edl.json"))
FIX = {"Metastell": "Meta still", "DMS": "DM us", "Meta.": "META."}           # Whisper slips, checked against the audio
i0, i1 = e["intro"]; s0, s1 = e["sample"]
T_SPLIT = i1 - i0; T_MAIN = T_SPLIT + (s1 - s0)
segs = [{"kind": "intro", "t0": 0, "t1": T_SPLIT, "src0": i0}, {"kind": "split", "t0": T_SPLIT, "t1": T_MAIN, "src0": s0}]
t = T_MAIN
for a, b in e["clips"]:
    segs.append({"kind": "main", "t0": round(t, 4), "t1": round(t + b - a, 4), "src0": a}); t += b - a
END = round(t, 4)
def host_out(h):
    if i0 <= h <= i1: return h - i0
    for s in segs:
        if s["kind"] == "main" and s["src0"] <= h <= s["src0"] + (s["t1"] - s["t0"]) + 1e-6: return s["t0"] + h - s["src0"]
    return None
words = []
for s in json.load(open(sys.argv[1]))["segments"]:
    for w in s["words"]:
        a, b = host_out(w["start"]), host_out(w["end"])
        if a is None and b is None: continue
        if a is None: a = b - 0.15
        if b is None: b = a + 0.15
        txt = w["word"].strip(); parts = FIX.get(txt, txt).split(" ")      # a fix may be two words: split the time evenly
        for j, p in enumerate(parts):
            d = (b - a) / len(parts)
            words.append({"w": p, "t0": round(a + j * d, 3), "t1": round(a + (j + 1) * d, 3), "who": "host"})
for s in json.load(open(sys.argv[2]))["segments"]:
    for w in s["words"]:
        words.append({"w": w["word"].strip(), "t0": round(T_SPLIT + w["start"] - s0, 3), "t1": round(T_SPLIT + w["end"] - s0, 3), "who": "sample"})
words.sort(key=lambda w: w["t0"])
json.dump({"END": END, "T_SPLIT": T_SPLIT, "T_MAIN": T_MAIN, "segs": segs, "words": words}, open("timeline.json", "w"), indent=1)
print("END", END, "split", T_SPLIT, "main", T_MAIN, "words", len(words))
for w in words: print(f'{w["t0"]:6.2f} {w["who"][0]} {w["w"]}', end=" |")
