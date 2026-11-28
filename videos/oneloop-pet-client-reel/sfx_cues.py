# Few real sounds, only where the picture does something (house rule): a soft pop as each "meet the team" role label lands,
# and a chime as the One Loop logo appears. Library ids from tools/real-sfx.index.json (real recordings, CC0).
#   python3 sfx_cues.py -> sfx_cues.json + sfx_map.json
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, "out", "edit.json")))
MAP = {"pop": {"ids": [10], "role": "ui"}, "chime": {"ids": [61], "role": "ui"}}
C = [(s["start"] + 0.14, "pop", 0.2, f"label lands: {s['text']}") for s in E["shots"] if s["kind"] == "role"]
C += [(s["start"] + 0.05, "chime", 0.5, "One Loop logo") for s in E["shots"] if s["kind"] == "end"]
json.dump([{"t": round(t, 3), "type": k, "g": g, "note": n} for t, k, g, n in C], open(os.path.join(HERE, "sfx_cues.json"), "w"), indent=1)
json.dump(MAP, open(os.path.join(HERE, "sfx_map.json"), "w"), indent=1)
print(len(C), "cues")
