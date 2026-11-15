# "They look scary but they're babies": kennel dogs reel (edited in invideo)

10.3 s · 1080×1920 · 60 fps. A remake of the user's reference reel (the "THIS IS YOUR SIGN TO EXPLORE" travel format:
five letterbox strips stack up one word at a time on the clicks, the last word lands alone on black, then full-screen
shots run under it). The whole edit lives in invideo, project "Original footage":

- Timeline: https://invideo.io/@oneloops-workspace/original-footage/tree/main/seq-2.1
- Footage: the kennel shoot (`docs/playbook/kennel-shoot-catalogue.md`), uploaded by the user to the same project. The
  copy there is byte-identical to the Drive originals (checked: same MD5 as MVI_0800 from Drive).

## The idea (text research)
The user's note: the caged dogs look ferocious, but with the barking muted they are cute, hopping on each other. Research
(Nov 2026) shows "big scary dog is secretly a baby" is one of the most shared dog formats (DogTime on two "dangerous"
Bullies playing as "two big babies"; an XL Bully "just a baby" clip; a tough Cane Corso that "melts into a total baby").
So the strips build the setup over the toughest-looking dogs and the reveal word lands on the playful moments:

**THEY / LOOK / SCARY / BUT / THEY'RE** → **BABIES**

Alternatives kept for later: "THEY ONLY KNOW HOW TO LOVE" (same 5 + 1 shape), "BIG SCARY DOGS ARE JUST BABIES".

## Layout (measured on the reference, frame by frame)
- Strips: five full-width bands, 336 px tall with 24 px gaps, at y 77 / 437 / 797 / 1157 / 1517 (reference: 165 px bands at
  y 38–906 of its 530×942 recording, scaled ×2.038).
- Each strip is the upright Sony frame at native size (rotation −90°, zoom 1.7778 = 1:1 pixels), cut to a 336 px band with
  invideo's crop effect and moved into place. Nothing is enlarged.
- Words: Gilda Display (OFL), white, 117 px (82 px caps, the reference's size), centred in each strip, soft dark shadow.
  Italiana was tried first (closest shape) but too thin to read over the mesh and the white dog.
- Grade: one adjustment layer, vibrance +0.18, temperature +0.05.

## Edit (60 fps frames; every cut is on the reference's own frame)
| Time | Frame | Event | Clip (source in → out) |
|---|---|---|---|
| 0.333 | 20 | strip 1 + THEY | MVI_0773 0.00–3.90: black German Shepherds standing at the mesh (band y 620) |
| 1.100 | 66 | strip 2 + LOOK | MVI_0810 1.00–4.53: black Cane Corso on a chain, staring (band y 850) |
| 1.867 | 112 | strip 3 + SCARY | MVI_0820 6.00–8.77: black Cane Corso in profile, chain collar (band y 1000) |
| 2.567 | 154 | strip 4 + BUT | MVI_0809 8.25–10.32: cream Cane Corso, cropped ears, staring (band y 700) |
| 3.333 | 200 | strip 5 + THEY'RE | MVI_0776 2.30–3.60: long-coat German Shepherd at the mesh (band y 640) |
| 4.233 | 254 | strip 1's picture drops out, THEY stays on black | — |
| 4.633 | 278 | all clear: BABIES alone on black | — |
| 5.133 | 308 | full screen | MVI_0777 4.75–5.75: one Saint Bernard hops onto the other |
| 6.133 | 368 | full screen | MVI_0775 0.00–0.97: Shepherd and black Shepherd standing up together, tongue out |
| 7.100 | 426 | full screen | MVI_0771 0.85–1.88: Tibetan Mastiff standing at the mesh, waving a paw |
| 8.133 | 488 | full screen | MVI_0770 7.90–8.90: two Saint Bernards standing up side by side |
| 9.133 | 548 | full screen | MVI_0814 0.95–2.02: Mastiff puppy grinning, tongue out |
| 10.200 | 612 | black to the end (10.28) | — |

Clip picks: every cage clip (MVI_0768–0782) and the tough-dog clips (0804, 0809–0811, 0816, 0820, 0822) were read at
3 fps; each strip band was checked across its whole on-screen time so the dog stays inside it.

## Sound
- The reference's own audio (no words): a camera click on every strip, then a whistled tune from ~5 s. It is uploaded to
  the project (`reference_audio.wav`) and placed from 0, so every strip lands on its click. Camera sound is muted.
- Sound pipeline: no SFX were added, because the reference track already carries a real click on each strip (the user's
  rule: few sounds, only where they matter). QA: clicks lead each strip by 0–4 frames, as in the reference; the mix is
  normalised to −14 LUFS on export.
- The audio belongs to the reference's creator: post with Instagram's "Use audio" on the reference reel (the no-audio file),
  or credit the creator.
