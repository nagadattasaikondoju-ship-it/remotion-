# One Loop x pet client: "meet the team". One table drives picture, text, music and sound cues.
#   python3 edit.py -> out/edit.json
# 115 BPM, 12 bars (25.04 s). Every cut sits on a downbeat of the in-house score (music.py), so the edit and the music can't drift.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("SRC_DIR", "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/drv2")
FPS, BPM = 60, 115
BEAT = 60 / BPM; BAR = 4 * BEAT; BARS = 12; DUR = round(BARS * BAR, 4)

# (start in beats, length in beats, source, in-point s, grade, text kind, text, note)
#   source: "k:" kennel original (Sony, stored sideways: turned upright, full 1080x1920 frame, 1:1 pixels)
#           "o:" One Loop B-roll original (same camera); None = black card
SHOTS = [
 (0,  4, "o:MVI_0729", 2.00, "warm", "hook", "we just signed\na new client", "One Loop: handshake with the client on the cafe sofa"),
 (4,  4, "k:MVI_0814", 0.85, "warm", "big",  "meet the team", "Mastiff puppy grins into the lens"),
 (8,  4, "k:MVI_0771", 0.85, "warm", "role", "the boss", "Tibetan Mastiff stands at the mesh, waves a paw"),
 (12, 4, "k:MVI_0811", 6.95, "warm", "role", "head of security", "black Cane Corso comes up to the lens, tongue out"),
 (16, 4, "k:MVI_0777", 4.60, "warm", "role", "the interns", "one Saint Bernard hops onto the other"),
 (20, 4, "k:MVI_0815", 3.85, "warm", "role", "lunch break", "Mastiff puppy eating from a big steel bowl"),
 (24, 4, "k:MVI_0826", 12.95, "warm", "role", "performance bonus", "Shih Tzus crowd the railing for treats"),
 (28, 4, "k:MVI_0808", 0.50, "warm", "role", "brand ambassador", "Shih Tzu lying like royalty, looking at the lens"),
 # the burst: one beat each, everyone else in the building
 (32, 1, "k:MVI_0770", 7.90, "warm", "burst", "honestly?", "two Saint Bernards standing up side by side"),
 (33, 1, "k:MVI_0775", 0.05, "warm", "burst", "honestly?", "two Shepherds standing up together"),
 (34, 1, "k:MVI_0779", 15.35, "warm", "burst", "honestly?", "Saint Bernard stands up at the mesh"),
 (35, 1, "k:MVI_0800", 2.05, "warm_in", "burst", "honestly?", "Maltese, face cradled in a hand"),
 (36, 1, "k:MVI_0778", 19.05, "warm", "burst", "best client ever.", "cream fluffy dog stands up on the mesh"),
 (37, 1, "k:MVI_0805", 0.20, "warm", "burst", "best client ever.", "Shih Tzu at the foot of the stairs"),
 (38, 1, "k:MVI_0832", 7.35, "warm", "burst", "best client ever.", "a hand pets the Mastiff puppy on red soil"),
 (39, 1, "k:MVI_0794", 7.00, "warm_in", "burst", "best client ever.", "Maltese trots up and looks up"),
 (40, 4, "o:MVI_0727", 0.00, "warm", "hook", "now let's make\nthem famous", "One Loop: the One Loop site on the laptop"),
 (44, 4, None, 0, None, "end", "pet brands,\nyou're next.", "One Loop logo on black"),
]
# role labels get a soft pop; the logo gets a chime (sound pipeline, sfx_cues.py)

def path(src):
    kind, name = src.split(":")
    return {"k": f"{SRC}/orig/{name}.mp4", "o": f"{SRC}/ol/{name}.mp4"}[kind]

def main():
    shots = []
    for b0, nb, src, i, grade, kind, text, note in SHOTS:
        a, b = b0 * BEAT, (b0 + nb) * BEAT
        shots.append({"start": round(a, 4), "dur": round(b - a, 4), "f0": round(a * FPS), "f1": round(b * FPS), "src": path(src) if src else None,
                      "in": i, "grade": grade, "kind": kind, "text": text, "note": note})
    out = {"fps": FPS, "bpm": BPM, "beat": BEAT, "bar": BAR, "bars": BARS, "duration": DUR, "frames": round(DUR * FPS), "shots": shots}
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "out", "edit.json"), "w"), indent=1, ensure_ascii=False)
    for s in shots: print(f"{s['start']:6.2f} {s['dur']:5.2f} {os.path.basename(s['src'] or '-'):13s} {s['kind']:6s} {s['text']!r:28} {s['note']}")
    print(f"{DUR:.3f} s, {out['frames']} frames")

if __name__ == "__main__": main()
