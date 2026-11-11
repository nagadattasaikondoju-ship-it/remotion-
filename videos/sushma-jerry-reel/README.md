# Dr. Sri Sushma: Jerry dental reel with the clinic's logo

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
2. **End card:** white, 44 frames, the same as the original.
   - Dr. Sri Sushma's logo (from the user's PDF) pops in: ease-out-back over 0.3 s, from 30 % size with a small overshoot.
   - It then keeps growing slowly (+6 %), like the original card.
   - The card is composed in RGB with the logo rendered on solid white, so there is no visible edge or box around the logo.
3. **Audio:** the original audio for the same loop, untouched. The card stays silent, as in the original.

```bash
REF=<screen recording.mp4> LOGO=<Dr.Sri_Sushma-logo2.pdf> bash build.sh   # → out/…_MASTER.mp4 (CRF 12) + _share.mp4 (CRF 17)
```

## Notes
- The cartoon is upscaled from the recording's 436×774, so it's as sharp as that source allows. The end card is rendered natively at 1080×1920.
- The reference media and the logo are not committed (client asset and third-party footage).
