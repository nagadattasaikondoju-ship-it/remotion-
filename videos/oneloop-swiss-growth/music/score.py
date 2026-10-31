# Original score for "The Growth Path": a motorik grid at 120 BPM that adds one instrument per rule.
#   Real samples: drum kit (MuldjordKit, FreePats, CC BY 4.0), electric bass, marimba, vibraphone, glockenspiel (VCSL, CC0).
#   Bars 1–2 kick + hats · 3–4 + bass pulse (01 audit) · 5–6 + snare (02 build) · 7–8 + marimba 16ths (03 market)
#   · 9–10 + vibraphone chords, glockenspiel on the ripple (04 automate) · 11–12 full band (05 scale) · hard stop at 24.0
#   · 24.5–26.0 a lone sine glide follows the thread drawing the mark · 26.0 mallet chord on the logo snap · ring-out.
# Writes out/music.wav (48 kHz stereo). Run with the library's Python from $LIB:  .venv/bin/python <project>/music/score.py
import os, sys, numpy as np, soundfile as sf
LIB = os.environ.get("LIB") or os.getcwd(); sys.path.insert(0, LIB)
from core.audio import sampler as S
from core.audio.sfx import SR, add, limit
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEAT, DUR, STOP = 0.5, 30.0, 24.0
S.seed(7)
ev = []
def at(beat): return beat * BEAT
# chords per two bars (D minor world, lifting to F and C, home again for "scale")
PROG = [(4, 'D'), (8, 'Bb'), (12, 'F'), (16, 'C'), (20, 'D')]
ROOT = {'D': 38, 'Bb': 34, 'F': 41, 'C': 36}              # bass roots (MIDI)
TONES = {'D': [50, 53, 57, 60, 64], 'Bb': [46, 50, 53, 57, 60], 'F': [53, 57, 60, 64, 67], 'C': [48, 52, 55, 59, 62]}
def chord_at(t):
    c = 'D'
    for t0, name in PROG:
        if t >= t0: c = name
    return c
# drums
for b in range(48):                                         # 0 – 24 s
    t = at(b)
    ev.append((t, 'drum_kit', 'kick_drum_left', None, .55 if t < 4 else .72, 0))
    if t >= 8 and b % 2 == 1: ev.append((t, 'drum_kit', 'snare_1', None, .55, .05))
    for h in (0, .5):                                       # closed hats in 8ths, accent on the off-beat
        ev.append((t + h * BEAT, 'drum_kit', 'hi_hat_closed', None, .28 if h == 0 else .38, -.25))
for i, t in enumerate(np.arange(23.0, 24.0, BEAT / 4)):     # a short tom run into the hard stop
    ev.append((float(t), 'drum_kit', ['tom_1', 'tom_2', 'tom_3', 'tom_4'][i // 2], None, .45 + i * .04, (-.3 + i * .08)))
ev.append((20.5, 'drum_kit', 'crash_left', None, .45, -.3))  # the pull-out to the wall
# bass: 8th-note motorik pulse with an octave on the off-beat
for k in range(int((STOP - 4) / (BEAT / 2))):
    t = 4 + k * BEAT / 2; r = ROOT[chord_at(t)]
    ev.append((t, 'electric_bass', r + (12 if k % 2 else 0), BEAT / 2 * .9, .62 if k % 2 == 0 else .5, 0))
# marimba: 16th ostinato through the chord tones (from 03 market)
pat = [0, 2, 1, 3, 2, 4, 3, 1]
for k in range(int((STOP - 12) / (BEAT / 4))):
    t = 12 + k * BEAT / 4; tones = TONES[chord_at(t)]
    ev.append((t, 'marimba', tones[pat[k % 8]] + 12, BEAT / 4, .42 + (.12 if k % 4 == 0 else 0), .35))
# vibraphone: a chord on each bar (from 04 automate)
for bar_t in np.arange(16, STOP, 2.0):
    tones = TONES[chord_at(bar_t)]
    for j, p in enumerate(tones[:4]): ev.append((float(bar_t), 'vibraphone', p + 12, 1.9, .45, -.2 + j * .12))
# glockenspiel on the automation ripple (cells filling by distance from the thread)
for i, t in enumerate([16.75, 17.0, 17.25, 17.5, 17.75, 18.0]):
    ev.append((t, 'glockenspiel', [81, 84, 86, 88, 91, 93][i], .6, .32, .4))
for i, t in enumerate([20.75, 21.0]): ev.append((t, 'glockenspiel', [86, 93][i], .8, .3, -.4))
mix = S.render(ev, dur=DUR)
# the hard stop: everything cut on the downbeat (10 ms), one beat of silence
n0 = int(STOP * SR); f = int(.01 * SR)
mix[n0:n0 + f] *= np.linspace(1, 0, f)[:, None]; mix[n0 + f:] = 0
# 24.5–26.0: the only element that sings, a sine gliding with the thread as it draws the mark (D5 → A5)
t = np.arange(int(1.5 * SR)) / SR; u = t / 1.5
freq = 587.33 * (880 / 587.33) ** u
sine = np.sin(2 * np.pi * np.cumsum(freq) / SR) * (0.16 * np.clip(t / .05, 0, 1)) * np.clip((1.5 - t) / .03, 0, 1)
add(mix, sine.astype(np.float32), 24.5, 1.0, 0.0)
# 26.0: the logo lands, a mallet chord and a felt kick; 27.0 glockenspiel on the tagline
end = S.render([
    (0.0, 'drum_kit', 'kick_drum_left', None, .6, 0),
    (0.0, 'vibraphone', 62, 3.5, .55, -.25), (0.0, 'vibraphone', 66, 3.5, .5, .0), (0.0, 'vibraphone', 69, 3.5, .5, .25),
    (0.0, 'marimba', 50, 2.0, .6, -.1), (0.0, 'electric_bass', 38, 2.5, .6, 0),
    (1.0, 'glockenspiel', 86, 2.5, .35, .3), (1.25, 'glockenspiel', 93, 2.5, .3, -.3),
], dur=4.0)
n1 = int(26.0 * SR); mix[n1:n1 + len(end)] += end[:len(mix) - n1]   # stereo stem: placed directly
mix = S.room(mix, size=.18, mix=.08)                       # dry and close: only a hint of room
mix = limit(mix, .9)
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
sf.write(os.path.join(HERE, "out", "music.wav"), mix, SR)
open(os.path.join(HERE, "out", "music_credits.txt"), "w").write("\n".join(S.credits(['drum_kit', 'electric_bass', 'marimba', 'vibraphone', 'glockenspiel'])) + "\n")
print("music.wav", mix.shape[0] / SR, "s; peak", float(np.abs(mix).max()))
