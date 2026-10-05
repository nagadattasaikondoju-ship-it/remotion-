---
workflow: general-video
flow: companion
storyboard: no
message: "Playing it safe erases you — be impossible to ignore."
destination: reels / shorts
aspect: "9:16"
length: 35.3s
---

# Brief

Talking-head recut of `assets/take.mp4` (9:16) with trims, punch-ins, motion-graphic overlays,
a synthesized dark-minimal music bed and SFX. Full edit decision list supplied by the user.

## Intent
- Hook cut at the first word; hard out right after "scrolled past".
- Framing ladder: 100% wide / 108% push / 110–114% punch.
- Style reference: minimalist editorial / brutalist corporate — cream paper cards, black Swiss
  type, crimson keywords, masking tape, 2.5D keycap, bezier ribbon, emoji stickers, glow type on
  near-black, ghost trails, spring overshoot.

## Edit decisions (source → timeline)
| Source range | Timeline | Note |
| --- | --- | --- |
| 1.65 – 18.20 | 0.00 – 16.55 | setup dead time removed |
| 20.15 – 26.25 | 16.55 – 22.65 | 2.4s dead pause after "erases it" tightened (not in the original plan — revertable) |
| 30.25 – 42.90 | 22.65 – 35.30 | 4.4s pause before the solution tightened to ~0.4s |

Measured with ffmpeg silencedetect; speech actually ends at 42.77s (plan said 41.8–42.3).

## Audio
- Voice: highpass 75 Hz, denoise, -6 dB @ 60 Hz hum, +2 dB high-shelf @ 3.2 kHz, loudnorm -14 LUFS / -1 dBTP.
- Bed + SFX synthesized offline (`scripts/synth_audio.py`); bed at ~-18 dB under voice, carved with
  `hyperframes-audio/scripts/carve.mjs`.

## Notes
- GSAP is vendored in `assets/vendor/` (CDN blocked in the build sandbox; also makes renders offline-safe).
