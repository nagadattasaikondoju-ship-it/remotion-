# A few real sounds under the reference audio, only where the picture does something: emoji stickers pop, sparkles shimmer.
#   python3 sfx_cues.py -> sfx_cues.json + sfx_map.json (cue kind -> Real SFX library ids)
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, "out", "edit.json"))); S = {s["id"]: s["start"] for s in E["shots"]}
MAP = {"pop": {"ids": [10], "role": "ui"}, "sparkle": {"ids": [59], "role": "ui"}}
C = [(S["s2"] + 0.07, "pop", 0.20, "💗 sticker pops in (My name is bobbattu)"),
     (S["s3"] + 0.07, "sparkle", 0.22, "✨ shimmer (ali billi bobbattu)"),
     (S["s4"] + 0.07, "pop", 0.18, "🥰 sticker pops in (andhala bobbattu)"),
     (S["s5"] + 0.07, "pop", 0.18, "💗 sticker pops in (maa nethi bobbattu)"),
     (S["s6"] + 0.07, "sparkle", 0.28, "✨✨ sparkles (Lakshmi Ganapathi bobbattu)")]
json.dump([{"t": round(t, 3), "type": k, "g": g, "note": n} for t, k, g, n in C], open(os.path.join(HERE, "sfx_cues.json"), "w"), indent=1, ensure_ascii=False)
json.dump(MAP, open(os.path.join(HERE, "sfx_map.json"), "w"), indent=1)
print(len(C), "cues")
