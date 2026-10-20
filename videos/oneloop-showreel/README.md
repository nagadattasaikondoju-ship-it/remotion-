# One Loop — "One stroke, never lifted" (15 s showreel)

1920×1080 · 60 fps · 120 BPM (7.5 bars). One copper line is the whole film. Every scene is made out of the one before it, and the camera only ever pushes forward. The last frame is the opening copper dot, so the film loops.

| Bar | Time | Technique | Made out of |
|---|---|---|---|
| 1 | 0–2 s | Hook | Dot → stroke draws the One Loop infinity → the X snaps in → push into the X, which becomes two rails |
| 2 | 2–4 s | Kinetic type | The rails form a slit that shutters through AUDIT. BUILD. MARKET. AUTOMATE.; dive into the copper full stop |
| 3 | 4–6 s | Shape morph | Full stop → lens (audit) → browser (build) → growth arrow (market) → infinity (automate) |
| 4 | 6–8 s | 2D → 3D | The infinity extrudes into a solid ribbon, orbits, and turns edge-on into one flat bar |
| 5 | 8–10 s | Data / UI | The bar unfolds a dashboard of the real portfolio: 24 brands · 13 digital marketing / 11 full-service · 4 countries |
| 6 | 10–12 s | Reach (riser) | The card rounds into a dotted globe; one route loops Hyderabad → Bengaluru → Australia → New Zealand → UK → Hyderabad |
| 7 | 12–14 s | Strongest moment | The route tears off into a giant 3D infinity with the promise racing around both lobes → locks into the logo |
| ½ | 14–15 s | End title | ONELOOP + tagline → collapse into the opening dot |

**Logo:** every appearance of the mark and the end lockup uses `logo.js`, vectorised from the real logo PNG, so the loops, cut ends, X and custom ONELOOP lettering match the brand artwork exactly. The continuous figure-eight used for drawing, morphing and 3D shares the logo's measured loop centres, radius and stroke.

**Rules followed:**
- **Type and colour:** one typeface (Montserrat variable), with One Loop copper, terracotta and cream plus black and white.
- **Motion:** spring and exponential easing only, no bounce.
- **Never used:** particles, glows, flares, shake, RGB split, crossfades or gradients.
- **No still holds:** nothing holds still for more than 0.5 s.
- **Data:** every number comes from `OneLoop_Client_Portfolio_5.xlsx`; see `docs/playbook/oneloop-brand.md`.

## Vertical (Instagram Reels)
`index.html?v=1` renders the same film at 1080×1920. It's not a crop: the scenes re-lay out for the tall frame, but timeline and soundtrack are identical.
- **Hook and slit type:** scaled to fit the width.
- **Icons:** 15 % larger.
- **3D ribbon and finale:** auto-fit to the frame width.
- **Dashboard:** a stacked portrait card.
- **Globe:** larger.
- **End lockup:** kept clear of the Reels right-hand buttons and bottom caption area.
```bash
VERT=1 node render.mjs beats    # review frames → out/vertical/beats/
VERT=1 node render.mjs full 3   # sub-frames → out/vertical/sub/
VERT=1 ./assemble.sh            # → out/vertical/OneLoop_OneStroke_Reel_1080x1920_60fps.mp4
```

## Build
```bash
npm i                          # playwright-core (uses /opt/pw-browsers Chromium)
node render.mjs beats          # one frame per beat → out/beats/ (review)
node render.mjs stills 3.9 12.7  # any frames
node render.mjs audio          # Web Audio OfflineAudioContext → out/audio_raw.wav
node render.mjs full 3         # 2,700 sub-frames (60 fps × 3) → out/sub/
./assemble.sh                  # tmix motion blur → 60 fps, master to −14 LUFS, mux → out/OneLoop_OneStroke_Showreel_1920x1080_60fps.mp4
```

**Purity and motion blur:**
- Every frame comes from `window.seek(t)`: no CSS animation, timers or carried state.
- Inside each sub-frame, 4 trailing samples are averaged, so blur follows the speed and direction of every move.
- `tmix` then blends the 3 sub-frames of each output frame.

**Sound:** all synthesised; the Ultimate Editors library isn't connected.
- A kick on every beat, offbeat hats and a sub bass line.
- A hit on every bar change.
- A riser across bar 6, cut dead into the strongest bar.
- Whooshes peaking on the fastest frame of each camera move.
- Clicks and pops on the type, morph, counter, chip and city events.
