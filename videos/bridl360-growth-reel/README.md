# BRIDL360: "Land around growth" (rebrand of a reference reel)

The user's request (25 Nov 2026):
- Take the land-investment reel they supplied, which was made for another developer.
- Keep its picture and motion graphics exactly as they are.
- Replace only the brand moments with BRIDL360.
- Use a new, clear male voice and the BRIDL360 logo they supplied.

Output: 49.77 s, 1080x1920, 30 fps, `out/BRIDL360_LandAroundGrowth_1080x1920_{MASTER,share}.mp4`.

## What is replaced (brand.html, a transparent layer over the reference)
Times are in the reference's own timeline.

| Time | Reference | BRIDL360 version |
|---|---|---|
| 14.0–14.6 | "Genome Valley" | "Hyderabad" (same red, same pop) |
| 22.9–26.1 | the other brand's logo on the growth arrows | white BRIDL360 tag: the supplied logo, "BRIDL360", "Real estate · Hyderabad". Same place and tilt |
| 26.9–28.5 | the other brand's logo in the map pin | the pin holds a Vishwasree Residency photo, plus a BRIDL360 label |
| 28.4–30.6 | approval-body logos on the satin | "Homes in" Kompally / Gachibowli / Sadashivpet, each popping on its spoken word (`vo/times.json`) |
| 30.4–32.45 | "40 acres" | "Listed across Hyderabad · 5 Projects" with three project photos, then the reference's dissolve to the family shot |
| 45.15–49.77 | the other brand's end card | BRIDL360 end card in the same layout: logo, tagline, DM US OR CALL NOW, phone, @bridl360, company name and CIN |

Everything else in the picture is the reference's own footage, AI-upscaled with Real-ESRGAN
(`tools/upscale_realesr.py`, from a 420x746 crop of the screen recording).

The base is cropped to 1050x1867 and scaled back up. This removes the recorder's 11 px black strip on the right and the player's
timestamp in the bottom rows. Segments A–C get the same scale, so they stay on their marks.

## Facts used (first-party or registry only)
- **Company:** BRIDL360 Consulting Pvt. Ltd., Hyderabad, Telangana. CIN U74999TG2021PTC151874, incorporated 31 May 2021
  (confirmed on Zaubacorp). The phone number and @bridl360 handle come from the user's research and the Instagram profile.
- **Projects:** Homes247's Vishwasree Residency page lists five projects under "Projects by Bridl360":
  - Vishwasree Residency;
  - Mayfair Luxury Apartments (Kompally);
  - Sai Prakruthi (Kompally);
  - Silpa Bamboo Groove (Sadashivpet);
  - Siva Hills (Sadashivpet).
- **How they are described:** the film says "listed", never "built by", because the listings don't say BRIDL360 built them.
- **Left out:** no RERA or agent claim, because it couldn't be verified. Bridl360.com is a parked domain.
- **Photos (`img/`):** downloaded from Homes247 and carrying its watermark. The watermark is left in place. Swap in BRIDL360's original renders when they arrive, using the same file names.

## Voice (vo/)
- Kokoro `hm_omega` (local, no API) via `tts.mjs`. The lines are in `vo/lines.tsv` (start, slot end, text).
- `build_vo.py` places each line at its start. It speeds a line up only if it overruns its slot (atempo ≤ 1.12).
- Names are spelled for the phonemiser:
  - "Bridle three sixty";
  - "Kom-pully. Gutchy-bowly. Sudda-shiv-pet".
- Whisper hears "Bridal 360", a homophone.

## Sound
- **Bed:** the reference's music stem (Demucs htdemucs, `--two-stems=vocals`, no_vocals). It sits about 6 LU under the voice, as in the reference.
  - The stem dips 7 dB under 28.15–29.95. Its own logo hits fall there and would land off our place-name pops.
- **SFX:** ten real recordings through the house pipeline (`real-sfx` from_cues + mix, then critique). Cues are in `sfx_cues.json`:
  - pops on Hyderabad, the tag, the pin, each place name and "5";
  - one swipe on the slide;
  - a soft whoosh on the end card;
  - a chime on the button.
- **Master:** two-pass loudnorm to −14 LUFS, true peak −1.5 dBTP.

## Rebuild
```
python3 build_vo.py                          # vo/l*.wav -> vo/voice.wav, vo/times.json (needs the explainroo Kokoro clone)
NODE_PATH=$(npm root -g) node render.cjs overlay
REF_UP=<ref_up.mp4> BED=<no_vocals.wav> bash assemble.sh
```

The plates `img/plate_satin.png` (14.0 s) and `img/plate_family.png` (32.5 s) are frames of the upscaled, framing-fixed base.

## Before posting
- The motion design and music belong to the reference ad's maker. Get rights, or ask BRIDL360 to confirm they hold them.
- Confirm the call number (+91 99666 96961) against WhatsApp (99666 86861).
