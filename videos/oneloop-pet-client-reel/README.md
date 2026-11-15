# One Loop × pet client: "meet the team"

25.0 s · 1080×1920 · 60 fps · 115 BPM, 12 bars. A One Loop brand reel: we signed a pet client, here's the team.
The hook and the turn are One Loop B-roll; everything between is the kennel shoot (`docs/playbook/kennel-shoot-catalogue.md`).
The kennel is never named.

```
bash assemble.sh                 # edit -> picture (one encode) -> score -> SFX -> MASTER / share / SFX-only
SKIP_PICTURE=1 bash assemble.sh  # sound and deliverables only
```

## Edit (one bar per beat of the story; every cut on a downbeat of the score)
| Bar | Time | Text | Shot |
|---|---|---|---|
| 1 | 0.00 | POV / we just signed a new client | One Loop MVI_0729 2.00: the handshake on the cafe sofa |
| 2 | 2.09 | OUR NEW CLIENT / meet the team | MVI_0814 0.85: Mastiff puppy grins into the lens |
| 3 | 4.17 | MEET THE TEAM / the boss | MVI_0771 0.85: Tibetan Mastiff stands at the mesh, waves a paw |
| 4 | 6.26 | head of security | MVI_0811 6.95: black Cane Corso comes up to the lens, tongue out |
| 5 | 8.35 | the interns | MVI_0777 4.60: one Saint Bernard hops onto the other |
| 6 | 10.43 | lunch break | MVI_0815 3.85: Mastiff puppy eating from a big steel bowl |
| 7 | 12.52 | performance bonus | MVI_0826 12.95: Shih Tzus crowd the railing for treats |
| 8 | 14.61 | brand ambassador | MVI_0808 0.50: Shih Tzu lying like royalty |
| 9–10 | 16.70 | honestly? → best client ever. | one beat each: 0770 Saint Bernards standing, 0775 Shepherds standing up, 0779 Saint Bernard up at the mesh, 0800 Maltese in a hand, 0778 fluffy dog up on the mesh, 0805 Shih Tzu at the stairs, 0832 puppy being petted, 0794 Maltese looking up |
| 11 | 20.87 | ONE LOOP / now let's make them famous | One Loop MVI_0727: the One Loop site on the laptop |
| 12 | 22.96 | pet brands, you're next. | One Loop logo on black |

**Left out on purpose:** barking or growling moments (0772, 0776 jumping, 0782 Rottweiler mouth open), the chained
Boxer (0804, 0822: reads sad), blurry or shaky clips (0796, 0828, 0836, 0838), landscape clips (0768, 0769, 0837),
0720 (the browser shows inbox and history suggestions).

## Look
- Every shot is the Sony original's own frame, upright, 1:1: no zoom, crop, upscale or sharpening. Footage, text and
  logo are composited in one pass and encoded once (CRF 8); the MASTER is that encode untouched.
- One Loop brand: cream Instrument Serif italic, copper Almarai caps overlines, logo from `oneloop-client-one`.
- Privacy: MVI_0727's browser tabs and bookmarks (a client's site name among them) sit under a moving blur band.

## Sound
- **Score** (`music.py`): composed in code for this reel, so One Loop owns it. Ukulele (Karplus-Strong), bass, soft kick,
  snaps, shaker, glockenspiel hook, a whistle doubling it in the burst; C major I–V–vi–IV with light swing. Layers come in
  a bar apart (bar levels −18.6 → −15.4 dB, no jump over 2.4 dB); drums drop for "make them famous", lands on C for the logo.
- **SFX** (sound pipeline, Real SFX library): a soft pop as each role label lands (6), a chime on the logo. SFX sit
  8 LU under the score. Master −14 LUFS, true peak −1.5 dBTP.
- `share_SFX-only-no-music`: the same SFX at their mix level, no score, for adding a trending song in Instagram.
