# One Loop: "how I'd turn 1 photo into 9 posts"
8.0 s · 1080×1920 · 60 fps · 480 frames · seamless loop. This rebuilds the user's reference reel; the breakdown is in `ANALYSIS.md`.
- **Picture:** MVI_0680 (Drive: "WRITING - Floral shirt sketching a plan in notebook, thinking, cafe"). The first 7.4 s is stretched to 8.2 s; the last 12 frames cross-fade into the first 12.
- **Overlay:** `overlay.html` has two states:
  - the hook: a sticker of one photo (the One Loop site on a laptop, MVI_0727, kept in `assets/` and gitignored) plus the line "how I'd turn 1 photo into 9 posts";
  - a 3×3 grid of nine One Loop posts built from that photo, using the reference's nine layouts in One Loop colours.
  - The cut to the grid is at 60 fps frame 184.
- **Sound:** the reference's song, one 8.0 s loop from the recording at 8.433 s, plus one real paper drop (id 17) as the grid lands. The master is −14 LUFS.
  - **The song is third-party.** If Instagram mutes it, add the same track in Instagram.
- **Build:** `SRC=<MVI_0680.mp4> bash assemble.sh` → `out/OneLoop_1Photo9Posts_1080x1920_60fps_{MASTER,share}.mp4`
- **Fonts:** Instrument Serif and Poppins 700/800 (OFL).
