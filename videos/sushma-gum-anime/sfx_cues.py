# Cue sheet for "Pink in the sink" (house sound playbook: whoosh = movement, texture = event, riser + hit = build).
# Every time comes from the voice timeline (timeline.json), the same numbers anime.html animates to. Real recordings only
# (tools/real-sfx.index.json, CC0): 66 drain swirl, 67 ice crack (tartar), 68 gleam sparkle, 69 electric-toothbrush hum
# (the scaler), 70 mouth-harp boing (the wobble), 13 real toothbrush scrub, 53/56/57 whooshes, 65 single pop,
# 55 punch-with-whoosh, 28 cinematic impact, 29 low impact, 43 short riser, 44 bright riser, 61 chime. No music under graphics.
#   python3 sfx_cues.py -> sfx_cues.json + sfx_map.json + CUES.md
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, "timeline.json")))
L = TL["lines"]
def w(li, rx):
    for x in L[li - 1]["words"]:
        if re.search(rx, x["w"]): return x["s"]
    return L[li - 1]["start"]
S = lambda i: L[i - 1]["start"]
T2, T7, T8, TEND = 2.85, S(7), S(8), 33.9
MAP = {"drain": {"ids": [66], "role": "water"}, "crack": {"ids": [67], "role": "hit"}, "sparkle": {"ids": [68], "role": "chime"},
       "scaler": {"ids": [69], "role": "misc"}, "boing": {"ids": [70], "role": "misc"}, "brush": {"ids": [13], "role": "foley"},
       "whoosh": {"ids": [56], "role": "whoosh"}, "swipe": {"ids": [53], "role": "whoosh"}, "softwhoosh": {"ids": [57], "role": "whoosh"},
       "pop": {"ids": [65], "role": "ui"}, "punch": {"ids": [55], "role": "hit"}, "impact": {"ids": [28], "role": "hit"},
       "lowhit": {"ids": [29], "role": "hit"}, "riser": {"ids": [43], "role": "riser"}, "brightriser": {"ids": [44], "role": "riser"},
       "chime": {"ids": [61], "role": "ui"}}
C = [
 # hook: the sink
 (0.0, "drain", .5, 0, "pink water swirling down the drain (diegetic bed under the hook)"),
 (w(1, r"^Pink"), "pop", .5, 0, "PINK IN THE SINK pops in"),
 (w(1, r"^sink"), "punch", .55, 0, "impact frames on 'sink' (the one impact of the hook)"),
 (w(1, r"^every"), "pop", .4, 0, "EVERY TIME line pops in"),
 (T2 - .05, "swipe", .5, 0, "whip into the story (white flash)"),
 # story
 (S(3) - .05, "brush", .55, 0, "giant toothbrush scrubs across Moti (real brushing)"),
 (w(3, r"blood") - .3, "softwhoosh", .4, 0, "camera pushes in to the gum line"),
 (w(3, r"blood"), "pop", .55, 0, "'!' pops over Moti, first drop of blood"),
 (w(4, r"normal") - .3, "pop", .45, 0, "IT'S NORMAL~ bubble"),
 (w(4, r"normal") - .05, "pop", .4, 0, "CHILL~ bubble"),
 (w(5, r"^tartar") - 2.0, "riser", .5, 2.0, "riser into the trouble (ends as the plaque hardens)"),
 (w(5, r"^tartar"), "crack", .45, 0, "plaque hardens into tartar"),
 (w(5, r"^tartar"), "lowhit", .45, 0, "hit under the first riser"),
 (w(5, r"^Red"), "punch", .5, 0, "RED! stamp (the impact of this scene)"),
 (w(5, r"Swollen"), "pop", .5, 0, "SWOLLEN! stamp"),
 (w(5, r"^Bleeding"), "pop", .5, 0, "BLEEDING! stamp"),
 (w(6, r"pulling") - .2, "softwhoosh", .4, 0, "gums pull back, camera pushes in"),
 (w(6, r"wobble"), "boing", .6, 0, "Moti wobbles (impact frames, WOBBLE?! stamp)"),
 (T7 - 1.6, "riser", .55, 1.6, "build to the rescue (ends on the hero flash)"),
 (T7, "impact", .5, 0, "hero entrance: impact frames, golden light"),
 (T7 + .05, "sparkle", .5, 0, "golden sparkle as the clinic pops up"),
 (T7 + .3, "pop", .5, 0, "clinic logo badge pops on the roof"),
 (w(7, r"dental") - .2, "pop", .5, 0, "DR. SRI SUSHMA plate lands (on screen only)"),
 (w(7, r"clinic") + .25, "pop", .4, 0, "GUM SPECIALIST · PERIODONTIST pill lands"),
 (T8 + .25, "scaler", .45, 0, "ultrasonic scaler sweeps the gum line (diegetic hum)"),
 (T8 + .6, "softwhoosh", .35, 0, "hero badge flies out"),
 (T8 + 1.0, "crack", .4, 0, "first tartar rocks shatter"),
 (T8 + 2.2, "crack", .35, 0, "last tartar rocks shatter"),
 (w(8, r"strong") - .1, "sparkle", .5, 0, "Moti flexes, sparkles, sun comes out (conclusion)"),
 (w(9, r"Don't") - .06, "pop", .5, 0, "DON'T WAIT FOR stamp"),
 (w(9, r"wobble") - .04, "boing", .45, 0, "THE WOBBLE! stamp (callback to the wobble)"),
 (TEND - 1.5, "brightriser", .4, 1.5, "lift into the end card"),
 # end card (Dr. Sri Sushma details), same three cues as the clinic's other reels
 (TEND + .06, "whoosh", .5, 0, "the card pops up out of the white flash"),
 (TEND + .36, "pop", .55, 0, "the logo lands"),
 (TEND + 1.17, "chime", .5, 0, "BOOK AN APPOINTMENT button lands"),
]
cues = [dict(t=round(t, 3), type=k, g=g, note=n, **({"len": ln} if ln else {})) for t, k, g, ln, n in C]
json.dump(cues, open(os.path.join(HERE, "sfx_cues.json"), "w"), indent=1)
json.dump(MAP, open(os.path.join(HERE, "sfx_map.json"), "w"), indent=1)
with open(os.path.join(HERE, "CUES.md"), "w") as f:
    f.write("# Cue sheet\n\n| Time | Family | Sound (library id) | Moment |\n|---|---|---|---|\n")
    fam = lambda k: "riser" if "riser" in k else ("hit" if k in ("punch", "impact", "lowhit", "crack") else ("whoosh" if "whoosh" in k or k == "swipe" else "texture"))
    for c in sorted(cues, key=lambda c: c["t"]):
        m = int(c["t"] // 60); f.write(f"| {m:02d}:{c['t'] - 60 * m:05.2f} | {fam(c['type'])} | {c['type']} ({MAP[c['type']]['ids'][0]}) | {c['note']} |\n")
print(len(cues), "cues")
