# Talking-head → vertical short

Auto-edits a talking-head clip into a 1080×1920, 30 fps short: silence and filler
removal, face-locked framing with punch-ins, word-level animated captions,
motion graphics, explicit transitions, ducked music and a light grade.

```bash
npm i
npm run prep:setup                 # once: python deps + models
npm run prep -- path/to/clip.mp4   # stages 1-2 -> public/media/source.*
npm run dev                        # preview in Remotion Studio
npm run render                     # stage 4 -> out/short.mp4 (H.264, CRF 18)
```

If Remotion can't download its headless Chrome, point it at a local one with
`REMOTION_BROWSER_EXECUTABLE=/path/to/chrome-headless-shell`.

## How it fits together

| Stage | Where | Output |
| --- | --- | --- |
| 1. Transcribe + silence/filler detection | `pipeline/transcribe.py`, `pipeline/build_edl.py` | `source.words.json`, `source.edl.json` (the cut list) |
| 2. Face detection | `pipeline/detect_faces.py` | `source.faces.json` (per-frame boxes) |
| Music placeholder | `pipeline/make_beat.py` | `music.wav` (synthesised, royalty-free) |
| 3. Composition | `src/Root.tsx`, `src/MyVideo.tsx`, `src/short/*` | the `Short` composition |
| 4. Render | `scripts/render.mjs` | `out/short.mp4` |

Details on stages 1–2 (review flow, overrides, tuning) are in
[`pipeline/README.md`](pipeline/README.md).

## Customising — `src/short/config.ts`

- `accent`, `hook`, `lowerThird`: brand colour and copy.
- `captions.keywords`: words that are highlighted in the accent colour and pop.
- `captions.corrections`: fix mis-heard words without re-running the pipeline.
- `stats`: kinetic number pop-ins, triggered when a phrase is spoken.
- `transitions`: whip-pan / crossfade on specific cuts, by a source time inside
  the removed gap (see `source.edl.json`).
- `face`, `punchIn`: framing target, headroom zoom, smoothing, punch-in level.
- `music`: track, full/ducked volume, attack/release.
- `colorGrade`: CSS filter on the video layer.
