"""Sound cues for the 'resolution' reel (real recordings from the house library; ids in tools/real-sfx.index.json)."""
import json
C = [(2.2, "sparkle", .4, "gums clean again"), (3.0, "swipe", .42, "whip pan"), (4.0, "drill", .28, "the implant screws in"),
     (5.28, "seat", .4, "the crown seats"), (5.35, "sparkle", .35, "gap filled"), (6.2, "swipe", .42, "whip pan"),
     (6.95, "softwhoosh", .35, "the cleaning sweep"), (7.95, "sparkle", .4, "white again"), (8.2, "whoosh", .42, "the page sweeps in"),
     (8.5, "pop", .38, "Dr. Sri Sushma"), (8.82, "slam", .42, "'is' slams in"),
     (9.3, "pop", .28, "unleashing"), (9.55, "pop", .28, "confident"), (9.8, "pop", .28, "smiles"), (10.05, "pop", .26, "across"), (10.25, "pop", .3, "Hyderabad."),
     (10.6, "whoosh", .4, "push-in and the blue sweep"),
     (11.17, "whoosh", .45, "the clinic card pops up"), (11.47, "pop", .5, "the logo lands"), (12.27, "chime", .45, "BOOK AN APPOINTMENT lands")]
json.dump([{"t": t, "type": k, "g": g, "note": n} for t, k, g, n in sorted(C)], open("sfx_cues.json", "w"), indent=1)
json.dump({"sparkle": {"ids": [68], "role": "chime"}, "swipe": {"ids": [53], "role": "whoosh"}, "drill": {"ids": [69], "role": "misc"}, "seat": {"ids": [21], "role": "click"},
           "softwhoosh": {"ids": [57], "role": "whoosh"}, "whoosh": {"ids": [56], "role": "whoosh"}, "pop": {"ids": [65], "role": "ui"},
           "slam": {"ids": [24], "role": "hit"}, "chime": {"ids": [61], "role": "ui"}}, open("sfx_map.json", "w"), indent=1)
