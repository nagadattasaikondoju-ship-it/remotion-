"""Edit decision list for the One Loop "client #1" reel (shared by build_cut.py, build_audio.py, build_html.py).

Dialogue segments are audio ranges on the cleaned (DeepFilterNet) tracks; every picture cut and
overlay is anchored to a word time inside one of those segments, so retiming a segment moves
everything attached to it.
"""
import os

FPS = 30
UP = "/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e"
SCR = "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad"
BROLL = os.path.join(SCR, "broll")
CLEAN = os.path.join(SCR, "ol", "audio")  # *_dn.wav from DeepFilterNet3

# camera sources: path, rotate (Canon bodies were shot sideways), grade, denoise
SRC = {
    "0647": (f"{UP}/b6b8081c-MVI_0647_1.mp4", True, "day", "hqdn3d=1.2:1.2:5:5"),
    "0658": (f"{UP}/e4ed3df4-MVI_0658_1.mp4", True, "dusk", "hqdn3d=2.5:2:8:7"),
    "0662": (f"{UP}/ec9099a2-MVI_0662_1_1.mp4", True, "night", "hqdn3d=3:2.5:8:7"),
    "VID": (f"{UP}/02474035-VID_20261016_182556442_1.mp4", False, "phone", "hqdn3d=3:2.5:6:5"),
}
for n in ("0422", "0425", "0431", "0432", "0434", "0436", "0446", "0447", "0457", "0458", "0467"):
    SRC[n] = (f"{BROLL}/MVI_{n}.MP4", True, "broll", "hqdn3d=1:1:4:4")

# dialogue: (audio track, in, out, picture source, picture offset = video time - audio time)
SEGS = [
    ("0647", 0.86, 3.84, "0647", 0.0),    # 0 Our first client agreed to pay us ₹10,000 for a website,
    ("0647", 4.46, 8.20, "0647", 0.0),    # 1 and we had just started One Loop, and that money mattered a lot to us.
    ("AUD", 0.00, 4.36, "0658", 1.91),    # 2 We went to every door in Hyderabad, from small-scale … enterprises.
    ("AUD", 4.52, 6.92, "0658", 1.91),    # 3 We pitched our idea on how to develop their business and
    ("AUD", 7.22, 8.90, "0658", 1.91),    # 4 one client [said yes / chose us] for a website.
    ("AUD", 9.32, 10.42, "0658", 1.91),   # 5 We built the demo and
    ("AUD", 10.70, 12.10, "0658", 1.91),  # 6 when we were ready to publish it.
    ("0662", 1.44, 5.40, "0662", 0.0),    # 7 And then the payments slowed down. At the beginning he paid us ₹1,500,
    ("0662", 6.10, 7.45, "0662", 0.0),    # 8 then nothing happened.
    ("0662", 7.60, 12.50, "0662", 0.0),   # 9 So we tried calling him … something or the other.
    ("0662", 12.62, 14.30, "0662", 0.0),  # 10 So what did we do next?
    ("VID", 0.78, 3.06, "VID", 0.0),      # 11 You would expect us to publish it anyway,
    ("VID", 3.44, 7.00, "VID", 0.0),      # 12 or to walk away, but we did neither. We wanted to handle it professionally,
    ("VID", 7.04, 9.70, "VID", 0.0),      # 13 but that was not the same case from the client's side. (+ whip start)
    ("VID", 10.00, 12.30, "VID", 0.0),    # 14 (whip end) That was about our first client,
    ("VID", 12.62, 15.04, "VID", 0.0),    # 15 and thankfully not every client is like that.
    ("VID", 15.10, 18.62, "VID", 0.0),    # 16 And in part 2, we'll talk about some of the best clients we've worked with.
]

# frame-quantised segment lengths and timeline starts
LEN = [round((b - a) * FPS) for _, a, b, _, _ in SEGS]
START = [sum(LEN[:i]) for i in range(len(SEGS))]
TOTAL_F = sum(LEN)
TOTAL = TOTAL_F / FPS


def F(seg, t):
    """timeline frame of audio time t inside segment seg"""
    return START[seg] + round((t - SEGS[seg][1]) * FPS)


