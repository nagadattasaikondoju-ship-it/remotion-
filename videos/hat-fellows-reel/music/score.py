# Original lo-fi bed for the HAT Fellows reel (in place of the reference's licensed track): 90 BPM, swung 8ths,
#   soft vibraphone 7th chords (Fmaj7 · Em7 · Dm7 · Cmaj7), fingered electric bass, MuldjordKit drums played gently.
#   Real samples: VCSL (CC0) vibraphone + electric bass, MuldjordKit (FreePats, CC BY 4.0) drums.
# House rule: music sits under the talking head only, so the bed stops down for every full-screen card and comes back
# on the cut back to the face (the cards are carried by SFX). Writes out/music.wav (48 kHz stereo).
# Run from the library:  cd $LIB && .venv/bin/python <project>/music/score.py
import os, sys, json, numpy as np, soundfile as sf
LIB = os.environ.get("LIB") or os.getcwd(); sys.path.insert(0, LIB)
from core.audio import sampler as S
from core.audio.sfx import SR, limit
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 90; B = 60 / BPM; BAR = 4 * B; DUR = 44.6
CARDS = [(11.40, 14.40), (20.96, 24.10), (26.20, 28.72), (33.90, 36.38), (42.62, DUR)]
S.seed(11)
CH = [("F", 41, [53, 57, 60, 64]), ("Em", 40, [52, 55, 59, 62]), ("Dm", 38, [50, 53, 57, 60]), ("C", 36, [48, 52, 55, 59])]
SW = 0.62                                                   # swing: the off-8th lands at 62 % of the beat
ev = []
nbars = int(DUR / BAR) + 1
for bar in range(nbars):
    t0 = bar * BAR; name, root, tones = CH[bar % 4]
    # vibraphone: chord on 1 (rolled), a lighter stab on the "and" of 2
    for i, p in enumerate(tones): ev.append((t0 + i * 0.018, "vibraphone", p, BAR * 0.55, .42, -.25 + i * .15))
    for i, p in enumerate(tones[1:]): ev.append((t0 + B + SW * B + i * 0.012, "vibraphone", p + 12, B * 0.6, .26, .3 - i * .1))
    # bass: root on 1, fifth on the "and" of 2, root again on 3, approach note on 4-and
    for tt, p, d, v in [(0, root, 1.4 * B, .62), (B + SW * B, root + 7, .5 * B, .45), (2 * B, root, 1.2 * B, .55), (3 * B + SW * B, root - 1 if bar % 4 == 3 else root + 2, .4 * B, .4)]:
        ev.append((t0 + tt, "electric_bass", p, d, v, 0))
    # drums: kick 1 and 3-and, snare (soft) 2 and 4, swung closed hats
    for tt in (0, 2 * B + SW * B): ev.append((t0 + tt, "drum_kit", "kick_drum_left", None, .5, 0))
    for tt in (B, 3 * B): ev.append((t0 + tt, "drum_kit", "snare_1", None, .30, .05))
    for k in range(4):
        for off, v in ((0, .16), (SW, .22)): ev.append((t0 + k * B + off * B, "drum_kit", "hi_hat_closed", None, v, -.2))
mix = S.render(ev, dur=DUR)
# lo-fi colour: gentle low-pass (one-pole, ~3.2 kHz) and a touch of room
a = np.exp(-2 * np.pi * 3200 / SR); y = np.zeros_like(mix)
for c in range(2):
    acc = 0.0; x = mix[:, c]; yc = y[:, c]
    from scipy.signal import lfilter
    yc[:] = lfilter([1 - a], [1, -a], x)
mix = S.room(y, size=.3, mix=.12)
# stop-downs under the cards: 60 ms out at the cut in, 120 ms back in at the cut out
g = np.ones(len(mix)); tt = np.arange(len(mix)) / SR
for a0, b0 in CARDS:
    g[(tt >= a0) & (tt < b0)] = 0
    i0 = int(a0 * SR); n = int(0.06 * SR); g[max(0, i0 - n):i0] = np.minimum(g[max(0, i0 - n):i0], np.linspace(1, 0, min(n, i0)))
    i1 = int(b0 * SR); n = int(0.12 * SR)
    if i1 < len(g): g[i1:i1 + n] = np.linspace(0, 1, len(g[i1:i1 + n]))
mix = limit(mix * g[:, None], .9)
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
sf.write(os.path.join(HERE, "out", "music.wav"), mix.astype(np.float32), SR)
open(os.path.join(HERE, "out", "music_credits.txt"), "w").write("\n".join(S.credits(["vibraphone", "electric_bass", "drum_kit"])) + "\n")
print("music.wav", len(mix) / SR, "s")
