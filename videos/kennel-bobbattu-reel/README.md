# "My name is bobbattu": kennel dogs reel

11.0 s · 1080×1920 · 60 fps · loops. A remake of the user's reference reel (a Telugu pet-name meme: a tough "Maximus Decimus Meridius"
intro, then the dog's cute names, one per shot). The hook is the reference's own Doberman shot, as the user asked; every other shot
is the kennel shoot from Drive (`docs/playbook/kennel-shoot-catalogue.md`), downloaded as the Sony originals.

## Edit (`edit.py`; cuts copied from the reference, 0.1 s before each spoken line)

| Time | Line (reference audio) | Caption | Shot |
|---|---|---|---|
| 0.00 | "My name is Maximus Decimus Meridius" | MY NAME IS MAXIMUS DECIMUS MERIDIUS (gold condensed caps) | the reference's Doberman, AI-upscaled from 512×916 |
| 1.90 | "My name is bobbattu" | My name is bobbattu 💗 | MVI_0814: Mastiff puppy comes up to the camera and smiles |
| 3.73 | "ali billi bobbattu" | ✨ ali billi bobbattu | MVI_0800: Maltese, chin cradled in a hand, tips its head up |
| 5.33 | "andhala bobbattu" | andhala bobbattu 🥰 | MVI_0805: Shih Tzu at the stairs looks away, then back (crop 1.6×, AI-upscaled) |
| 7.13 | "maa nethi bobbattu" | 💗 maa nethi bobbattu | MVI_0794: Maltese trots up and looks straight up at the camera |
| 8.97 | "Lakshmi Ganapathi bobbattu" | Lakshmi Ganapathi bobbattu ✨✨ | MVI_0808: Shih Tzu lying like royalty, looking at the camera |

Shots were picked frame by frame (6 fps sheets of 20 candidate clips) for calm, close, looking-at-camera moments; no barking.

## Look
- **Captions** match the reference:
  - the hook in Bebas Neue (OFL) with a cream-to-gold gradient;
  - the bobbattu lines in Instrument Serif, hot pink #F2179E with a thin white outline, at the reference's size and positions;
  - emoji stickers drawn with Noto Color Emoji, sparkles twinkling.
- The reference spells one caption "andhala bobbatu"; here it is "bobbattu" like the rest.
- **The hook:** the reference is a screen recording, so a dark band covers its burned-in caption and the Instagram UI (profile bubble, sound icon), and the caption is redrawn on top in the same place.
- **Grade:** the dog shots are bright and warm; the hook keeps its own look. Slow push-ins on every shot.

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
