# Dr. Sri Sushma: wisdom-teeth reel (remake of a reference ad), IN PROGRESS

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
