"""Generate index.html (timeline + audio tags) from the cut map + word timings.

Run: python3 scripts/build_html.py
Word times are on the source *video* timeline (forced alignment + energy check); they are
mapped onto the jump-cut output timeline with the same segment table as build_cut.py.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
FPS = 30

# (id, src start, src end) -- keep in sync with build_cut.py (frame-snapped there)
SEGS = [("hook-a", 1.95, 4.62), ("hook-b", 4.74, 5.90), ("miss-a", 6.22, 7.17), ("miss-b", 7.33, 8.56),
        ("build", 8.74, 14.35), ("does-a", 14.60, 15.80), ("does-b", 15.96, 19.38), ("home", 19.64, 22.16),
        ("cta", 22.40, 24.70)]
fr = lambda t: round(t * FPS)
starts, t = [], 0
for sid, a, b in SEGS:
    starts.append((sid, fr(a) / FPS, t / FPS, (fr(b) - fr(a)) / FPS))
    t += fr(b) - fr(a)
TOTAL = t / FPS


def out(src):
    for sid, s, o, d in starts:
        if s - 0.25 <= src < s + d:
            return round(o + max(0.0, src - s), 3)
    raise ValueError(src)


# word onsets on the source video timeline (aligner output + 0.094 s audio offset)
W = [("how", 2.11), ("many", 2.33), ("customers", 2.63), ("are", 3.17), ("calling", 3.30), ("your", 3.67),
     ("business", 3.77), ("right", 4.17), ("now", 4.38), ("and", 4.85), ("nobody's", 5.01), ("picking", 5.42),
     ("up", 5.72),
     ("that", 6.34), ("missed", 6.64), ("call", 6.86), ("could", 7.13), ("be", 7.46), ("a", 7.68), ("missed", 7.71),
     ("customer", 8.02),
     ("we", 8.84), ("build", 9.13), ("AI", 9.44), ("voice", 9.71), ("agents", 10.05), ("that", 10.48), ("can", 10.67),
     ("answer", 10.80), ("calls", 11.11), ("and", 11.49), ("understand", 11.58), ("what", 12.0), ("the", 12.30),
     ("customer", 12.36), ("needs", 12.84), ("and", 13.21), ("respond", 13.37), ("instantly", 13.77),
     ("they", 14.69), ("can", 14.77), ("qualify", 14.97), ("leads", 15.42), ("book", 15.98),
     ("appointments", 16.21), ("and", 16.85), ("handle", 17.03), ("common", 17.44), ("questions", 17.77),
     ("even", 18.27), ("after", 18.63), ("hours", 18.98),
     ("your", 19.69), ("business", 19.92), ("shouldn't", 20.56), ("stop", 20.84), ("answering", 21.11),
     ("when", 21.44), ("you", 21.57), ("go", 21.71), ("home", 21.92),
     ("comment", 22.49), ("voice", 22.79), ("and", 23.23), ("I'll", 23.47), ("send", 23.64), ("you", 23.82),
     ("the", 23.92), ("demo", 24.0)]
WO = [(w, out(s)) for w, s in W]
END_OF_SPEECH = out(24.35)

# caption chunks: lists of lines, each line a list of word indices
idx = {}
chunks_def = [
    [[0, 1, 2]], [[3, 4], [5, 6]], [[7, 8]], [[9, 10], [11, 12]],
    [[13, 14, 15]], [[16, 17, 18], [19, 20]],
    [[21, 22, 23], [24, 25]], [[26, 27], [28, 29]], [[30, 31]], [[32, 33], [34, 35]], [[36, 37], [38]],
    [[39, 40, 41], [42]], [[43], [44]], [[45, 46], [47, 48]], [[49, 50, 51]],
    [[52, 53], [54, 55]], [[56, 57], [58, 59, 60]],
    [[61, 62]], [[63, 64, 65, 66], [67, 68]],
]
KEY = {2, 10, 14, 19, 20, 24, 25, 38, 42, 44, 48, 51, 60, 62, 68}  # accent-colour words (indices into W)
chunks = []
for ci, lines in enumerate(chunks_def):
    flat = [i for ln in lines for i in ln]
    t0 = WO[flat[0]][1]
    # hold until the next chunk starts (or ~0.3 s after the last word, or the end)
    nxt = WO[chunks_def[ci + 1][0][0]][1] if ci + 1 < len(chunks_def) else TOTAL
    t1 = min(nxt - 0.02, WO[flat[-1]][1] + 0.55) if ci + 1 < len(chunks_def) else TOTAL
    chunks.append({"lines": [[{"w": WO[i][0].upper(), "t": WO[i][1], "k": i in KEY} for i in ln] for ln in lines],
                   "t0": t0, "t1": round(t1, 3)})

# camera segments (output time)
cam = []
for k, (sid, s, o, d) in enumerate(starts):
    cam.append({"id": sid, "t": o, "d": d})

js_data = json.dumps({"chunks": chunks, "cam": cam, "total": TOTAL}, ensure_ascii=False)

w = {n: o for n, o in [(f"{n}{i}", o) for i, (n, o) in enumerate(WO)]}
wt = lambda i: WO[i][1]

sfx = []  # (file, start, volume, duration)


def add(f, t, v, d):
    sfx.append((f, round(t, 3), v, d))


DUR = {"impact": 0.9, "whoosh": 0.4, "whoosh-down": 0.35, "pop": 0.14, "tick": 0.05, "ding": 0.5, "missed": 0.7,
       "chime": 1.1, "tock": 0.09}
add("impact", 0.0, 0.7, DUR["impact"])
add("whoosh-down", 2.62, 0.3, DUR["whoosh-down"])
add("whoosh", 2.78, 0.28, DUR["whoosh"])
add("pop", 2.86, 0.5, DUR["pop"])
add("missed", 3.5, 0.5, DUR["missed"])
add("impact", wt(10) - 0.02, 0.4, DUR["impact"])
add("whoosh", 3.84, 0.28, DUR["whoosh"])
add("pop", 3.97, 0.5, DUR["pop"])
add("pop", wt(20), 0.55, DUR["pop"])
add("impact", wt(20) - 0.02, 0.4, DUR["impact"])
add("whoosh", 5.98, 0.3, DUR["whoosh"])
add("pop", wt(22), 0.5, DUR["pop"])
add("pop", wt(24), 0.5, DUR["pop"])
add("whoosh", 8.7, 0.28, DUR["whoosh"])
add("pop", 9.0, 0.5, DUR["pop"])
add("pop", 9.95, 0.5, DUR["pop"])
add("impact", wt(38) - 0.02, 0.4, DUR["impact"])
add("whoosh", 11.62, 0.28, DUR["whoosh"])
add("ding", wt(42) + 0.0, 0.45, DUR["ding"])
add("ding", wt(44) + 0.02, 0.45, DUR["ding"])
add("ding", wt(48) + 0.02, 0.45, DUR["ding"])
add("whoosh", 15.02, 0.28, DUR["whoosh"])
for i, tt in enumerate((15.3, 15.6, 15.9)):
    add("tock", tt, 0.4, DUR["tock"])
add("whoosh-down", 17.2, 0.25, DUR["whoosh-down"])
add("impact", 18.77, 0.5, DUR["impact"])
add("chime", wt(61) + 0.0, 0.55, DUR["chime"])
add("impact", wt(68) - 0.02, 0.45, DUR["impact"])

audio_tags = []
busy = {}  # track index -> end time of the last clip placed on it
for n, (f, t0, v, d) in enumerate(sfx):
    tr = next(i for i in range(11, 40) if busy.get(i, -1) <= t0)
    busy[tr] = t0 + d
    audio_tags.append(
        f'      <audio id="sfx-{n + 1}" src="assets/audio/{f}.wav" data-start="{t0}" data-duration="{d}" '
        f'data-track-index="{tr}" data-volume="{v}"></audio>')

tpl = open(os.path.join(HERE, "template.html")).read()
html = (tpl.replace("%%DATA%%", js_data)
        .replace("%%TOTAL%%", f"{TOTAL:.4f}")
        .replace("%%AUDIO%%", "\n".join(audio_tags))
        .replace("%%W_NOBODY%%", f"{wt(10):.3f}").replace("%%W_CUSTOMER%%", f"{wt(20):.3f}")
        .replace("%%W_VOICE%%", f"{wt(24):.3f}").replace("%%W_INSTANT%%", f"{wt(38):.3f}")
        .replace("%%W_QUALIFY%%", f"{wt(42):.3f}").replace("%%W_BOOK%%", f"{wt(44):.3f}")
        .replace("%%W_QUESTIONS%%", f"{wt(48):.3f}").replace("%%W_COMMENT%%", f"{wt(61):.3f}")
        .replace("%%W_DEMO%%", f"{wt(68):.3f}").replace("%%W_UP%%", f"{wt(12):.3f}"))
open(os.path.join(ROOT, "index.html"), "w").write(html)
print("total", TOTAL, "chunks", len(chunks), "sfx", len(sfx))
for sid, s, o, d in starts:
    print(f"{sid:8s} out {o:6.3f}-{o + d:6.3f}")
print({k: wt(i) for k, i in dict(nobody=10, up=12, customer=20, voice=24, instantly=38, qualify=42, book=44,
                                  questions=48, comment=61, demo=68).items()})
