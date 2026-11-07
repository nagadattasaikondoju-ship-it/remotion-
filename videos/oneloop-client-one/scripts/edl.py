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
CLEAN = os.path.join(SCR, "ol", "audio2")  # *_dn.wav from DeepFilterNet3, full suppression

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
# every in/out sits in a measured silence (no clipped words, no dragged "and" fragments)
SEGS = [
    ("0647", 0.86, 3.84, "0647", 0.0),    # 0 Our first client agreed to pay us ₹10,000 for a website,
    ("0647", 4.56, 8.20, "0647", 0.0),    # 1 and we had just started One Loop, and that money mattered a lot to us.
    ("AUD", 0.00, 4.36, "0658", 1.91),    # 2 We went to every door in Hyderabad, from small-scale … enterprises.
    ("AUD", 4.52, 8.90, "0658", 1.91),    # 3 We pitched our idea … their business, and one client said yes for a website.
    ("AUD", 9.32, 10.25, "0658", 1.91),   # 4 We built the demo
    ("AUD", 10.74, 12.22, "0658", 1.91),  # 5 when we were ready to publish it.   ("it" lands at 12.00-12.12)
    ("0662", 1.44, 5.30, "0662", 0.0),    # 6 And then the payments slowed down. At the beginning he paid us ₹1,500,
    ("0662", 5.95, 7.45, "0662", 0.0),    # 7 and then nothing happened.
    ("0662", 7.60, 12.50, "0662", 0.0),   # 8 So we tried calling him … something or the other.
    ("0662", 12.62, 14.30, "0662", 0.0),  # 9 So what did we do next?
    ("VID", 0.78, 3.06, "VID", 0.0),      # 10 You would expect us to publish it anyway,
    ("VID", 3.44, 7.00, "VID", 0.0),      # 11 or to walk away, but we did neither. We wanted to handle it professionally,
    ("VID", 7.04, 9.70, "VID", 0.0),      # 12 but that was not the same case from the client's side. (+ whip start)
    ("VID", 10.00, 18.93, "VID", 0.0),    # 13 (whip end) That was about our first client, … we've worked with.
]
FREEZE_F = 21  # end hold on Prahalad's last clean frame for the Part 2 lockup

# frame-quantised segment lengths and timeline starts
LEN = [round((b - a) * FPS) for _, a, b, _, _ in SEGS]
START = [sum(LEN[:i]) for i in range(len(SEGS))]
SPEECH_F = sum(LEN)
TOTAL_F = SPEECH_F + FREEZE_F
TOTAL = TOTAL_F / FPS


def F(seg, t):
    """timeline frame of audio time t inside segment seg"""
    return START[seg] + round((t - SEGS[seg][1]) * FPS)


def T(seg, t):
    return F(seg, t) / FPS


# picture track: each shot runs from its anchor to the next shot's anchor.
#   A-roll: ("A", seg, t, zoom | (z0, z1))   zoom on the speaker, face-centred
#   B-roll: ("B", seg, t, src, src_in, zoom, (cx, cy) or None)
#   J-cut:  ("J", seg)  previous speaker's picture carries on while the next speaker's audio starts
SHOTS = [
    ("A", 0, 0.86, 1.15, 0.40),                    # framed a little low: headroom for the caption beats
    ("A", 0, 2.86, 1.24, 0.40),                    # punch-in on "₹10,000"
    ("A", 1, 5.88, 1.34, 0.40),                    # closer crop after the One Loop match cut
    ("J", 2),                                      # Tarun's "We…" starts 0.2 s before his picture
    ("A", 2, 0.20, 1.38),                          # Tarun: "We went to every door in Hyderabad,"
    ("B", 2, 1.80, "0436", 2.2, 1.0, None),        # feet: "from small-scale"
    ("B", 2, 2.62, "0458", 1.0, 1.0, None),        # street shops: "local business"
    ("B", 2, 3.18, "0457", 31.2, 1.0, None),       # large building: cut on "to large-scale enterprises"
    ("B", 3, 4.52, "0447", 5.4, 1.0, None),        # pitching at a cafe table
    ("A", 3, 6.40, 1.45),                          # Tarun: "and one client said yes for a website."
    ("B", 4, 9.32, "0422", 4.1, 1.0, None),        # hand pulls the laptop out → match cut
    ("B", 4, 9.90, "0431", 1.0, 1.0, None),        # typing close-up: "We built the demo"
    ("B", 5, 10.74, "0425", 0.4, 1.0, None),       # "when we were ready to publish it"
    ("A", 6, 1.62, 1.20),                          # J-cut: "And…" heard over the laptop, then night Prahalad
    ("A", 6, 3.28, (1.30, 1.40)),                  # single push across "he paid us ₹1,500"
    ("A", 7, 5.95, 1.40, 0.43),                    # "and then nothing happened." held on the face (headroom for the line)
    ("B", 8, 7.60, "0432", 2.9, 1.0, None),        # phone to ear: "So we tried calling him"
    ("B", 8, 9.96, "0432", 10.4, 1.0, None),       # phone lowered, checked
    ("B", 8, 11.30, "0434", 0.3, 1.0, None),       # standing, looking away: "something or the other"
    ("A", 9, 12.62, 1.32),                         # eye contact: "So what did we do next?"
    ("J", 10),                                     # Tarun's "You…" starts under Prahalad
    ("A", 10, 0.98, 1.00),                         # Tarun wide: "You would expect us to publish it anyway,"
    ("B", 11, 3.44, "0467", 6.3, 1.0, None),       # "or to walk away"
    ("A", 11, 4.22, 1.32, 0.42),                   # tightest: "but we did neither." (headroom for the beat)
    ("A", 11, 5.26, 1.15, 0.42),                   # "We wanted to handle it professionally,"
    ("B", 12, 8.20, "0446", 1.45, 1.0, None),      # laptop lid closes (after the not-published insert)
    ("A", 12, 8.90, 1.15),                         # Tarun: "client's side." → real whip begins
    ("A", 13, 10.00, 1.10),                        # whip lands on Prahalad's selfie
    ("A", 13, 12.62, (1.10, 1.00)),                # slow pull-out
    ("A", 13, 15.10, 1.00),                        # "And in part 2 …"
]
J_LEN = 0.20
# directional whip blur, one featured transition: (timeline frame, blur radius px)
WHIP_CUT = START[13]
WHIP = [(WHIP_CUT + k, r) for k, r in zip(range(-6, 5), (6, 12, 22, 34, 46, 56, 50, 38, 26, 14, 6))]

