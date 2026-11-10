# One Loop: "Your network is your net worth" loop reel

10.0 s · 1080×1920 · 60 fps · 600 frames. A founder's-day b-roll montage under one static caption, cut so the last frame flows into the first and the reel loops seamlessly.

## Caption (on screen for the whole reel, styled after the user's reference)
- **White headline:** Fraunces Bold (soft): "Your network is your / net worth".
- **Yellow block:** Poppins Bold in the reference's exact golden yellow, **#FCD400** (sampled from the user's photo). It's flat, with no outline.
  - **Wobble:** a wave travels through every line. As it passes, each letter bobs, leans italic, swells slightly and gets heavier, like Instagram's wobble text. The period is 1 s, so it repeats exactly inside the 10 s loop.
  - **Two caption versions:**
    - default: "If you are a Founder| / Entrepreneur / building something / for the future / Join the CHANNEL / (link in bio), / let's connect 🥂"
    - `_COMMENTS`: "Introduce yourself / in the COMMENTS," in place of the channel lines, as in the reference.
- **Readability:** a soft dark band sits behind the white headline only; the yellow block has just a faint shadow, to stay true to the reference.

## Cut (`edl.txt`, all from the One Loop b-roll Drive folder)
20 half-second beats, so the cuts land on the beat of most 100–130 BPM songs:
1. Bike POV (0456)
2. Feet walking (0436)
3. Laptop out of the bag (0422)
4. Typing (0431)
5. Headphones on (0440)
6. On a call (0432)
7. Working together (0433)
8. A guest walks in (0449)
9. **Handshake**, the 1.5 s hero beat (0450)
10. High-five (0447)
11. Bike POV (0456)

The final shot is the second immediately before the opening shot's in-point. The jump from the last frame to the first is as smooth as a normal frame step (SSIM 0.901, against 0.907 for an ordinary step).

Not used:
- 0417/0418: a landscape talking head.
- 0451/0452/0459: a client's signboard.
- 0448: other creators' faces on a phone.
- 0457/0458: night and street shots with no people.

## Sound
None. The user adds the song in Instagram's editor. The files carry a silent stereo track so every app accepts them.

## Build
```bash
bash assemble.sh [channel] [comments]   # renders overlay.html frame by frame (60 fps), cuts the EDL from the camera originals (transpose=2), writes MASTER (CRF 10) + share (CRF 18)
```
`SRC` points at the downloaded camera originals (Drive folder 1hD2ac0YRejkVVhFfPBrYrpVGIjxQAKNY).

Fonts (`fonts/`):
- Fraunces: OFL.
- Poppins 600/700/800: OFL, © The Poppins Project Authors, via Google Fonts.