def T(seg, t):
    return F(seg, t) / FPS


# picture track: each shot runs from its anchor to the next shot's anchor.
#   A-roll: ("A", seg, t, zoom | (z0, z1))   zoom on the speaker, face-centred
#   B-roll: ("B", seg, t, src, src_in, zoom, (cx, cy) or None)
SHOTS = [
    ("A", 0, 0.86, 1.15),
    ("A", 0, 2.86, 1.24),                          # punch-in on "₹10,000"
    ("A", 1, 5.88, 1.34),                          # closer crop after the One Loop match cut
    ("A", 2, 0.00, 1.38),                          # R: "We went to every door in Hyderabad,"
    ("B", 2, 1.80, "0436", 2.2, 1.0, None),        # feet: "from small-scale"
    ("B", 2, 2.62, "0458", 1.0, 1.0, None),        # street shops: "local business"
    ("B", 2, 3.30, "0457", 31.0, 1.0, None),       # large building: "to large-scale enterprises"
    ("B", 3, 4.52, "0447", 5.4, 1.0, None),        # pitching at a cafe table
    ("A", 3, 6.40, 1.45),                          # R: "and one client … for a website."
    ("B", 5, 9.32, "0422", 4.1, 1.0, None),        # hand pulls the laptop out → match cut
    ("B", 5, 9.90, "0431", 1.0, 1.0, None),        # typing close-up: "We built the demo"
    ("B", 6, 10.70, "0425", 0.4, 1.0, None),       # "when we were ready to publish it"
    ("A", 7, 1.44, 1.20),                          # Y night: "And then the payments slowed down."
    ("A", 7, 3.28, (1.30, 1.40)),                  # single push across "he paid us ₹1,500"
    ("A", 8, 6.10, 1.40),                          # "then nothing happened." (payment insert overlays first)
    ("B", 9, 7.60, "0432", 2.9, 1.0, None),        # phone to ear: "So we tried calling him"
    ("B", 9, 9.96, "0432", 10.4, 1.0, None),       # phone lowered, checked
    ("B", 9, 11.30, "0434", 0.3, 1.0, None),       # standing, looking away: "something or the other"
    ("A", 10, 12.62, 1.32),                        # eye contact: "So what did we do next?"
    ("A", 11, 0.78, 1.00),                         # R wide: "You would expect us to publish it anyway,"
    ("B", 12, 3.44, "0467", 6.3, 1.0, None),       # "or to walk away"
    ("A", 12, 4.22, 1.32),                         # tightest: "but we did neither."
    ("A", 12, 5.26, 1.15),                         # "We wanted to handle it professionally,"
    ("B", 13, 8.20, "0446", 1.45, 1.0, None),       # laptop lid closes (after the not-published insert)
    ("A", 13, 8.90, 1.15),                         # R: "client's side." → real whip begins
    ("A", 14, 10.00, 1.10),                        # whip lands on Y selfie
    ("A", 15, 12.62, (1.10, 1.00)),                # slow pull-out
    ("A", 16, 15.10, 1.00),                        # "And in part 2 …" cut out on "with."
]

# overlays drawn in HyperFrames (timeline seconds)
OVER = {
    "paper": (T(1, 4.78), T(1, 5.88)),             # One Loop text match cut, lands on "One Loop"
    "pay": (T(7, 4.80), T(8, 6.45)),               # blurred ₹1,500 receipt
    "flash": (T(9, 12.43), T(10, 12.62)),          # 2-frame black between the clauses
    "notpub": (T(13, 7.30), T(13, 8.20)),          # "Webpage not available"
}
# keyword lockups: (small words, keyword, t0, t1, position)
CAPS = [
    ("agreed to pay us", "₹10,000", T(0, 2.86), T(0, 3.84), "low"),
    ("we went to", "every door", T(2, 0.30), T(2, 1.80), "top"),
    ("and then", "nothing.", T(8, 6.50), T(8, 7.45), "low"),
    ("we wanted to handle it", "professionally.", T(12, 5.40), T(12, 7.00), "low"),
    ("next, in", "part 2", T(16, 15.30), T(16, 18.62), "top"),
]