# overlays drawn in HyperFrames (timeline seconds)
OVER = {
    "paper": (T(1, 4.78), T(1, 5.88)),             # One Loop text match cut, lands on "One Loop"
    "pay": (T(6, 4.28), T(7, 6.30)),               # blurred ₹1,500 receipt, L-cut under Prahalad's voice
    "notpub": (T(12, 7.30), T(12, 8.20)),          # "Webpage not available" — website held offline
    "end": (T(13, 18.55), TOTAL),                  # "Next in Part 2" lockup on the held face
}
# One Loop newspaper text match cut (after the supplied reference): page changes, in frames from OVER["paper"][0]
MATCH_PAGES = [0, 5, 10, 20, 27]  # last page = One Loop logo card, 4-6 frame settle
# voice groups for tonal matching (Prahalad's camera-mic voice is the reference)
VOICE = ["P_cam", "P_cam", "T_aud", "T_aud", "T_aud", "T_aud", "P_cam", "P_cam", "P_cam", "P_cam",
         "T_vid", "T_vid", "T_vid", "P_vid"]
# ambience beds follow the picture's location changes: (start, kind)
AMBIENCE = [(0.0, "day"), (T(2, 0.20), "dusk"), (T(6, 1.62), "night"), (T(10, 0.98), "night2"),
            (WHIP_CUT / FPS, "street")]

# flash-cut pass: every picture change to the next clip or speaker (the whip at WHIP_CUT keeps its own blur + whoosh)
#   (timeline s, kind, level, what changes)
#   "flash" = exposure flash peaking on the cut + flash SFX; level 3 speaker change, 2 clip change, 1 light
#   "paper" = clean cut with a 1-frame light snap + paper-cut SFX; level 2 proof screen, 1 quick B-roll step
#   flashes stay ≥ 1 s apart (no strobing); cuts that land closer than that become paper cuts
FLASHCUTS = [
    (OVER["paper"][0], "paper", 1, "Prahalad → OneLoop newspaper match cut"),
    (OVER["paper"][1], "flash", 2, "OneLoop logo card → Prahalad"),
    (T(2, 0.20), "flash", 3, "speaker: Prahalad → Tarun"),
    (T(2, 1.80), "flash", 2, "Tarun → feet B-roll"),
    (T(2, 2.62), "paper", 1, "feet → street shops"),
    (T(2, 3.18), "flash", 2, "street → large building"),
    (T(3, 4.52), "flash", 2, "building → café pitch"),
    (T(3, 6.40), "flash", 2, "café → Tarun (\"one client said yes\")"),
    (T(4, 9.32), "flash", 2, "Tarun → laptop B-roll"),
    (T(4, 9.90), "paper", 1, "hand match cut → typing"),
    (T(5, 10.74), "paper", 1, "typing → laptop screen"),
    (T(6, 1.62), "flash", 3, "speaker: Tarun's laptop → Prahalad, night"),
    (OVER["pay"][0], "paper", 2, "Prahalad → ₹1,500 proof"),
    (OVER["pay"][1], "paper", 1, "proof → Prahalad (the low impact carries \"nothing\")"),
    (T(8, 7.60), "flash", 2, "Prahalad → phone-call B-roll"),
    (T(8, 9.96), "paper", 1, "phone to ear → phone checked"),
    (T(8, 11.30), "paper", 1, "phone → standing, looking away"),
    (T(9, 12.62), "flash", 3, "B-roll → Prahalad (\"So what did we do next?\")"),
    (T(10, 0.98), "flash", 3, "speaker: Prahalad → Tarun"),
    (T(11, 3.44), "flash", 2, "Tarun → walk-away B-roll"),
    (T(11, 4.22), "paper", 1, "B-roll → Tarun (\"neither\")"),
    (OVER["notpub"][0], "paper", 2, "Tarun → website held offline"),
    (OVER["notpub"][1], "flash", 1, "offline screen → laptop lid closes"),
    (T(12, 8.90), "paper", 1, "lid → Tarun (\"client's side\")"),
]
