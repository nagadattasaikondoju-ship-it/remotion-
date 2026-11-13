# Cue sheet for the Real SFX skill, computed from out/timeline.json so a re-cut moves every sound with its picture.
#   python3 sfx_cues.py -> sfx_cues.json (+ sfx_map.json: cue kind -> library sound ids)
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, "out", "timeline.json")))
seg = {s["id"]: s for s in TL["segments"]}; S = lambda i: seg[i]["start"]
T1 = lambda x: S("frz") + 0.60 + (x - 1.85); T2 = lambda x: S("t2a") + (x - 0.60); T3 = lambda x: S("t3") + (x - 0.55)
T7 = lambda x: S("t7a") + (x - 0.45); T8 = lambda x: S("t8") + (x - 0.75); T9 = lambda x: S("t9") + (x - 0.70)
MAP = {"glitch": {"ids": [62], "role": "glitch"}, "lowhit": {"ids": [29], "role": "hit"}, "scratch": {"ids": [64], "role": "hit"},
       "beep": {"ids": [63], "role": "ui"}, "swoosh": {"ids": [56], "role": "whoosh"}, "swoosh2": {"ids": [53], "role": "whoosh"},
       "fastwhoosh": {"ids": [50], "role": "whoosh"}, "softwhoosh": {"ids": [57], "role": "whoosh"}, "tick": {"ids": [24], "role": "ui"},
       "punch": {"ids": [55], "role": "hit"}, "pops": {"ids": [10], "role": "ui"}, "impact": {"ids": [28], "role": "hit"},
       "bigimpact": {"ids": [32], "role": "hit"}, "chime": {"ids": [61], "role": "ui"},
       "key1": {"ids": [33], "role": "ui"}, "key2": {"ids": [34], "role": "ui"}, "key3": {"ids": [37], "role": "ui"}}
APPROVE = next(w["t"] for c in TL["captions"] if c["text"].startswith("So you can deploy") for w in c["words"] if w["w"] == "deploy")
td = T1(4.40); spd = (790 - 80) / (td - (S("t1b") + 0.05))   # overlay.html sECG: trace from x0 = 80, flatlines at x = 790
beats = [S("t1b") + 0.05 + (x - 80) / spd for x in (213, 443, 673)]
C = [
 (S("co1") + 0.30, "glitch", 0.50, "cold open: the deployment crashes, punch-in on the developer"),
 (S("co2"), "lowhit", 0.55, "cut to black: He had no idea what was coming."),
 (S("a1") + 0.10, "pops", 0.30, "label: THE DEVELOPER"), (S("a1") + 0.28, "pops", 0.28, "label: THE CLIENT"),
 (APPROVE, "chime", 0.36, "DEMO APPROVED (on 'deploy')"),
 (S("lat") - 0.06, "softwhoosh", 0.34, "cut to the card: 3 weeks later"),
 *[(S("lat") + 0.04 + 0.45 * k / 13, f"key{k % 3 + 1}", 0.30, "typing: 3 weeks later") for k in (0, 2, 9)],
 (S("b"), "lowhit", 0.55, "back from the card: Deployment failed"), (S("b") + 0.04, "glitch", 0.40, "the red toast + glitch"),
 (S("b") + 0.42, "glitch", 0.42, "the crash: quick zoom on the developer"),
 (S("c1") + 0.20, "pops", 0.26, "Calling Manager chip"),
 (S("frz"), "scratch", 0.80, "freeze-frame: record scratch (the handoff)"),
 *[(b, "beep", 0.32, "heart-monitor beep on the ECG blip") for b in beats],
 (td, "lowhit", 0.38, "'dies': the trace flatlines, the beeping stops"),
 (S("t1c") + 0.05, "swoosh", 0.40, "split screen: the DEMO panel slides up"),
 (T1(6.90), "tick", 0.50, "tick: data clean"), (T1(7.72), "tick", 0.50, "tick: one user"), (T1(8.74), "tick", 0.50, "tick: Wi-Fi perfect"),
 (S("t2a") - 0.27, "glitch", 0.42, "the demo panel glitches apart"),
 (S("t2a"), "punch", 0.48, "THE REAL WORLD title on the night-traffic b-roll"),
 (S("t2b"), "fastwhoosh", 0.40, "cut: hundreds of people"), (S("t2b") + 0.15, "pops", 0.30, "avatars multiplying"),
 (S("t2c"), "swoosh2", 0.40, "cut: messy data"), (S("t2c") + 0.10, "glitch", 0.28, "bad cells"),
 (S("t2d"), "swoosh", 0.40, "cut: phone on a bad network"),
 (T2(5.22), "beep", 0.22, "signal drops"), (T2(5.50), "beep", 0.22, "signal drops again"),
 (T2(6.26), "glitch", 0.32, "Request timed out"),
 (S("t3"), "softwhoosh", 0.30, "back to Tarun, one steady shot"), (T3(3.20), "chime", 0.30, "the OneLoop badge appears"),
 (S("t4b"), "impact", 0.60, "PROOF 1: Nirvaha, live on Google Play"), (S("t4b") + 0.02, "fastwhoosh", 0.35, "proof card slides in"),
 (S("t5"), "impact", 0.55, "PROOF 2: logistics"), (S("t6"), "impact", 0.55, "PROOF 3: LN Sports Arena"),
 (S("t7b"), "bigimpact", 0.70, "copper slam"), (T7(2.14) + 0.12, "swoosh2", 0.45, "DEMOS gets struck through"),
 (T7(2.44) - 0.04, "fastwhoosh", 0.40, "copper wipes away, black: we build software"), (T7(3.82), "punch", 0.55, "WORKS."),
 (T9(1.38) - 0.05, "lowhit", 0.75, "bass hit: the OneLoop logo lands"),
 *[(T8(0.86) + k * 0.09, f"key{k % 3 + 1}", 0.45, f"typing '{'BUILD'[k]}' into the comment box") for k in range(5)],
 (T8(1.36), "impact", 0.55, "BUILD lands"), (T8(1.50), "chime", 0.32, "comment posted"),
]
json.dump([{"t": round(t, 3), "type": k, "g": g, "note": n} for t, k, g, n in sorted(C)], open(os.path.join(HERE, "sfx_cues.json"), "w"), indent=1)
json.dump(MAP, open(os.path.join(HERE, "sfx_map.json"), "w"), indent=1)
print(f"{len(C)} cues -> sfx_cues.json")
