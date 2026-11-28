# Veridale Properties — "if I handled your real estate brand's Instagram… ep. 03"

10.08 s · 1080×1920 · 60 fps. The same edit as ep. 01 (`../morrow-ig-reel`) and ep. 02 (`../aavarya-ig-reel`), applied to the user's Veridale Properties profile mock-up.

## Hook (0–2.38 s)

- Footage: the camera original of MVI_0425 from Drive, rotated to vertical, from 2.95 s in.
- What happens: he finishes typing, puts a hand to his chin and is thinking when the beat drop cuts to "his screen".
- Ep. 01 used this clip's opening typing, so this hook uses a different moment.
- Caption, in the series style:
  - lemon #FFE81A Fraunces Black, top and bottom lines bent on arcs;
  - a dark outline, shadow and soft darkening band behind it for contrast;
  - text: "if i handled / your real estate / brand's / instagram... / ep. 03".

## Profile build (from the beat drop)

One step every 2 beats (113 BPM):

1. Username, logo, link, Following button and nav avatar.
2. Bio, including the location line.
3. The six highlights.
4. Grid row 1.
5. Grid row 2.
6. Grid row 3.

During the grid steps the stats count up to the profile's own numbers: 482 posts, 56.3K followers, 47 following.

Grid wireframe labels: New launch · Brand promise · Amenities · Interior walkthrough · Brand identity · Milestones · Our process · Master plan · Sustainability.

How `index.html` works:
- The screenshot (941×1671, Lanczos-upscaled to 1080 wide) is the finished state.
- Wireframe patches sit over it, and the matching crop of the screenshot pops in over each one.
- The stats are live text.

## Sound

- The song is "DANCE…" (Slayyyter), taken from the reference recording starting at 3.73 s.
- Real CC0 SFX, run through the sound pipeline (Openverse → Real SFX → Earshot):
  - a pop on each build step ("3 Popping Pops");
  - a soft bar-chime shimmer when the grid completes ("PB Bar Chimes Long").
- Openverse refused downloads of key-jingle recordings (403 from the file host), so no key sound was added.
- The mix is two-pass loudnorm at −14 LUFS.

## Outputs

`assemble.sh` writes three files to `out/`:
- MASTER (CRF 8), with song and SFX;
- share copy, with song and SFX;
- `share_SFX-only-no-song`: post this one with Instagram's "Use audio" on the reference reel, so the song stays licensed.

## Notes

- Veridale is the user's mock-up. Post it as a concept, not as a client case study.
- The person in the hook isn't named on screen.
