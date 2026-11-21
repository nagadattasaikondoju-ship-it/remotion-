# Dr. Sri Sushma: wisdom-teeth reel (remake of a reference ad), v1 delivered 16 Nov

User's brief (16 Nov): keep the reference video EXACTLY (same animations, 3D teeth, captions, timing) and change only:
1. foreign people/photos -> Indian people; 2. the other clinic's brand -> Dr. Sri Sushma's details;
3. the American voice -> an Indian woman doctor (20s-30s) voice. Not a coded/HTML rebuild: edit the video itself.

Reference: the user's upload `06b4398b-20261116-1111-41.8325729.mp4` (430x742, 30 fps, 37.9 s, 10 shots; another clinic's ad).

## Script (Whisper medium, reference timings)
| t (s) | line |
|---|---|
| 0.98 | Hi. Excuse me. Can I please ruin your week a little? |
| ~4.5 | Are you suffering from pain in the gums? |
| ~8.0 | Have a difficulty in fully opening your mouth? |
| ~11.5 | Or a persistent bad taste or odor coming specifically from the back of the mouth? |
| 14.3–20.1 | That means your wisdom teeth might be running out of space. |
| 20.1–25.6 | And when they stay impacted, the pain usually doesn't stay small for long. |
| 25.6–31.1 | The good news? Wisdom tooth removal is way easier when you catch it early. |
| 31.1–37.0 | If your mouth keeps sending warning signs, stop ignoring them. Call **Dr. Sri Sushma Dental Clinic** today. (was "Next Care Dental") |

Word-level timings: re-run `whisper a16.wav --model medium --word_timestamps True` on the reference audio; the new voice is fitted
phrase by phrase to the same windows so every kinetic caption still lands on its word.

## Shots to change (scenedetect cuts: 0, 6.40, 7.97, 10.83, 13.67, 16.67, 20.27, 25.50, 30.17, 34.33)
| time | original | replacement (iStock search that found a good Indian match) |
|---|---|---|
| 6.4–8.0 | white woman holding her cheek | "indian woman toothache holding cheek" -> *Indian Woman with Toothache* (white bg, navy top) |
| 10.8–13.7 | white man opening mouth, tongue depressor | "indian dentist treating indian patient" -> *Indian female patient undergoing a dental procedure* (mouth open, mirror) |
| ~15.0 | woman eating, "Bad Taste" (faded) | "indian woman eating food disgusted bad taste" -> *Indian woman in a yellow shirt eating* |
| ~15.6 | profile, "Or Odor" (faded) | "indian woman checking bad breath" -> *Indian woman* (hand over mouth, pink top) |
| ~26.0 | Black woman smiling + red tooth, "The good NEWS?" | "happy indian woman smiling" -> *Smiling Indian woman* (peach bg) |
| 28.3–30.2 | masked dentist + white patient | *Indian female patient undergoing dental procedure* (portrait, dentist's hands) |
| 34.3–37.9 | end card "NEXT Care Dental / CALL NEXT CARE DENTAL TODAY / +1 713-952-0522" | "Dr. Sri Sushma Dental Clinic / CALL DR. SRI SUSHMA TODAY / +91 79958 15454" in the same type |
Kept (no identifiable face): open-mouth close-ups, gloved hands, 3D teeth. Optional: the "Warning signs" lip/gum tiles (32 s).

## Blocked (16 Nov)
- invideo: the workspace used all its iStock licences this billing cycle and has 0 credits (`stock_quota_exceeded`).
- Keys can't be saved from this (long) session. Needed in the environment's settings: ElevenLabs (header `xi-api-key`, host
  api.elevenlabs.io) for the voice; for photos, a free Pexels key (api.pexels.com) or invideo licences/credits.
- Fallback voice tested: Kokoro hf_beta (explainroo, espeak-ng installed) reads the English clearly but adds "he/and" sounds at
  pauses; usable only after cleanup.
- ElevenLabs (user's key works, FREE tier, 10k chars): free accounts can't use library voices (402) or Voice Design (403) via the
  API, and free output has no commercial licence. Chosen voice once on Starter+: **Monika Sogam - Deep and Natural**
  (`2zRM7PkgwBPiau2jvVXc`, young Indian English female; already in the account's voices). Model eleven_multilingual_v2,
  stability 0.5, similarity 0.8, style 0.15; `/with-timestamps`, then cut into the 14 phrases and place each on its reference start.
- Pexels: the site is 403 to scripts; the API needs a free key (api.pexels.com, header Authorization). Openverse finds only
  Flickr/Wikimedia photos without model releases: not for a clinic ad.

## v1 build (16 Nov): how it was made
- Picture: `tools/upscale_realesr.py` on the reference (crop 418x742 at x 6, x4 -> 1080x1920) -> `out/base_up.mp4`;
  `python3 composite.py out/base_up.mp4 out/picture.mp4` swaps the people and the end card, frame for frame:
  toothache 154-191 (Pexels 3808804), open mouth 240-325 (6502742, Mathura), bad taste 359-396 and odour 397-415 (4584059),
  good news 781-799 (6977987, soft oval cut-out with the original's pop-in/slide-out), dentist 834-904 (8224633, Assam).
  Photos: Pexels licence (free, commercial, no attribution), found by web search and downloaded from images.pexels.com.
  Each photo is row-matched to the original frame's colour (the ad's blue grade and fades) and the original captions are kept on top.
  End card 1031-1136: logo/name/CALL line/number rebuilt (white Dr. Sushma badge, Poppins + Montserrat), fading in like the original.
- Voice: Kokoro `hf_beta` (Indian female) with English phonemes (`node tts_indian.mjs lines.tsv outdir`; the Hindi phonemizer
  added "in/he" sounds at every line edge), "Sri Sushma" said "Shree Sush-maa"; `warp_voice.py` fits it to the original
  speaker's word timing (difflib word match, 0.85-1.2x pieces) so the kinetic captions land on their words.
- Music/SFX: the reference's own bed, separated from the American voice with Demucs htdemucs (vocals removed, ~13 dB under);
  voice level matched to the original vocal stem; mix -14 LUFS, true peak -1.5.

## v2 (16 Nov, current): the reference unchanged, only the brand swapped
User: keep the reference exactly (voice, visuals); only turn the other brand into Dr. Sushma's and end on her pop-up card.
- Picture: the AI-upscaled reference frames 0-1030 untouched (no face swaps), then `endcard/` (the Jerry reel's card.html,
  backdrop = frame 1030, the white flash the original's card came out of), 150 frames; 39.37 s in all.
- Sound: original soundtrack to 34.80 s (just after "them."; "Call" starts at 35.12); then the Demucs music/SFX bed alone, so "Call Next Care Dental today" is gone; the bed's
  last 2 s loop once under the longer card and fade; whoosh/pop/chime on the card via the sound pipeline (trim +2 dB = 4 dB under
  the bed). -14 LUFS.
- `REF=<reference.mp4> STEMS=<dir with music_sfx.wav> bash build_brand.sh` (needs out/base_up.mp4 and endcard/out/card.mp4).
