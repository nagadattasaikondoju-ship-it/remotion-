# Repo memory

Video editing workspace: Remotion app (`src/`, `pipeline/`) plus HyperFrames projects under `videos/<project>/`
(each has its own CLAUDE.md and scripts).

## House standards (read before any edit or sound work)
- Sound design: @docs/playbook/sound-design.md
- Short-form editing brief (captions, hooks, animations): @docs/playbook/short-form-editing.md
- One Loop brand, palette, logo and client-portfolio data: @docs/playbook/oneloop-brand.md
- Motion-graphics reference library: `docs/library/prompt-motion/README.md`.
  - Contents: all 236 Prompt Motion entries, one file per category with full prompt text, plus the site's 5 skills.
  - Installed skills: `cinetic` (cinematic launch/product films, Remotion or HyperFrames) and `product-film` (Remotion films from a product's own design system). Use them for product and launch videos.
  - taste-skill, session-story and generative-film are reference copies only.
- Wants the work done, not a long pre-approval loop. If they say "start directly", skip the blocking questions,
  but still deliver the cue sheet/breakdown alongside the result.
- Always send the finished video as a file (share copy + high-bitrate 1080×1920 master).
  They can't receive files on their desktop directly; they download from the app.
- Never fabricate client identity, payment records or press. Blur personal and client details.
  Ask before adding name tags.
- Project briefs override the house standard for that project (e.g. One Loop: no music bed, dialogue dominant).
- Ultimate Editors SFX library: not yet available in this repo. Ask for its Drive folder before a sound pass.
  Synthesised SFX are a fallback only, and the user must be told when they're used.
- Real-recording SFX tools (installed Oct 2026):
  - Skills: `real-sfx` (Clipwing: places real sounds on frames), `real-sound` and `earshot` (earshot: measures sounds the agent can't hear).
  - Library: `assets/sfx/openverse/`, CC0 sounds from Openverse/Freesound. Per-file source and licence are in `credits.json`.
    Grow it with `python3 tools/openverse_sfx.py ["query" N]`; the API is flaky, so re-run to fill categories.
  - Fresh container: `bash tools/setup_sfx.sh` installs the earshot package (pinned).
    For real-sfx, set `REAL_SFX_CONFIG=tools/real-sfx.config.json` and `REAL_SFX_INDEX=tools/real-sfx.index.json`.
  - Never run `earshot llm`: it uploads audio to Google's Gemini. Use it only if the user explicitly asks.
  - User's verdict on the story reel: few SFX, real recordings, placed only on moments that matter. 100+ synthesised clicks read as cheap.
