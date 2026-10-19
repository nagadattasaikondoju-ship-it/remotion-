# One Loop — "Client #1" founder-story reel

1080×1920 · 30 fps · 46.3 s · see `EDIT_PLAN.md` for the edit thinking.

Rebuild (needs the original uploads + Drive B-roll at the paths in `scripts/edl.py`):

1. Clean dialogue with DeepFilterNet3 → `*_dn.wav` (WhatsApp phone recording replaces the 0658 camera audio, +1.91 s sync).
2. `python3 scripts/prep_stills.py` — redacts the ₹1,500 receipt, crops the "not available" screen and logo.
3. `python3 scripts/build_cut.py` — rotated, face-framed, graded, denoised picture cut → `assets/base.mp4`.
4. `python3 scripts/build_audio.py` — dialogue edit + natural B-roll sound + restrained SFX → `assets/audio/master.wav` (−14.5 LUFS, no music).
5. `python3 scripts/build_html.py && npx hyperframes@0.8.78 render -f 30 --crf 12 -o renders/hf.mp4`, then mux `master.wav`.

`scripts/edl.py` is the single source of truth: every cut, overlay and caption is anchored to a spoken word.
