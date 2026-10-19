"""Write TRANSITIONS.md — one row per speaker change and per designed transition, with the SFX actually placed.

Run: python3 scripts/audit.py   (after build_audio.py)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import J_LEN, OVER, START, WHIP, WHIP_CUT, FPS, T, TOTAL  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
cues = json.load(open(os.path.join(ROOT, "assets", "audio", "sfx_cues.json")))["sfx"]
moments = {}
for c in cues:
    moments.setdefault(c["moment"], []).append(c)


def sfx(m):
    if m not in moments:
        return "none"
    c = moments[m]
    return f"{c[-1]['sfx']} ({c[-1]['peak_db']} dBFS peak)" + (f" + {len(c) - 1} faint page textures" if len(c) > 1 else "")


rows = [
    ("Speaker", f"{START[2] / FPS:.2f} → {OVER['dip1']:.2f}", "Prahalad, day lane", "Tarun, dusk tree stump",
     f"J-cut: Tarun's \"We…\" starts {J_LEN:.2f} s under Prahalad's picture; day → dusk ambience 6-frame constant-power crossfade",
     "6-frame dark exposure dip centred on the picture cut", sfx(2)),
    ("Speaker", f"{OVER['wipe2'] - 0.18:.2f} → {OVER['wipe2']:.2f}", "Tarun's section (laptop B-roll, \"…publish it.\")",
     "Prahalad, night", "J-cut: Prahalad's \"And…\" heard over the laptop shot; dusk → night ambience crossfade",
     "7-frame soft shadow wipe (no flash — day to night)", "none"),
    ("Speaker", f"{START[10] / FPS:.2f} → {OVER['wipe3']:.2f}", "Prahalad, night (\"So what did we do next?\")",
     "Tarun, night (\"You would expect us…\")",
     f"J-cut: Tarun's \"You…\" starts {J_LEN:.2f} s under Prahalad; night ambience crossfade",
     "5-frame shadow pass", "none (moral turning point kept quiet)"),
    ("Speaker", f"{WHIP[0][0] / FPS:.2f} → {(WHIP[-1][0] + 1) / FPS:.2f}", "Tarun, night (\"…client's side.\")",
     "Prahalad, night selfie", "real camera whip in the footage; ambience crossfade to street at the blur peak",
     f"the one featured transition: {len(WHIP)}-frame directional whip blur, peak on the cut at {WHIP_CUT / FPS:.2f}",
     sfx(6)),
    ("Graphic", f"{OVER['paper'][0]:.2f} → {OVER['paper'][1]:.2f}", "Prahalad", "OneLoop newspaper match cut → Prahalad",
     "voice continues (\"…we had just started One Loop…\")",
     "hard page swaps, OneLoop locked on one screen point, 3-frame blur settle per page, 5-frame logo-card settle; clean cut back",
     sfx(1)),
    ("Proof", f"{OVER['pay'][0]:.2f} → {OVER['pay'][1]:.2f}", "Prahalad, night", "redacted ₹1,500 receipt → Prahalad",
     "L-cut: his voice carries over the proof", "3-frame fade in + slow settle; clean cut back to the face for \"nothing happened\"",
     sfx(3) + "; then " + sfx(4) + f" at {T(7, 6.58):.2f}"),
    ("Beat", f"{OVER['flash'][0]:.2f} → {OVER['flash'][1]:.2f}", "phone B-roll (\"…the other.\")",
     "Prahalad (\"So what did we do next?\")", "speech pause", "2-frame black between the two clauses (not a fade)", "none"),
    ("Proof", f"{OVER['notpub'][0]:.2f} → {OVER['notpub'][1]:.2f}", "Tarun", "\"Website held offline\" screen → laptop lid closes",
     "voice continues", "clean factual cut, 4-frame screen settle", sfx(5)),
    ("End", f"{OVER['end'][0]:.2f} → {TOTAL:.2f}", "Prahalad selfie", "held face + \"Next in Part 2\"",
     "room tone + street ambience", "face held, gentle opacity rise of the lockup, clean end (no boom)", sfx(7)),
]
md = ["# Transition audit — One Loop \"Client #1\"", "",
      f"Designed SFX moments: {len(moments)} (limit 6–8). Everything else is a clean cut.", "",
      "| type | time (s) | outgoing | incoming | audio bridge | visual | SFX |", "|---|---|---|---|---|---|---|"]
md += ["| " + " | ".join(r) + " |" for r in rows]
md += ["", "B-roll montage (8.40–17.90) and the phone sequence (23.10–28.00) are motion-led hard cuts with the narration "
       "running continuously; natural footsteps (J-cut 0.3 s), keyboard and laptop-lid sound come from the footage itself."]
open(os.path.join(ROOT, "TRANSITIONS.md"), "w").write("\n".join(md) + "\n")
print("\n".join(md))
