# Three Angle Method: stickman explainer (16:9 · 1920×1080 · 24 fps · 42.5 s)

The Three Angle reel script retold as a minimal hand-drawn stickman story: a confused business owner, a female explainer, and the problem / proof / offer method. The scene plan and timings are in `STORYBOARD.md`.

## Brief → what was built
- **Style:**
  - Pure white background, thick uniform black lines that redraw (boil) 12 times a second, hollow heads, dot eyes and line mouths, no clothing.
  - Accents: electric purple, vivid green and coral red only, all flat (no gradients, shadows or 3D).
  - The explainer is the same rig with a ponytail.
- **Text:** none on screen except the final word **META**. No subtitles, no logos.
  - The ad platform is a generic round machine with one eye. The second platform is a generic magnifier.
- **Scenes:** six sequential scenes, about 5–8.6 s each, timed to the narration. Each ends on the object or motion the next one starts from:
  1. panel → card flight
  2. triangle → card slots
  3. third slot
  4. audiences → coin stacks
  5. crowned winner → strategy deck
  6. deck → phone
- **Facts:** nothing is added beyond the script. Coin stacks and audiences are shown without numbers. Which card gets cut is illustrative only.

## Voice
- **Model:** Kokoro `hf_alpha`, a local voice trained on Indian speech, reading English with American phonemes. It is free and nothing leaves the machine.
- **One continuous master:** the same voice and speed (1.12×) throughout. Rebuild it with `voice/build.sh`.
- **Intelligibility:** Whisper small reads the bare voice back word-perfect, and the finished mix at 3.9 % word error rate (mostly "your"/"you're").
- **Length:** the script needs 41.8 s at this pace, so the film is 42.5 s, not 40. At 40 s the narrator would have to speak about 200 words a minute.
- **No speech markup:** Kokoro has no emphasis tags, so key phrases are stressed only by punctuation and by the picture landing on them.
- **For a cloned or premium voice:** ElevenLabs (paid) can replace `voice/voice_master.wav`. Nothing else changes.

## Sound
- **Music:** `audio.js` composes an upbeat tech bed in code: 112 BPM, C–G–Am–F, plucks, a soft kick and a pad. It sits about 15 dB down and is sidechain-ducked under the voice.
- **SFX:** real CC0 recordings from the Openverse library, placed by the Real SFX skill from `sfx_cues.json` and `sfx_map.json`:
  - the ad-targeting scan
  - three different pops for the three angles
  - a rising whoosh as the budget moves
  - typing for META, the send click and the notification chime
  - a few quiet whooshes and paper slides on the moves
- **Master:** two-pass loudnorm to −14 LUFS. Stems are written to `out/stems/`.

## Build
```bash
voice/build.sh                      # narration (once)
node render.mjs stills 3.4 25.6     # review frames → out/stills/
node render.mjs audio               # music bed → out/music_raw.wav
node render.mjs frames 4            # 1,020 frames → out/frames/
bash assemble.sh                    # video, ducked music, real SFX, −14 LUFS, MASTER + share
```
