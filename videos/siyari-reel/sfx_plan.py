"""Sound cues for the Siyari ring-chain reel (real recordings from the house library; ids in tools/real-sfx.index.json).
Few sounds, only on moments that matter: shimmer under the rings, a riser that ends on each cut, the diamond landing on the swan, the sheen."""
import json
C = [(0.05, "shimmer", .2, "rings + velvet open"), (1.6, "sparkle", .2, "a centre stone glints"), (3.4, "sparkle", .2, "a centre stone glints"),
     (2.6, "riser", .26, "riser ends on the cut to the logo (4.6)"),
     (4.72, "whoosh", .4, "the diamond falls (peak on the fastest frames)"), (5.22, "chime", .42, "the diamond lands as the swan's crown"), (5.24, "sparkle", .32, "crown flash"),
     (5.3, "softwhoosh", .24, "the swan draws itself"), (6.0, "tick", .2, "SIYARI letters open"), (7.4, "sparkle", .28, "sheen across the logo"),
     (8.2, "swipe", .34, "cut back to the rings"), (8.3, "shimmer", .17, "rings again"), (10.2, "sparkle", .2, "a centre stone glints"),
     (10.2, "riser", .24, "riser ends on the cut to the end card (12.2)"),
     (12.32, "whoosh", .4, "the diamond falls"), (12.82, "chime", .42, "crown lands"), (12.84, "sparkle", .32, "crown flash"), (12.9, "softwhoosh", .22, "swan draws"),
     (13.6, "tick", .2, "letters open"), (14.57, "pop", .26, "DM CUSTOM pill"), (15.0, "sparkle", .28, "final sheen")]
json.dump([{"t": t, "type": k, "g": g, "note": n} for t, k, g, n in sorted(C)], open("sfx_cues.json", "w"), indent=1)
json.dump({"shimmer": {"ids": [60], "role": "chime"}, "sparkle": {"ids": [68], "role": "chime"}, "riser": {"ids": [43], "role": "riser"},
           "whoosh": {"ids": [56], "role": "whoosh"}, "softwhoosh": {"ids": [57], "role": "whoosh"}, "swipe": {"ids": [53], "role": "whoosh"},
           "chime": {"ids": [61], "role": "ui"}, "tick": {"ids": [58], "role": "ui"}, "pop": {"ids": [65], "role": "ui"}}, open("sfx_map.json", "w"), indent=1)
