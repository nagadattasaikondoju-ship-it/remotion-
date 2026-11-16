# v2 end card sound: three real recordings, only where the card does something (house rule: few sounds, moments that matter).
# The cartoon keeps its own audio; the card starts at 6.0333 s (frame 181). Library ids from tools/real-sfx.index.json (CC0).
#   python3 sfx_cues.py -> sfx_cues.json + sfx_map.json
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
CARD = 181 / 30
MAP = {"whoosh": {"ids": [56], "role": "whoosh"}, "pop": {"ids": [65], "role": "ui"}, "chime": {"ids": [61], "role": "ui"}}
# whoosh-1 (56): earshot's best "quick soft swoosh" and a real recording; 65 = the best single pop cut from 3-popping-pops (10)
C = [(CARD + 0.06, "whoosh", 0.5, "the card pops up over the cartoon (fastest frames 0-4)"),
     (CARD + 0.36, "pop", 0.55, "the logo lands (scale passes 100 %)"),
     (CARD + 1.17, "chime", 0.5, "the BOOK AN APPOINTMENT button lands")]
json.dump([{"t": round(t, 3), "type": k, "g": g, "note": n} for t, k, g, n in C], open(os.path.join(HERE, "sfx_cues.json"), "w"), indent=1)
json.dump(MAP, open(os.path.join(HERE, "sfx_map.json"), "w"), indent=1)
print(len(C), "cues")
