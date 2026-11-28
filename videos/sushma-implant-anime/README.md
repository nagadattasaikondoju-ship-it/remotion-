# Missing tooth → dental implant: split-screen anime awareness reel for Dr. Sri Sushma (23 Nov 2026)

34.5 s · 1080×1920 · 30 fps. Format copied from the user's reference reel (split screen: speaker on top, animation below, clinic CTA).

- **Top (0–31.5 s):** the speaker clip from the reference (KBC footage). The user's call: general awareness.
  - Cropped to its panel.
  - From 29.3 s it punches in 1.29× from the top, so the original sponsor's banner (another dental chain) is out of frame.
  - AI-upscaled with `tools/upscale_realesr.py`.
- **Bottom:** `implant.html`, a new anime story in the Pink in the Sink style (`lib.js` = shared primitives), timed to his words (Whisper turbo):
  - the tooth cracks and flies out → MISSING TOOTH, the neighbours drift
  - the face collapses against a dotted original outline → FACE SHAPE CHANGES
  - bone dissolves under the gap → BONE LOSS
  - a late implant wobbles out → HARDER TO FIX
  - rewind: implant spun into healthy bone, abutment, new crown lands → DENTAL IMPLANT, ON TIME!
  - calendar flips while a ₹ stack grows → DON'T DELAY!
- **End (31.5–34.5 s):** Dr. Sri Sushma's details card (`endcard/`, same card as her other reels).
- **Sound:** his voice (cleaned), plus 21 real recordings through the house pipeline (cue list `sfx_cues.json`).
  - New: coin drop (Openverse CC0, index id 71).
  - critique: sync 10, balance 10; −14 LUFS.

```
node render.cjs [--stills 2 9 20]        (NODE_PATH=$(npm root -g))  -> out/anime.mp4
REF=<reference.mp4> TOP=<top_up.mp4> bash assemble.sh
```
