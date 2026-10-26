# Morrow Coffee House — "if I handled your café's Instagram… ep. 01"

10.08 s · 1080×1920 · 60 fps. Recreates the reference reel's edit:
- **Hook (0–2.38 s):** Prahalad typing, with a lemon-yellow soft-serif caption, arched top and bottom lines ("if i handled / your café's / instagram..."), styled after the reference.
- **Wireframe profile (beat drop at 2.38 s):** placeholder avatar, bio, highlights and grid.
- **Fill-in:** the profile fills in one step every 2 beats (113 BPM, the song "DANCE…" by Slayyyter):
  1. name, logo and link
  2. bio
  3. highlights
  4. grid row 1 (stats count up)
  5. grid row 2
  6. grid row 3, landing on the profile's real numbers (248 / 18.6K / 612)

The reference recording is 24.6 s, but it's one 10.1 s reel looping about 2.5 times. Its cuts trail the beat by ~0.1 s; these sit exactly on it.

- `index.html`: the profile UI, rebuilt as real text and vector icons in the screenshot's own coordinates. Tiles, avatar and highlight icons are cropped from the Morrow screenshot. `seek(t)` sets every element for time t.
- `render.mjs`: `node render.mjs caption` and `node render.mjs ui` → PNG frames (Playwright).
- `assemble.sh`: hook plus UI, giving MASTER (CRF 8) + share copy without music, plus a sync PREVIEW with the reference audio as a temp track. The PREVIEW is not for posting; add the song in Instagram with "Use audio" on the reference reel.
