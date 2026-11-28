# "My name is bobbattu": kennel dogs reel

11.0 s · 1080×1920 · 60 fps · loops. A remake of the user's reference reel (a Telugu pet-name meme: a tough "Maximus Decimus Meridius"
intro, then the dog's cute names, one per shot). The hook is the reference's own Doberman shot, as the user asked; every other shot
is the kennel shoot from Drive (`docs/playbook/kennel-shoot-catalogue.md`), downloaded as the Sony originals.

## Edit (`edit.py`; cuts copied from the reference, 0.1 s before each spoken line)

| Time | Line (reference audio) | Caption | Shot |
|---|---|---|---|
| 0.00 | "My name is Maximus Decimus Meridius" | MY NAME IS MAXIMUS DECIMUS MERIDIUS (gold condensed caps) | the reference's Doberman, AI-upscaled from 512×916 |
| 1.90 | "My name is bobbattu" | My name is bobbattu 💗 | MVI_0814 from 0.85 s: Mastiff puppy comes up to the camera and smiles |
| 3.73 | "ali billi bobbattu" | ✨ ali billi bobbattu | MVI_0800 from 2.05 s: Maltese, chin cradled in a hand, looks at you, then tips its head up |
| 5.33 | "andhala bobbattu" | andhala bobbattu 🥰 (above the dog) | MVI_0805 from 0.20 s: Shih Tzu at the foot of the stairs looks away, then back |
| 7.13 | "maa nethi bobbattu" | 💗 maa nethi bobbattu | MVI_0794 from 7.00 s: Maltese trots up and looks straight up at the camera |
| 8.97 | "Lakshmi Ganapathi bobbattu" | Lakshmi Ganapathi bobbattu ✨✨ | MVI_0808 from 0.50 s: Shih Tzu lying like royalty, looking at the camera |

Shots were picked frame by frame (6 fps sheets of 20 candidate clips) for calm, close, looking-at-camera moments; no barking.
In-points were then moved to each clip's sharpest stretch (Laplacian variance of the full frame, scored every 0.05 s).

## Quality (v2, 15 Nov 2026)
v1 looked softer than the Drive files. It zoomed every shot (up to 1.22×), blew up a 1.6× crop of MVI_0805 with AI upscaling,
sharpened, and encoded the footage three times. v2 fixes all of that:
- every kennel shot is the Sony original's full frame, turned upright, at its native 1080×1920: no zoom, no crop, no upscaling, no sharpening;
- the captions are drawn as transparent frames (`node render.mjs overlay`) and composited in `base.py`, so the footage is encoded once (CRF 8);
- the MASTER is that encode untouched (stream copy). Only the share copies get one more encode (CRF 14).
The hook is the one exception: the reference's Doberman exists only at 512×916, so it stays AI-upscaled.

## Look
- **Captions** match the reference:
  - the hook in Bebas Neue (OFL) with a cream-to-gold gradient;
  - the bobbattu lines in Instrument Serif, hot pink #F2179E with a thin white outline, at the reference's size and positions;
  - emoji stickers drawn with Noto Color Emoji, sparkles twinkling.
- The reference spells one caption "andhala bobbatu"; here it is "bobbattu" like the rest.
- **The hook:** the reference is a screen recording, so a dark band covers its burned-in caption and the Instagram UI (profile bubble, sound icon), and the caption is redrawn on top in the same place.
- **Grade:** the dog shots are bright and warm; the hook keeps its own look. No push-ins (they soften the picture).

## Sound
- **Audio:** the reference reel's audio, cut to the loop (`assets/ref_audio.wav`, gitignored).
- **Real SFX** (sound pipeline), placed under it:
  - a soft pop as each 💗/🥰 sticker lands;
  - a bar-chime shimmer on the ✨ sparkles.
- **Master:** −14 LUFS.

## Outputs (`bash assemble.sh`)
- `out/Bobbattu_KennelReel_1080x1920_60fps_MASTER.mp4` and `_share.mp4`: with the reference audio.
- `_share_SFX-only-no-song.mp4`: post this one and add the sound with Instagram's "Use audio" on the reference reel, so the audio stays licensed.

## Third-party material
The hook shot and the audio belong to the creator of the reference reel. Credit them in the caption, or replace the hook with a
kennel dog before using this as paid or client work. `MVI_0811` from 6.85 s (the black Cane Corso filling the frame, slowed to 0.8×,
darkened with a spotlight on the face) was tested for this and works.
