# "To them, you're their whole book": kennel dogs story reel

43.6 s · 1080×1920 · 60 fps. A remake of the user's reference reel (a voiceover about how much a dog's life is about us),
in its exact layout: one 1.15:1 picture box on black with the reference's rounded corners (radius 39 px, measured on its
flash frame), one small lowercase italic caption under it, hard cuts on each phrase,
a warm light-leak flash, and an orange ":)" at the end. The voiceover and music are the reference's.

## Picture quality (the user's note: "Drive quality is good, keep it")
- Every kennel and One Loop shot is cut straight out of the Sony original: a 1080×936 window of the upright frame, scaled
  down to the 1010×876 box. Nothing is enlarged, there are no zooms, no AI upscaling and no sharpening.
- The captions are drawn in the same pass, so the master's picture is compressed once (CRF 8); the share copy is one more encode.
- Every in-point was picked by measuring sharpness over each shot's length (`Laplacian variance` of the box), then checked by eye.

## Shots (`edit.py`), timed to the reference's measured cuts and caption changes
| Time | Caption | Shot |
|---|---|---|
| 0.00 | there's a very famous saying / "to you, / your pet is just a small chapter of your life | MVI_0812 Mastiff puppy in its crate turns and looks at us through the bars |
| 5.67 | but to them, | MVI_0794 Maltese trots up and looks up at you |
| 6.87 | you're their whole book" | MVI_0799 cheek to cheek with the Maltese |
| 8.70 | that hits really hard | MVI_0808 Shih Tzu lying still |
| 10.37 | because they don't get decades like we do | MVI_0816 black Cane Corso walks across the yard |
| 12.23 | they just get a few short years | MVI_0800 sleepy Maltese, face in a hand |
| 13.93 | and they spend every single one of them, / loving you.. | MVI_0832 a man crouches to pet a Mastiff puppy |
| 17.10 | (flash) | the reference's light leak |
| 17.43 | we get busy, | One Loop B-roll MVI_0719, hand writing in a diary |
| 18.60 | caught up with work and life, | One Loop B-roll MVI_0432, on a call at the laptop |
| 20.53 | but there they are, / waiting by the door, | MVI_0805 Shih Tzu waiting at the foot of the stairs |
| 22.47 | tail wagging like nothing has changed | MVI_0826 Shih Tzus crowd the railing for treats |
| 25.03 | one day you'll look around / and the house will feel a little too quiet | MVI_0809 fawn Cane Corso sitting under the trees |
| 28.60 | the floor a little too clean | the reference's empty floor (AI-upscaled from the recording) |
| 30.57 | and you'll wish you had sat down / more often just to play with them | MVI_0819 a man plays with two dogs |
| 33.60 | because to you, they were just a part of your life | MVI_0834 a Labrador and a Cane Corso eat side by side |
| 35.83 | but to them, | MVI_0779 a Saint Bernard ambles along its run |
| 37.13 | you were their whole damn universe. | MVI_0798 the Maltese's nose up to the lens |
| 39.93 | :) | black |

From the reference, only shots with no golden retriever and no person are reused (the empty floor, the light leak), as the user asked.

## Sound
The reference audio (voiceover + music), plus one real whoosh under the light-leak flash (sound pipeline). −14 LUFS.
`_share_SFX-only-no-song.mp4` is for posting with Instagram's "Use audio" on the reference reel.

## Build
`bash assemble.sh` (sources in `SRC_DIR`: `orig/` kennel originals, `ol/` One Loop originals, `up/ref_*.mp4` reference elements).
