# Aavarya Fine Jewellery — "if I handled your jewellery brand's Instagram… ep. 02"

10.08 s · 1080×1920 · 60 fps. Same edit as ep. 01 (`../morrow-ig-reel`), on the user's Aavarya profile mock-up.

- **Hook (0–2.38 s):** Prahalad at the laptop (MVI_0432, from 1.12 s in): he types, picks up his phone and looks at it, and the beat drop cuts to "his screen".
  - Caption keeps the series style: lemon-yellow Fraunces Black with arched top and bottom lines, and **ep. 02** kept.
  - This shot is bright and sunlit, so the letters get a dark outline and shadow, with a soft darkening band behind them, for contrast.
- **Profile build (from the drop):** one step every 2 beats (113 BPM):
  1. name, logo, link, Follow button
  2. bio
  3. highlights
  4.–6. grid row by row, with the stats counting up to the profile's own 485 / 62.4K / 8
- `index.html`: the screenshot (Lanczos-upscaled so it lands 1:1 on output pixels) is the finished state.
  - Wireframe patches sit over it, and the matching crop of the screenshot pops in over each one.
  - The stats are live text. `seek(t)` sets every element for time t.
- **Sound:** "DANCE…" (Slayyyter), lifted from the user's reference recording (from 3.73 s), plus real CC0 SFX through Openverse → Real SFX → Earshot:
  - a pop on each build step (Openverse "3 Popping Pops"; Earshot match z +4.2)
  - a wind-chime glint when the grid completes ("Wind Chime G-003"; z +4.5)
  - `sfx_cues.json` and `sfx_map.json` hold the cues. The mix is two-pass loudnorm −14 LUFS.
  - Earshot critique: launch-grade, 22/23 metrics in range. The one miss: the song is mono, because the source recording is.
  - The clip's own sound isn't used: it has speech and other music on it.
- `assemble.sh` gives:
  - MASTER (CRF 8) and share copy, both with the song and SFX;
  - a SFX-only share copy, for posting with Instagram's "Use audio" on the reference reel, which keeps the song licensed.
- Photo: the user's second Aavarya screenshot (blue Follow button, standard bottom nav), 2 Nov.
- Aavarya is the user's mock-up. Post it as a concept, not as a client case study.
