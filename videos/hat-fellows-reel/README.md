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
  3. `tools/grade.py` (v2, after the user's notes on 3 Nov: **no background blur or dimming**, the room stays as shot):
     - alternating punch-ins that hide the jump cuts (1.42–1.50× on the wide hook take, Lanczos);
     - a clarity grade read from the footage: the walls' green fluorescent cast neutralised, highlights kept off the clip point,
       a gentle S-curve, +8 % chroma, light local contrast (CLAHE) and a thresholded unsharp mask for an HD read;
     - an 8 % edge vignette.
  4. `index.html` + `render.mjs frames`: captions and cards as transparent PNGs. Word times come from Whisper on the cut; captions are verbatim, with the name corrected to "HAT Fellows".
  5. Voice: `tools/denoise.py` runs DeepFilterNet3 (speech enhancement) on the whole take before cutting.
     - Pauses drop from about −57 dB to −80/−88 dB.
     - Then it's cut on the EDL, with EQ (de-box, presence, air), a de-esser and gentle compression (in `assemble.sh`).
     - Needs `deepfilternet` + `torchaudio` 2.5.1 on PYTHONPATH, with the model unzipped in `~/.cache/DeepFilterNet/DeepFilterNet3`.
  6. `music/score.py`: an original lo-fi bed. It's **not in the main version** (the user asked for only the voice plus the transition SFX).
     - Kept for `_share_with-soft-music.mp4`, 4 dB lower than before.
  7. `assemble.sh`:
     - Real SFX from `sfx_cues.json` / `sfx_map.json`: card whooshes (softer), the HAT-reveal impact, stamps, pops, the "live" chime and the end-card glint. The risers were removed.
     - Two-pass loudnorm to −14 LUFS.
     - Outputs: MASTER (CRF 8) and share (CRF 15), both voice + SFX; plus `_share_with-soft-music`.
- **QA (v2):**
  - Real SFX: 14/14 sounds on their frames.
  - Voice gaps sit at −68 to −81 dB after noise reduction.
  - Final −14.5 LUFS.
  - Earshot's only critical flag is "no music", which is deliberate: the main version is voice + transition SFX, as the user asked.
- **To confirm before posting:**
  - "Human Accelerator Tank" is the speaker's expansion of HAT; the site doesn't spell it out.
  - "AI credits" is as spoken; the site lists partner product credits.
