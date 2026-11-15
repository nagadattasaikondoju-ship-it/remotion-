# "bobbattu" dog reel: one table drives the picture (base.py), the captions (overlay.html) and the sound cues.
#   python3 edit.py -> out/edit.json
# Timing = the reference reel's own cuts (measured on its frames), so every caption lands on its spoken line:
#   reference cuts at 0.233 / 2.133 / 3.967 / 5.567 / 7.367 / 9.200 s, loop end 11.067 s; the audio here starts at 0.233.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("SRC_DIR", "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/drv2")
FPS, DUR = 60, 11.0167          # 661 frames; the cut reference audio is 11.018 s (assets/ref_audio.wav)
CUTS = [0.0, 1.900, 3.733, 5.333, 7.133, 8.967, DUR]

# (id, source, in-point s, rotate?, zoom keys [(t, z)], anchor (x, y) in the upright frame, grade, caption, emoji, note)
#   "up/…" sources are AI-upscaled crops (tools/upscale_realesr.py), already upright and 1080x1920.
SHOTS = [
 ("s1", "up/s1_ref.mp4", 0.0, False, [(0, 1.00), (1.9, 1.03)], (540, 700), "ref",
  "MY NAME IS MAXIMUS DECIMUS MERIDIUS", None, "the hook: the reference reel's own Doberman shot (0.233-2.133 s), AI-upscaled to 1080x1920; its caption and the Instagram UI are covered and the caption redrawn"),
 ("s2", "orig/MVI_0814.mp4", 0.75, True, [(0, 1.02), (1.833, 1.08)], (440, 950), "cute",
  "My name is bobbattu", "💗", "MVI_0814: Mastiff puppy comes up to the camera and smiles"),
 ("s3", "orig/MVI_0800.mp4", 3.20, True, [(0, 1.00), (1.6, 1.05)], (560, 700), "cute",
  "ali billi bobbattu", "✨", "MVI_0800: Maltese, chin cradled in a hand, tips its head up"),
 ("s4", "up/s4_0805.mp4", 0.00, False, [(0, 1.00), (1.8, 1.05)], (520, 1216), "cute",
  "andhala bobbattu", "🥰", "MVI_0805: Shih Tzu at the stairs looks away, then back at the camera; crop 1.6x"),
 ("s5", "orig/MVI_0794.mp4", 6.95, True, [(0, 1.14), (1.833, 1.22)], (530, 1000), "cute",
  "maa nethi bobbattu", "💗", "MVI_0794: Maltese trots up and looks straight up at the camera"),
 ("s6", "orig/MVI_0808.mp4", 0.00, True, [(0, 1.04), (2.05, 1.10)], (490, 870), "cute",
  "Lakshmi Ganapathi\nbobbattu", "✨", "MVI_0808: Shih Tzu lying like royalty, looking at the camera"),
]

# fallback for the two zoomed shots: the same crop from the original, Lanczos-scaled (PREVIEW=1, or until the AI upscale exists)
FALLBACK = {"s4": ("orig/MVI_0805.mp4", 0.00, "crop=676:1202:100:640")}

SPEED = {}   # per-shot speed, e.g. {"s2": 0.8} for slow motion (the originals are 59.94 fps)

def main():
    out = {"fps": FPS, "duration": DUR, "shots": []}
    for (sid, src, i, rot, zk, anc, grade, cap, emo, note), a, b in zip(SHOTS, CUTS, CUTS[1:]):
        pre = ""
        if sid in FALLBACK and (os.environ.get("PREVIEW") or not os.path.exists(os.path.join(SRC, src))):
            src, i, pre = FALLBACK[sid]; rot = True
        out["shots"].append({"id": sid, "src": os.path.join(SRC, src), "in": i, "rotate": rot, "pre": pre, "start": a, "dur": round(b - a, 4),
                             "zoom": zk, "anchor": anc, "grade": grade, "caption": cap, "emoji": emo, "note": note,
                             "speed": SPEED.get(sid, 1.0)})
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "out", "edit.json"), "w"), indent=1, ensure_ascii=False)
    for s in out["shots"]: print(f"{s['start']:6.3f} {s['dur']:5.3f} {s['id']} {s['caption']!r:40} {s['note']}")

if __name__ == "__main__": main()
