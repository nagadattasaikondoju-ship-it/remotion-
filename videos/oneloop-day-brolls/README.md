# "A Day at Oneloop": recovered B-rolls

The original B-roll files were lost, so these clips are cut back out of the finished 19.6 s edit
(`Adobe Express - finallll (1).mp4`, 1080×1920 60 fps).

There are 10 shots. The editor's blur/zoom transitions are trimmed, so every clip starts and ends sharp. All audio is removed.

| # | Shot | Source frames (60 fps) | Length | Captions |
|---|---|---|---|---|
| 01 | walking in (title "A Day at Oneloop") | 15–118 | 1.73 s | title, not yet removed |
| 02 | gate opening | 134–173 | 0.67 s | none |
| 03 | wooden door opening | 194–239 | 0.77 s | none |
| 04 | 9:30am checking in | 264–359 | 1.60 s | removed (draft: door edge artifacts) |
| 05 | 11am checking emails | 374–475 | 1.70 s | removed |
| 06 | 12pm scrum meet | 483–561 | 1.32 s | removed |
| 07 | 1pm heads down coding | 575–675 | 1.68 s | removed |
| 08 | 3pm bro check this bug | 689–815 | 2.12 s | removed |
| 09 | 5pm testing what we built | 816–955 | 2.33 s | removed (draft: hair artifacts) |
| 10 | 6pm wrapping up | 956–1169 | 3.57 s | not yet removed (person moves through the caption) |

## How the caption removal works
1. `extract.py` cuts each shot.
2. `masks.py` builds per-frame masks: thin bright text strokes plus their drop shadow, inside the caption strip.
3. `band.py` crops the text strip at full resolution.
4. `clean.py` aligns every frame to the middle frame (ECC affine) and builds a clean plate from all the uncovered background. Pixels never uncovered are filled with OpenCV xphoto FSR inpainting. The plate is warped back under the caption, so there's no flicker.
5. `compose.py` pastes the cleaned strip back into the full frame.

This works where the background behind the text is static. Shots 01 and 10 need flow-guided video inpainting (e.g. ProPainter), because the subject moves under the text.
