# One Loop: story reel (1080×1920, 60 fps, 38 s)

The user's script, voiced in the WhatsApp VO and cut over One Loop's own footage. It runs from the hook ("We made ₹95,000 in two months"), through the story and the method (audit, build, market, automate), to the team, then 25+ brands, then a 4-second silent proof beat (client wall, then real Google Ads results), and ends on the CTA.

## Build
```
PYTHONPATH=/tmp/pyimg python3 build_base.py   # footage track → out/base.mp4 (needs the Drive B-rolls, see DRIVE in the script)
node render.mjs full 4                       # captions + graphics → out/ov/f_NNNNN.png (transparent, 2,280 frames)
./assemble.sh                                # VO mix + composite → out/OneLoop_Story_1080x1920_60fps_{MASTER,share}.mp4
node render.mjs stills 1.4 12.6 …            # single overlay frames for checking
```

## Screenplay (video time; VO word times from Whisper)
| Time | Picture | On screen |
|---|---|---|
| 0.0–3.2 | testing what we built → scrum | **WE MADE / ₹95,000** (counts up on "95000") **/ IN 2 MONTHS** |
| 3.2–9.5 | gate, door, night city, calls, BTS reflector and shoot | subtitles: a few friends in Hyderabad, late nights, back-to-back calls, building for brands… |
| 9.5–12.75 | MVI_0425 → One Loop reel notification stack | **TRAFFIC PROBLEM** (struck in copper) → **THEY HAVE / A LEAK.** (the copper full stop drips) |
| 12.75–18.55 | MVI_0424, emails, coding, BTS, MVI_0431 | **AUDIT. BUILD. MARKET. AUTOMATE.** builds on each word, the current one lit |
| 18.55–19.70 | black | "That's one loop": the copper line traces the figure-eight and snaps into the traced logo |
| 19.70–23.30 | MVI_0440, TruFit, FuturoWorks reel, MVI_0424 | **01–04: DEVELOPERS / DESIGNERS / MARKETERS / AI BUILDERS** |
| 23.30–24.85 | bug check | **ONE TEAM. ONE LOOP.** |
| 24.85–28.45 | portfolio shoots as a card pile | **25+ BRANDS**, chips HYDERABAD · DUBAI · AUSTRALIA |
| 28.45–30.45 | (no VO) | client wall: the 24 verified names from the client portfolio |
| 30.45–32.45 | (no VO) | Google Ads: 8.43 conv. value/cost (Q2 2025), 6,406 conversions (Mar 2026) |
| 32.45–36.30 | MVI_0440, BTS camera operator | **WE'RE JUST GETTING STARTED.** → **COME GROW WITH US / @ONELOOP.IN** |
| 36.30–38.00 | black | logo lockup + oneloop.in |

## Notes
- Audio is the VO only (no music bed, per the One Loop brief), cleaned and normalised to −14 LUFS. No SFX: the Ultimate Editors library isn't in the repo yet.
- The client wall uses names, not logos; swap in logo files when available.
- Excluded footage:
  - Mahesh Babu film footage (les_x_bob): copyrighted.
  - Futuro Works SaaS animation: excluded by the user.
  - Day B-rolls 01 and 10: burned-in captions.
