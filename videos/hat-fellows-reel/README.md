# HAT Fellows: "a room full of people as curious as you" (Early Access reel)

44.6 s · 1080×1920 · 30 fps. The founder-voice talking head (VID_20261103_175222, 65 s) is cut to 42.6 s of voice, styled after the user's reference reel and adapted to HAT's own design system.
`ANALYSIS.md` has the full reference breakdown, the comparison and the blueprint.

- **Reference DNA** (a creator reel with a podcast desk and white paper cards), adapted to HAT:
  - two-tier captions: a small lead line, then a big keyword on the stressed word;
  - only the action/payoff words boxed;
  - hard cuts to full-screen paper cards on headline words;
  - the CTA kept on the face.
- **HAT system** (from hatfellows.com, 3 Nov 2026): Space Grotesk / Manrope / DM Mono (OFL, in `fonts/`); cream #F4F1E8, ink #111418, lime #C9FF52; hard ink offset shadows; an outlined headline word.
  - The user's letterpress logo is in `img/`.
  - Card copy quoted from the site: "Build · Ship · Belong", "Applications open", "Founding cohort", "Invite only · selection by application".
- **Pipeline:**
  1. `edl.json`: 16 kept phrases (pauses and fillers cut).
  2. Build `out/base.mov` from the EDL (the ffmpeg trim/concat in the session notes; 12 ms audio fades).
  3. `tools/grade.py`:
     - person matte (torchvision DeepLabV3-MobileNetV3);
     - background softly defocused and dimmed;
     - alternating punch-ins that hide the jump cuts (1.42–1.50× on the wide hook take);
     - warm tone curve with a highlight knee, and a vignette.
     - Needs Pillow on PYTHONPATH (the system PIL is broken for python3.11).
  4. `index.html` + `render.mjs frames`: captions and cards as transparent PNGs. Word times come from Whisper on the cut; captions are verbatim, with the name corrected to "HAT Fellows".
  5. `music/score.py`: an original lo-fi bed.
     - 90 BPM, vibraphone / electric bass from VCSL (CC0), drums from MuldjordKit (CC BY 4.0).
     - Plays under the face only and stops down for every card (house rule).
     - Sits −19 LU under the voice.
  6. `assemble.sh`:
     - voice clean-up;
     - music level;
     - Real SFX from `sfx_cues.json` / `sfx_map.json` (Openverse CC0 recordings picked with Earshot);
     - two-pass loudnorm to −14 LUFS;
     - outputs: MASTER (CRF 8), share copy, and a voice+SFX version with no music.
- **QA:**
  - Real SFX: 16/16 sounds on their frames.
  - Earshot critique: launch-grade, 22/23 metrics. The one flag is music coverage: the stop-downs under the cards are deliberate.
- **To confirm before posting:**
  - "Human Accelerator Tank" is the speaker's expansion of HAT; the site doesn't spell it out.
  - "AI credits" is as spoken; the site lists partner product credits.
