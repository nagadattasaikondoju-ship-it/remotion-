# One Loop: "What we send a client the day they sign"

8.4 s · 1080×1920 · 60 fps · 504 frames · seamless loop. This rebuilds the user's reference reel; the full breakdown is in `ANALYSIS.md`.

- **Picture:** MVI_0425 from the One Loop B-roll (Drive: "WORK - Green polo typing then thinking, hand on chin, cafe").
  - Upright, with a 15 % punch-in framed high, so the face stays clear of the documents and the blown ceiling is cropped out.
  - Stretched 3.5 % slower to 8.6 s. The last 12 frames cross-fade into the first 12, so the jump from the last frame back to the first is as smooth as a normal frame step (SSIM 0.90).
- **Overlay:** `overlay.html` holds six static scenes: the hook, then Contract, Invoice, Welcome pack, Questionnaire and Brand strategy.
  - They hard-cut on the reference's own frames (60 fps): 0, 116, 172, 234, 298, 362, 434 → 504.
  - The documents are One Loop's own, with placeholders, no amounts and no client names.
  - Photos are One Loop B-roll stills, fetched into `img/` (gitignored).
- **Type:** Instrument Serif (OFL; One Loop's site accent) for the hook and labels; Inter for the documents.
- **Sound:**
  - The reference reel's song: one 8.4 s loop, cut from the user's recording at 8.333 s.
  - Five real CC0 paper drops (library ids 17/18) placed by Real SFX on the document frames, at about −12 dB under the song.
  - Critique: sync 10, balance 10, headroom 10.
  - The master is two-pass loudnorm, −14 LUFS.
  - **The song is a third-party track.** If Instagram mutes it, pick the same song in Instagram's audio picker.

## Build
```bash
SRC=<MVI_0425.mp4> SONG=<song_ref.wav> bash assemble.sh   # → out/OneLoop_DayTheySign_1080x1920_60fps_{MASTER (CRF 10), share (CRF 15)}.mp4
```
