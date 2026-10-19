# One Loop — "Client #1" founder-story reel

1080×1920 · 30 fps · 47.8 s. Edit thinking: `EDIT_PLAN.md`. Every caption: `CAPTION_MAP.md`. Every speaker change and SFX: `TRANSITIONS.md`.

## Caption system (why not everything is behind the speaker)

- **Behind the speaker** (roto-masked, the person stays in front) — only the story's big beats:
  "mattered a lot to us", "every door", "slowed down", "and then nothing", "neither.", "professionally."
- **Clean phrase above the head** (in front of the background, never on the face or hands) — the regular reading lane.
- **Pinned to the surface** in B-roll (pavement, road, facade, café wall, foliage) with planar tracking.
- **Above the proof** for the ₹1,500 receipt and the "website held offline" screen; **low** only where a shot has no headroom.
- Key words in One Loop copper; Playfair italic only for the emotional words.

## Rebuild

Needs the original uploads + Drive B-roll at the paths in `scripts/edl.py`.

1. DeepFilterNet3 (full suppression) → `*_dn.wav` (the WhatsApp phone take replaces the 0658 camera audio, +1.91 s sync).
2. `python3 scripts/prep_stills.py` — redacts the ₹1,500 receipt, crops the "not available" screen and logo.
3. `python3 scripts/build_cut.py` — rotated, face-framed, graded, denoised picture cut, J-cuts, whip blur → `assets/base.mp4`.
4. `python3 scripts/build_audio.py` — dialogue edit, Tarun/Prahalad match, ambience beds, 7 SFX → `assets/audio/master.wav`.
5. `python3 scripts/track.py` — faces + planar tracks on the cut.
6. `python3 scripts/build_html.py` → `python3 scripts/make_cutouts.py` → `python3 scripts/build_html.py` (cut-outs for behind captions).
7. `npx hyperframes@0.8.78 render -f 30 --crf 12 -o renders/hf_v2.mp4`, then mux `master.wav`; `python3 scripts/audit.py`, `python3 scripts/qa_sheet.py <final>`.
