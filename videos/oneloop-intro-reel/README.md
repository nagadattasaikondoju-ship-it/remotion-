# One Loop intro reel: "The Node" (25 s · 1080×1920 · 60 fps · 120 BPM)

One copper dot carries the whole film. It's the dot from the live site's Growth Path timeline (oneloop.in), and in each scene it turns into the next real UI element:
1. The full stop that breaks "GAPS"
2. The arrow head of "Audit my business"
3. The audit card's corner dot
4. The timeline node the cursor drags down the path
5. A product's LIVE light
6. The active client tab
7. The dot riding the "x" of ~9x
8. The pen that draws the logo's two loops
9. The arrow head of the end-card call to action

The full beat-by-beat plan is in `STORYBOARD.md`, along with what was captured from the site (`site/`: screenshots, computed styles, results-tab text).

## Truth
- **Words and figures:** every word and number on screen is copied from oneloop.in as captured on 7 Nov 2026. That covers the Growth Path copy, the shipped products and the four client tabs in Proven Results; the tile values are exactly what each tab shows. The "~9x" payoff is the Bikers Wear Australia tile ("~9x return on ad spend, sustained across 17 months · $753K on $88K ad spend").
- **Logo:** the traced vector from `videos/oneloop-showreel/logo.js`.

## Brand rules followed
- **Type:** one typeface, Almarai (OFL, `fonts/`).
- **Colour:**
  - The ground is black, with cards #161616.
  - Text is cream #E1E0CC, and the button and light tiles are #DEDBC8.
  - Copper #E59C69 appears only on the Node and on each scene's one key word: Audit, Build, Market, Automate, Scale, Built, Proven. The logo's own copper parts are the exception.
- **Changed from the site:** the site's pastel result tiles are rendered cream and dark, and its Instrument Serif and mono accents are dropped. Both keep the reel to one typeface and one accent.
- **Motion:**
  - Every move is a damped spring (about 1.5 % overshoot) or exponential easing.
  - Things grow, unfold, or are revealed by masks and clip insets.
  - Each scene's camera pushes about 4 %, and the Node match carries the zoom into the next scene.
  - Blur follows each move's speed and axis: an SVG Gaussian sized from the frame-to-frame velocity of the camera, the Node, the cursor, thrown cards and split type.
- **Never used:** particles, glows, flares, shake, RGB split, crossfades (opacity is only ever 0 or 1) or gradients.

## Build
```bash
node render.mjs stills 1.0 4.3 16.3   # any frames → out/stills/
node render.mjs beats                 # every half beat → out/beats/
node render.mjs audio                 # audio.js OfflineAudioContext score → out/audio_raw.wav
node render.mjs full 6                # 25 s × 180 sub-frames → out/sub/ (about 3 min)
bash assemble.sh                      # tmix 3-sub-frame motion blur → 60 fps; score + real SFX; −14 LUFS; deliverables
```
- **Determinism:** `window.seek(t)` is pure. Every style is computed from `t`: no CSS animation, timers or carried state. Match cuts measure the target element on screen at runtime (`getBoundingClientRect`), never hard-coded.
- **Picture:** each output frame averages three trailing sub-frames (1/180 s apart).

## Sound
- **Score (`audio.js`, written in code as the brief asked):**
  - A kick on every beat, offbeat hats (16ths through the results section) and a bass root per bar.
  - A hit on every scene change: 2, 4, 8, 10, 18 and 21 s, with the biggest at 16.
  - A riser from 14 to 16 s that cuts dead on the payoff.
  - A rising sweep while the loops are drawn, and a chord under the end card.
- **Interface sounds:** real CC0 recordings from the Openverse library, placed on their frames by the Real SFX skill from `sfx_cues.json` (`sfx_map.json` picks the recordings), then checked by its critique.
  - Sounds: clicks on every cursor click, card and paper slides on unfolds and throws, pops on lock-ups, a few whooshes on the big moves, and keystrokes on the URL.
  - Stems are written to `out/stems/`.
