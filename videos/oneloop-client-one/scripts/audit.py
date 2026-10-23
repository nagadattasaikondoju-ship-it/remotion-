"""Write TRANSITIONS.md — every picture change (flash cut / paper cut / whip / graphic) with the SFX actually placed.

Run: python3 scripts/audit.py   (after build_audio.py)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import FLASHCUTS, J_LEN, OVER, START, WHIP, WHIP_CUT, FPS, T, TOTAL  # noqa: E402

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


fx = {c["t"]: c for c in cues if c["moment"] in ("flash", "paper")}
VIS = {("flash", 3): "flash cut, strong (2-frame warm exposure rise → peak on the first incoming frame → 0.16-0.24 s "
                     "recovery) + 4.5 % frame punch settling over 0.36 s",
       ("flash", 2): "flash cut, medium + 3.5 % punch", ("flash", 1): "flash cut, light + 2.5 % punch",
       ("paper", 2): "paper cut: clean cut, 1-frame light snap (0.3) + 1.2 % settle",
       ("paper", 1): "paper cut: clean cut, 1-frame light snap (0.2) + 1.2 % settle"}
NOTE = {T(2, 0.20): f"J-cut: Tarun's \"We…\" starts {J_LEN:.2f} s under Prahalad's picture; day → dusk ambience crossfade",
        T(6, 1.62): "J-cut: Prahalad's \"And…\" heard over the laptop shot; dusk → night ambience crossfade",
        T(10, 0.98): f"J-cut: Tarun's \"You…\" starts {J_LEN:.2f} s under Prahalad; night ambience crossfade",
        OVER["paper"][0]: "voice continues; the newspaper pages then swap hard with faint page flicks + a paper tap "
                          "on the logo card",
        OVER["pay"][0]: "L-cut: his voice carries over the proof; muted phone notification 1 frame later",
        OVER["pay"][1]: "low impact on \"nothing\" 0.3 s later",
        OVER["notpub"][0]: "quiet browser-tab close on the screen"}
md = ["# Transition audit — One Loop \"Client #1\"", "",
      "Final pass: **every change to the next clip or speaker is a flash cut or a paper cut**, each with its own SFX. "
      "Flash cuts go on speaker changes and the main clip changes; quick B-roll steps, proof screens and the "
      "newspaper entry get the lighter paper cut, so flashes always stay ≥ 1 s apart (fast, never strobing). "
      "The real camera whip into Prahalad's selfie stays the one featured transition.", "",
      "SFX level follows the dialogue at each cut: about 15–20 dB under the voice (RMS) over speech, "
      "quieter in pauses, peaks ≤ −11 dBFS; master −14.6 LUFS / −0.9 dBTP.", "",
      "| # | time (s) | cut | visual | SFX (peak dBFS) | audio bridge |", "|---|---|---|---|---|---|"]
for k, (t, kind, lvl, what) in enumerate(FLASHCUTS):
    c = min(fx.values(), key=lambda c: abs(c["t"] - t))
    md.append(f"| {k + 1} | {t:.2f} | {what} | {VIS[kind, lvl]} | {c['sfx'].split(' (')[0]} ({c['peak_db']}) | "
              f"{next((v for tt, v in NOTE.items() if abs(tt - t) < 0.02), 'narration runs across the cut')} |")
md.append(f"| {len(FLASHCUTS) + 1} | {WHIP[0][0] / FPS:.2f}–{(WHIP[-1][0] + 1) / FPS:.2f} | speaker: Tarun → Prahalad selfie "
          f"(real camera whip) | {len(WHIP)}-frame directional whip blur, peak on the cut at {WHIP_CUT / FPS:.2f} | "
          f"{sfx(6)} | ambience crossfade to street at the blur peak |")
md += ["", "Other designed sound: " + "; ".join(f"{sfx(m)} at {moments[m][-1]['t']:.2f} s" for m in (1, 3, 4, 5, 7)
                                                  if m in moments) + ".",
       f"End ({OVER['end'][0]:.2f}–{TOTAL:.2f}): face held, gentle opacity rise of \"Next in Part 2\", clean end."]
open(os.path.join(ROOT, "TRANSITIONS.md"), "w").write("\n".join(md) + "\n")
print("\n".join(md))
