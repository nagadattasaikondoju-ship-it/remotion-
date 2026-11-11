# One Loop: "Your network is your net worth" loop reel

10.0 s · 1080×1920 · 60 fps · 600 frames. A founder's-day b-roll montage under one static caption, cut so the last frame flows into the first and the reel loops seamlessly.

## Caption (on screen for the whole reel, styled after the user's reference)
- **White headline:** Fraunces Bold (soft): "Your network is your / net worth".
- **Yellow block:** a 3D perspective-warp caption matched side by side to the user's reference photo.
  - **Type:** Poppins Bold, with "CHANNEL"/"COMMENTS" ExtraBold, in the reference's exact golden yellow **#FCD400** (sampled from the photo).
  - **Perspective:** the block sits on a plane turned 14° so its right edge is nearer the camera. Letters on the left are smaller and the right side is bigger and heavier, so the top line rises and the bottom lines dip to the right. The plane bows slightly toward the camera right of centre, and the first letter or two of the far-left words lean italic.
  - **Separation:** a soft drop shadow and glow on the letters, plus a faint dark glow behind the block, keep the gold readable over the bright foliage shots.
  - **Kinetic:** a gentle 3D drift (±3° turn, ±1.6° tilt, 6 px float) with periods of 5 s and 2.5 s, so it repeats exactly inside the 10 s loop.
  - All of these are parameters at the top of `overlay.html`, and can be overridden for tests with `QS="rotY=-10&fs=80" node render_overlay.mjs comments still 0`.
  - **Two caption versions:**
    - default: "If you are a Founder| / Entrepreneur / building something / for the future / Join the CHANNEL / (link in bio), / let's connect 🥂"
    - `_COMMENTS`: "Introduce yourself / in the COMMENTS," in place of the channel lines, as in the reference.
    - `_BLACK` (`bash assemble.sh black`): the channel wording in solid black #000, with "Founder/" and 🤝. Everything else is unchanged (perspective, font, size, line breaks, position, white headline).
      - Separation flips to a soft light glow around the letters, plus a faint light glow behind the block.
      - The 🤝 is rendered in dark grey so the hands stay visible.

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
