# One Loop: story reel (1080×1920, 60 fps, 34.5 s)

The user's script, voiced in the WhatsApp VO (one continuous take, no gaps) over One Loop's own footage, with plain cuts.
It runs from the hook ("We made ₹95,000 in two months"), through the story and the method, to the team and the brands.
Every graphic sits on a line of dialogue: the Google Ads proof lands on "market it" and "we're just getting started", and the client logos pop on "25-plus brands". It ends on the CTA.

## Build
```
PYTHONPATH=/tmp/pyimg python3 build_base.py   # footage track → out/base.mp4 (needs the Drive B-rolls, see DRIVE in the script)
node render.mjs full 4                       # captions + graphics → out/ov/f_NNNNN.png (transparent, 2,280 frames)
./assemble.sh                                # VO + SFX mix + composite → out/OneLoop_Story_1080x1920_60fps_{MASTER,share}.mp4
MUSIC=track.mp3 MUSIC_IN=0 ./assemble.sh     # same, plus a music bed ducked under the VO (stems in out/stems, cue sheet in out/CUES.md)
node render.mjs stills 1.4 12.6 …            # single overlay frames for checking
```

## Screenplay (video time = VO time − 1.05 s; word times from Whisper)
| Time | Picture | On screen |
|---|---|---|
| 0.0–3.2 | testing what we built → scrum | **WE MADE / ₹95,000** (counts up on "95,000") **/ IN 2 MONTHS** |
| 3.2–9.5 | gate, door, night city, calls, BTS shoot | subtitles: a few friends in Hyderabad, late nights, back-to-back calls, building for brands… |
| 9.5–12.75 | MVI_0425 → One Loop reel notification stack | **TRAFFIC PROBLEM** (struck in copper) → **THEY HAVE / A LEAK.** (the copper full stop drips) |
| 12.75–16.85 | MVI_0424, emails, coding | **AUDIT. BUILD.** builds on each word |
| 16.85–18.55 | BTS, MVI_0431 | "market it": the stack moves up (**MARKET. AUTOMATE.**) and the proof lands below: **8.43× RETURN ON AD SPEND**, Google Ads Apr–Jun 2025, tile ringed |
| 18.55–19.70 | black | "That's one loop": the copper line traces the figure-eight and snaps into the traced logo |
| 19.70–23.30 | MVI_0440, TruFit, FuturoWorks reel, MVI_0424 | **01–04: DEVELOPERS / DESIGNERS / MARKETERS / AI BUILDERS** |
| 23.30–24.75 | bug check | **ONE TEAM. ONE LOOP.** |
| 24.75–28.45 | client logo wall | "25-plus brands": **25+ BRANDS**, 24 client tiles pop one by one, then chips **HYDERABAD · DUBAI · AUSTRALIA** on the words |
| 28.45–30.50 | MVI_0440 | "we're just getting started": **6,406 CONVERSIONS IN ONE MONTH**, Google Ads March 2026, tile ringed |
| 30.50–32.75 | BTS camera operator | **COME GROW WITH US / @ONELOOP.IN** |
| 32.75–34.50 | black | logo lockup + oneloop.in |

## Notes
- Cuts: plain cuts throughout (the user found transitions on every cut cheap).
- Sound: `sfx.py` places synthesised SFX on the cue sheet: pops, clicks and ticks on captions, logo tiles and counters; impacts on the two results; four risers with hits; a chime on the end card. There are no transition whooshes and no silent stretches. The Ultimate Editors library isn't in the repo, so these are a stand-in; swap per cue. Mix normalised to −14 LUFS, voice on top.
- Music: the user chose "Memory Reboot" (VØJ & Narvent). Pass a licensed copy with `MUSIC=`.
- Client logos: radaar, bikersgear, bamboospa, lnsports, cellbay (from the user); amrplanet, antiqueloft, bikerswear, ctrlx, hydsmiles, lfe, rmc, studlyf, sushma, nirvaha (from each client's own website). Name tiles for clients without a logo yet.
- Excluded footage:
  - Mahesh Babu film footage (les_x_bob): copyrighted.
  - Futuro Works SaaS animation: excluded by the user.
  - Day B-rolls 01 and 10: burned-in captions.
