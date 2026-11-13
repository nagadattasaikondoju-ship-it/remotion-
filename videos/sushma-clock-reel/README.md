# Dr. Sri Sushma: "tooth clock" reel

18.73 s · 1080×1920 · 60 fps · seamless loop, timed to the reference song. Rebuilt in code from the user's reference (another clinic's reel, screen-recorded at 446×744), in Dr. Sri Sushma Multispeciality Dental Clinic's own blues and with its logo.

## Reference analysis
- **Clock (0–13 s):** a clock face of 8 teeth decaying around the dial: healthy · small spot · cavity · deep decay · broken · roots only · empty socket · implant.
- **Hands:** one hand stays at 12 while the other steps from tooth to tooth. At each tooth a label appears: Ignored, Decayed, Treatable, Delayed, Hopeless, Lost it, Choose Health.
- **End card (13–19.5 s):** back at 12, the clock fades to the clinic's end card:
  - logo
  - "Act Early… Choose Wisely!" typed out
  - the "BOOK AN APPOINTMENT WITH US" button
  - the contact lines popping in one by one
- **Audio:** a background song, 18.73 s per loop. The music starts 0.93 s into the recording, and the reel loops at 0.80 s.
- **Hand landings:** 0.80, 2.17, 3.60, 5.27, 6.80, 8.30, 9.97 and 11.33 s from the start of the loop, on the music. The end card comes in around 12.2 s.

## This version
- **Palette:** taken from the logo, deep blue #257BC6 → light blue #5AB4FF, with navy #0E4C8A for text. The background gradient, hands and labels are blue; the gums stay pink, as anatomy.
- **Teeth:** drawn as vector illustrations (`index.html`, `TEETH`), so they're sharp at full resolution.
- **Logo:** the blue 3D logo the user supplied (`assets/logo_blue.png`, not committed). Its white background is turned into transparency in the browser ("colour to alpha"), keeping its soft shadows.
  - It sits above the clock from the start, glides into the end card's top position, and "breathes" gently (a 3.5 s cycle).
- **Clock motion:**
  - The hand steps every 1.5 s with a small overshoot.
  - The tooth it lands on bounces and glows blue, and the label pops in as a white pill.
- **End card (from 12.15 s):** the clock blurs out and the logo glides up. The rest appear in order:
  1. The clinic-name banner.
  2. "Act Early… Choose Wisely!" typewriter text.
  3. The booking button, which gets a periodic shine.
  4. Dr. Sri Sushma, MDS · Periodontist and Implantologist.
  5. Phone, website and address (the user's text).
  6. The social icons.

  Everything sits above Instagram's caption area. The card dissolves back into the clock from 20.35 s, so frame 1260 matches frame 0.
- **Song (the user asked for it, 12 Nov 2026):** the reference reel's own background song.
  - One loop (0.80–19.53 s) is cut from the user's screen recording into `assets/song_ref.wav` (not committed).
  - The reel is re-timed to it: the hand lands on the reference's own beats, and the loop is 18.73 s.
  - It is a third-party track, so Instagram may mute it. `SONG=0 bash assemble.sh` writes an SFX-only version.
- **Sound:** real CC0 recordings placed by the Real SFX skill (`sfx_cues.json`, `sfx_map.json`): a wood-block tick when the hand lands, whooshes on the transitions, typewriter keys, and soft pops and a chime for the details.
  - Critique: sync 10/10.
  - They are mixed over the song. The final mix is two-pass normalised to −14 LUFS, peak −1.4 dBTP.

## Build
```bash
node render.mjs stills 1.9 13.5 18.5   # preview frames → out/stills/
node render.mjs video 60               # 1124 frames piped into ffmpeg → out/video.mp4 (about 3.5 min)
bash assemble.sh                       # SFX pipeline → out/DrSriSushma_ToothClock_1080x1920_60fps_{MASTER,share}.mp4
```
