# Dr. Sri Sushma: Jerry dental reel with the clinic's full end card

## v2 (16 Nov, current): AI-upscaled cartoon + the clinic's full card popping up
11.03 s · 1080×1920 · 30 fps. The user asked for the end card to carry every detail of the clinic's own card (screenshot) with a
good pop-up, and to stay on it, in high quality.

| Time | What happens | Sound |
|---|---|---|
| 0.00–6.03 s | the same Jerry loop, now Real-ESRGAN ×4 (`tools/upscale_realesr.py`) from the recording's 436×774 instead of a lanczos resize: clean outlines and fills, no blocking | the clip's own audio, 60 ms fade at the cut |
| 6.03 s | the card pops up over the frozen last frame (scale 12 % → 100 % with a small overshoot, corners square off, the cartoon blurs and dims) | whoosh-1 (real, earshot's best "quick soft swoosh"), peak 6.09 s |
| 6.21 s | logo bursts in with a twist and a soft blue glow, then keeps growing slowly (+3.5 %) and floats | a single real pop (cut from 3-popping-pops, library id 65) at 6.39 s |
| 6.53 s | clinic-name pill stretches open, letters settle | — |
| 6.69 s | "Act / Early… / Choose / Wisely!" word by word | — |
| 7.03 s | BOOK AN APPOINTMENT WITH US pops; it then breathes, a light streak runs across it (7.5, 9.0, 10.4 s) and a ring pulses off the play icon | chime at 7.20 s |
| 7.27 s | Dr. Sri Sushma, MDS / Periodontist and Implantologist | — |
| 7.51 s | phone and website rows: icon pops, text slides in | — |
| 7.81 s | pin drops in, the three address lines rise | — |
| 8.17 s | "Follow us on social media", Facebook / Instagram / WhatsApp pop one by one | — |
| 8.5–11.03 s | hold; a ring pulses off the phone icon twice (8.8, 9.9 s) to point at the number | — |

- Layout: the clinic's card measured at ×2.5 (432×767 → 1080×1918) and moved down 40 px to clear Instagram's top bar; every line of
  text as on the card. Fonts Poppins and Oswald (OFL, `fonts/`); icons are Simple Icons paths (CC0, `icons/`) and Material-style
  glyphs drawn in `card.html`. The logo (`out/logo.png`, not committed) is blended with multiply, so its white box disappears and
  its 3D shadow stays.
- Render: `card.html` is a pure function of time (`seek(t)`); `render.cjs` screenshots it at 2× with the preinstalled Chromium
  and downsizes once. Picture: cartoon + card in one encode (CRF 10); MASTER = that picture untouched + the mix (−14 LUFS).
- `REF=<screen recording.mp4> bash build_v2.sh` (`SKIP_PICTURE=1` for sound only). v1's `build.sh` is kept below for reference.

## v1 (11 Nov)

7.5 s · 1080×1920 · 30 fps. The user's reference reel (a screen recording that plays the reel twice) re-cut to a single loop, with the end card's logo swapped for **Dr. Sri Sushma Multispeciality Dental Clinic**'s.

## Reference analysis (one loop = recording frames 12–236, 0.4–7.9 s)
| Time | What happens | Sound |
|---|---|---|
| 0.00–6.03 s | Jerry in front of dental forceps and a toothbrush: covers his eyes, points, poses, then a tongue gag | the clip's own audio (0.15–5.9 s) |
| 6.03 s | hard cut to a white card | — |
| 6.03–7.50 s | another clinic's logo, centred; it slowly grows about 8 % | silent |

The recording also carries player chrome: black side bars (content is columns 12–447), a button in the top-left corner, a darkening gradient over the bottom 105 px, and a "0:0x / 0:07" timer.

## What `build.sh` does
1. **Cartoon:** takes the same 181 frames and crops off the side bars. It undoes the bottom gradient (a measured multiplicative ramp, 1.0 → 0.733), removes the timer with `delogo`, and upscales with lanczos plus a light sharpen.
2. **End card:** white, 44 frames, the same as the original. It uses the **blue 3D logo** the user chose (image, 1056×992), 870 px wide at full size.
   - The logo pops in: ease-out-back over 0.3 s, from 30 % size with a small overshoot.
   - It then keeps growing slowly (+6 %), like the original card.
   - The card is composed in RGB. The logo image's near-white background (≥250) is lifted to pure white and its edges are feathered 90 px, so there is no visible box.
   - The flat black PDF version still works: pass `LOGO=…pdf`.
3. **Audio:** the original audio for the same loop, untouched. The card stays silent, as in the original.

```bash
REF=<screen recording.mp4> LOGO=<Dr.Sri_Sushma-logo2.pdf> bash build.sh   # → out/…_MASTER.mp4 (CRF 12) + _share.mp4 (CRF 17)
```

## Notes
- The cartoon is upscaled from the recording's 436×774, so it's as sharp as that source allows. The end card is rendered natively at 1080×1920.
- The reference media and the logo are not committed (client asset and third-party footage).
