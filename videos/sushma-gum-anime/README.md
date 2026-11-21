# Pink in the Sink: anime story reel for Dr. Sri Sushma (20 Nov 2026)

39.5 s, 9:16, rendered at 4K (2160x3840) and downscaled for the 1080x1920 MASTER and share copy.

- **Topic:** bleeding gums ("pink in the sink"), the clinic's own specialty (periodontist). Facts kept general and true:
  bleeding gums are an early sign of gum disease; a deep cleaning removes tartar and calms the gums. Recession is not shown reversing.
- **Style:** anime cel shading (ten-styles-reel skill, style 06): two-tone hard shadows, bold ink lines, saturated sky with
  cumulus, speed lines, 3 black/white impact frames + a colour frame on the hook, the wobble and the hero entrance, lens flare.
- **Story:** sink hook → Moti the molar → a little blood → "it's normal" → plaque hardens into tartar, gums angry → gums pull
  back, Moti wobbles → "found the right dental clinic": an anime clinic building with the logo badge, DR. SRI SUSHMA + GUM SPECIALIST ·
  PERIODONTIST pop on screen (the name is never spoken, user's call 21 Nov) → scaler deep cleaning → "Don't wait for the wobble" →
  back, Moti wobbles → Dr. Sri Sushma (clinic badge, gum specialist) → scaler deep cleaning, tartar shatters, gums calm → "Don't
  wait for the wobble" → the clinic's full details card (same card as the clinic's other reels).
- **Voice:** local Kokoro, Indian female voice (hf_beta) with English phonemes; "Sushma" and "Moti" set by hand (`tts.mjs`).
  No paid TTS. Captions use the script's exact words, timed by Whisper (`build_vo.py`).
- **Sound:** house pipeline. Openverse (new CC0 recordings: drain, ice crack, sparkle, electric-toothbrush hum, mouth-harp boing,
  appended to the real-sfx index as ids 66-70) → real-sfx `from_cues` + `mix` → critique (sync 10, headroom 10, balance 10).
  Cue sheet: `CUES.md`. No music under graphics. Mixed to -14 LUFS, true peak -1.5 dB.

## Rebuild
```
node tts.mjs vo/lines.tsv vo        # then trim silence (see build_vo.py header) 
python3 build_vo.py && echo "window.TL = $(cat timeline.json);" > timeline.js
node render.cjs                     # out/anime_4k.mp4 (stills: --stills 1 5 10)
ffmpeg -sseof -0.05 -i out/anime_4k.mp4 -frames:v 1 -update 1 endcard/out/last_frame.png
(cd endcard && CARD_DUR=5.6 CARD_4K=1 node render.cjs)
bash build.sh                       # picture, voice polish, SFX, mix, deliverables
```
(`NODE_PATH=$(npm root -g)` for the Playwright scripts.)
