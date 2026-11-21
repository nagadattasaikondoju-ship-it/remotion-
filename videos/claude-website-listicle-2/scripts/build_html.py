"""Generate index.html (timeline data + SFX audio tags) from the word timings of the cut.

Run: python3 scripts/build_html.py
All times are on the output timeline (cut.mp4 / voice.wav), from forced alignment of the take.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
TOTAL = 28.3

# item onsets ("A who-this-is-NOT-for section", "An honest...", ...)
ITEMS = [4.91, 6.73, 9.32, 11.07, 12.27, 13.78, 15.60, 17.40, 19.37, 21.02]
CTA = 22.64  # "comment"

LABELS = ["Not for everyone", "After-payment timeline", "Objection killer", "Price anchor", "Live demo",
          "Small first step", "Cost of waiting", "Proof near the CTA", "Common mistakes", "Intentional friction"]
NOTES = ["Be clear about <b>fit.</b>", "No post-payment <b>mystery.</b>", "Answer the <b>real</b> hesitation.",
         "Give the price <b>context.</b>", "Show. <b>Don't</b> just describe.", "A <b>smaller</b> first step.",
         "Make the trade-off <b>visible.</b>", "Proof where the <b>decision</b> happens.",
         "<b>Teach</b> before you sell.", "Useful <b>qualification.</b> Not obstruction."]

CAPS = [
    ("10 things you can tell <em>Claude</em><br>to add to your website", 0.05, 2.48),
    ("and a few of these", 2.50, 3.46),
    ("will <em>actually shock you</em>", 3.46, 4.87),
    ("a “who this is <em>NOT for</em>” section", 4.87, 6.71),
    ("an honest “what happens<br><em>after you pay</em>” timeline", 6.71, 9.30),
    ("a real <em>objection killer</em>", 9.30, 11.05),
    ("a <em>price anchor</em>", 11.05, 12.25),
    ("a “<em>see it working</em>” demo", 12.25, 13.76),
    ("a <em>micro-commitment</em> CTA", 13.76, 15.58),
    ("a “<em>cost of waiting</em>”<br>calculator", 15.58, 17.38),
    ("<em>proof</em> inside the CTA area", 17.38, 19.35),
    ("a “<em>common mistakes</em>”<br>section", 19.35, 21.00),
    ("a deliberate<br><em>friction point</em>", 21.00, 22.60),
    ("comment “<em>PART 3</em>”", 22.62, 23.56),
    ("and I'll show you 5 things", 23.56, 25.04),
    ("Claude should <em>delete</em><br>from your website", 25.04, 26.78),
    ("first.", 26.78, TOTAL),
]

D = {
    "total": TOTAL, "items": ITEMS, "cta": CTA,
    "claude": 1.09, "website": 1.85, "shock": 3.48, "actually": 3.60, "part3": 23.03, "del": 25.55,
    "labels": LABELS, "notes": NOTES,
    "caps": [{"h": h, "t0": a, "t1": b} for h, a, b in CAPS],
}

DUR = {"tick": 0.06, "click": 0.05, "pop": 0.14, "whoosh": 0.42, "riser": 1.45, "impact": 0.8, "chime": 1.1,
       "done": 0.4}
sfx = []  # (file, start, volume)


def add(f, t, v):
    sfx.append((f, round(t, 3), v))


I = ITEMS
# opening: strong accent, headline pop, browser enters, teaser flashes, rise into item 1
add("impact", 0.0, 0.55)
add("pop", 0.05, 0.5)
add("whoosh", D["website"] - 0.14, 0.3)
for t in (D["shock"] + 0.08, D["shock"] + 0.42, D["shock"] + 0.76):
    add("click", t, 0.45)
add("riser", D["shock"] - 0.02, 0.32)
# soft tick per checklist reveal
for t in I:
    add("tick", t - 0.04, 0.38)
# UI clicks at each cursor press
for t in (I[0] + 0.34, I[2] + 0.62, I[4] + 0.30, I[5] + 0.80, I[6] + 0.42, I[9] + 0.26, I[9] + 0.82):
    add("click", t, 0.42)
add("pop", I[4] + 0.98, 0.32)  # "reply sent"
add("whoosh", I[5] - 0.36, 0.26)  # midpoint list swap
add("done", I[9] + 1.18, 0.4)
# CTA accents
add("impact", CTA, 0.45)
add("pop", CTA + 0.06, 0.5)
add("chime", D["part3"], 0.4)
add("pop", D["del"], 0.35)

audio_tags = []
busy = {}  # track index -> end time of the last clip placed on it
for n, (f, t0, v) in enumerate(sorted(sfx, key=lambda s: s[1])):
    d = DUR[f]
    tr = next(i for i in range(11, 40) if busy.get(i, -1) <= t0)
    busy[tr] = t0 + d
    audio_tags.append(
        f'      <audio id="sfx-{n + 1}" src="assets/audio/{f}.wav" data-start="{t0}" data-duration="{d}" '
        f'data-media-start="0" data-track-index="{tr}" data-volume="{v}"></audio>')

tpl = open(os.path.join(HERE, "template.html")).read()
html = (tpl.replace("%%DATA%%", json.dumps(D, ensure_ascii=False))
        .replace("%%TOTAL%%", f"{TOTAL:.4f}")
        .replace("%%AUDIO%%", "\n".join(audio_tags)))
open(os.path.join(ROOT, "index.html"), "w").write(html)
print("total", TOTAL, "caps", len(CAPS), "sfx", len(sfx))
