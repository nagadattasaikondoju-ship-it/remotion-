# One Loop: "What I check first in your ad account"
12.7 s · 1080×1920 · 60 fps · 762 frames · seamless loop. This rebuilds the user's reference reel; the breakdown is in `ANALYSIS.md`.
- **Picture:** MVI_0432 (Drive: "WORK - Green polo on phone call at laptop, terrace wide"), stretched 11.81 → 12.7 s.
- **Overlay:** `overlay.html` holds the hook plus nine checklist steps, using the reference's text and card contents verbatim. Each step sits on a near-black/red grade.
  - Hard cuts at 60 fps frames 0, 198, 258, 324, 378, 434, 504, 576, 642, 712 → 762.
- **Sound:** the reference's song, one 12.7 s loop cut from the recording at 10.967 s and kept in `assets/` (gitignored).
  - Nine real CC0 key taps (library ids 33/34/37) are placed by Real SFX, one per step, at about −10 dB under the song.
  - The master is −14 LUFS.
  - **The song is third-party.** If Instagram mutes it, pick the same track in Instagram's audio picker.
- **Build:** `SRC=<MVI_0432.mp4> bash assemble.sh` → `out/OneLoop_AdAccountCheck_1080x1920_60fps_{MASTER,share}.mp4`
