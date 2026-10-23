# One Loop — "The Thread That Closes the Gaps" (vertical explainer)

76 s · 1080×1920 · 60 fps · 120 BPM (38 bars).

- **Research, brand essence, strategy, script, hooks, versions and gaps:** see [STRATEGY.md](STRATEGY.md).
- **Picture:** `index.html` is a canvas renderer. `window.seek(t)` draws any frame as a pure function of time, with 4-sample in-page motion blur.
- **Logo:** `logo.js` is the traced One Loop logo, the same file as `../oneloop-showreel/logo.js`.
- **Sound:** `audio.js` is the OfflineAudioContext soundtrack (kick, hats, sub, hits, 4 risers, whooshes, textures). All SFX are synthesised; the Ultimate Editors library isn't in the repo yet.
- **Fonts:** Almarai and Instrument Serif, the website's own faces. Photos come from One Loop's own portfolio PDF and team shoot.

```bash
npm i                         # playwright-core (Chromium is pre-installed at /opt/pw-browsers)
node render.mjs beats 0 76 0.5    # review stills, one per half-beat → out/beats
node render.mjs stills 12.2 66.5  # specific frames → out/stills
node render.mjs audio             # → out/audio_raw.wav
node render.mjs full 4            # 180 sub-frames/s → out/sub (≈13 min)
./assemble.sh                     # tmix → 60 fps, −14 LUFS master, MASTER + share MP4s in out/
```
