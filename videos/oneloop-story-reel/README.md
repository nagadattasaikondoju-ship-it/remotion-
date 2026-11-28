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
One shot per line, matched to what is said; plain cuts; no black frames before the end.
| Time | Picture | On screen |
|---|---|---|
| 0.0–3.3 | team testing what they built → whiteboard scrum | **WE MADE / ₹95,000 / IN 2 MONTHS** (count-up, one deep impact) |
| 3.3–4.7 | two of them arriving at the office | "A few friends in Hyderabad" |
| 4.7–5.7 | the city at night | "late nights" |
| 5.7–6.95 | on a phone call (MVI_0432) | "back-to-back calls" |
| 6.95–9.55 | the shoot crew, shooting for a brand | "building for brands that had never heard of us" |
| 9.55–12.8 | thinking at the laptop → notification pile | **TRAFFIC PROBLEM** struck → **THEY HAVE / A LEAK.** (copper drip) |
| 12.8–16.85 | opening the laptop, emails, coding | **AUDIT.** "find what's holding them back" **BUILD.** |
| 16.85–18.55 | over-the-shoulder at the laptop | **MARKET. AUTOMATE.** + **8.43× RETURN ON AD SPEND** (Google Ads, Apr–Jun 2025) |
| 18.55–19.75 | same shot, darkened | "That's OneLoop": the copper line snaps into the logo |
| 19.75–23.4 | headphones at the laptop, typing | "Developers, designers, / marketers and AI builders." |
| 23.4–24.75 | bug check | **ONE TEAM. ONE LOOP.** |
| 24.75–28.45 | logo wall | **21+ BRANDS**, the 15 client logos pop in one by one |
| 28.45–30.5 | headphones outdoors | **WE'RE JUST GETTING STARTED.** + **6,406 CONVERSIONS IN ONE MONTH** (Google Ads, March 2026) |
| 30.5–34.5 | camera operator on set | **COME GROW WITH US / @ONELOOP.IN** → logo lockup over the shot |

## Notes
- Cuts: plain cuts throughout (the user found transitions on every cut cheap).
- Voice: the WhatsApp voice note (AAC 128 kbps, cut at ~15 kHz, gated) goes through a repair chain in `assemble.sh`: warmth, de-box, presence, air, harmonic exciter, de-ess, 3:1 compression, plus a −62 dBFS room-tone bed under the gate holes. A proper re-record (lav or USB mic, sent as a file) will still sound clearly better.
- Sound: six SFX only (`sfx.py`, cue sheet in `out/CUES.md`), all low and warm, 12–18 dB under the voice: hook impact, 8.43× lift, riser and hit into the logo, swell into the logo wall, 6,406 lift, end-card sting. Synthesised, because the Ultimate Editors library isn't in the repo yet.
- Music: the user chose "Memory Reboot" (VØJ & Narvent). Pass a licensed copy with `MUSIC=`.
- Client logos (only real logos, no name tiles): radaar, bikersgear, bamboospa, lnsports, cellbay (from the user); amrplanet, antiqueloft, bikerswear, ctrlx, hydsmiles, lfe, rmc, studlyf, sushma, nirvaha (from each client's own website).
- Excluded footage:
  - Mahesh Babu film footage (les_x_bob): copyrighted.
  - Futuro Works SaaS animation: excluded by the user.
  - Day B-rolls 01 and 10: burned-in captions.
  - Client ads (TruFit, FuturoWorks) as filler under the team line: read as random.
