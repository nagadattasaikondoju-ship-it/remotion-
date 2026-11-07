# WHY Venture Studio: "if you are 25 and building something meaningful, pay attention" (next-cohort reel)

41.0 s · 1080×1920 · 30 fps. The founder talking head (VID_20261104_044324_816, 47.3 s) is cut to 39.2 s of voice, plus a 1.8 s end card.
It's edited in the style of the user's reference reel (20261106-0657-06). `ANALYSIS.md` has the full Parts 1–10 breakdown and blueprint.

- **Name:** "WHY Venture Studio", confirmed by the user.
  - Speech-to-text heard the letters W-H-Y, at low confidence.
  - The end card's hatfellows.com was given in the brief; it still needs confirming.
- **Pipeline:**
  1. `edl.json`: 14 phrases, pauses cut.
  2. `out/base.mov` built from the EDL (trim/concat, 12 ms fades).
  3. `tools/grade.py`: punch-ins plus a clarity grade. No blur or background dimming, per the user's note on the HAT reel.
  4. `index.html` + `render.mjs frames` render the overlay:
     - three-tier lime captions with an ink outline, timed with Whisper medium word times;
     - a red strike, the top title, proof chips and the REC/LIVE viewfinder;
     - the ring punch-in on "only 15 startups", blinds glitches, CTA boxes and the end card.
  5. `tools/denoise.py` (DeepFilterNet3) on the whole take, then `assemble.sh`: EDL voice cut, EQ, de-esser, compression, plus Real SFX from `sfx_cues.json` / `sfx_map.json` (Openverse CC0, Earshot-picked). No music (the user's choice). Master at −14 LUFS / −1.5 dBTP.
  6. `tools/preview.py <t…>`: graded frames with overlay stills, for layout checks.
- **QA:**
  - Real SFX: 13/13 sounds on their frames.
  - video-director `qa_video.py`: loudness PASS (−14.0 LUFS, −1.5 dBTP), no flashes or pops. Its one warning is a 4-frame blank at the start of the end card.
