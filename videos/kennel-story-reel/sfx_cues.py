# One real sound, on the only "moment" the picture makes: the warm light-leak flash between "loving you.." and "we get busy,".
# Everything else is carried by the reference voiceover and its music, as in the reference.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
C = [(17.06, "softwhoosh", 0.5, "light-leak flash: the turn from love to busy life")]
json.dump([{"t": t, "type": k, "g": g, "note": n} for t, k, g, n in C], open(os.path.join(HERE, "sfx_cues.json"), "w"), indent=1)
json.dump({"softwhoosh": {"ids": [57], "role": "whoosh"}}, open(os.path.join(HERE, "sfx_map.json"), "w"), indent=1)
print(len(C), "cue")
