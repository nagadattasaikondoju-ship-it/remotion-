# Repo memory

Video editing workspace: Remotion app (`src/`, `pipeline/`) plus HyperFrames projects under `videos/<project>/`
(each has its own CLAUDE.md and scripts).

## House standards (read before any edit or sound work)
- Sound design: @docs/playbook/sound-design.md
- Short-form editing brief (captions, hooks, animations): @docs/playbook/short-form-editing.md
- One Loop brand, palette, logo and client-portfolio data: @docs/playbook/oneloop-brand.md
- One Loop Instagram: what gets views and leads (measured Nov 2026), episode slate: `docs/playbook/oneloop-instagram.md`
- Skills knowledge base (all project skills by job, with sources and routing): `docs/skills-knowledge-base.md`. Regenerate with `python3 tools/build_skills_kb.py` after installs.
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
- Lemo-Opuscar (github.com/lemomo-ai/lemo-opuscar, MIT; films and styles CC BY 4.0): skill `lemo-opuscar` with 99 code-made film styles (library updated to f2471ca, 12 Nov 2026).
  - Keep the library in the repo: `LEMO_OPUSCAR_HOME=/home/user/remotion-/tools/lemo-opuscar sh .claude/skills/lemo-opuscar/scripts/setup.sh` (gitignored, re-fetch per container).
  - The user approved its render packages (Oct 2026). In a fresh container, `cd tools/lemo-opuscar`, then run `npm install` and create `.venv` with python3.12 from `requirements.txt`.
    Skip `setup.sh deps`: it downloads a second browser.
  - Use the preinstalled browser with `PLAYWRIGHT_CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. A test render of swiss-motion works.
  - Fonts aren't in the library: download each film's OFL fonts from github.com/google/fonts into its `fonts/` folder.
  - WebGL is software-rendered here, so 3D styles render slowly. Its ffmpeg check wants 7+; this container has 6.1.
  - Its sound still goes through the sound pipeline below.
- Imported motion and editing skills (Oct 2026): 119 skills from 30 repos.
  - `tools/skill-repos.json` lists each skill's source repo and licence. `python3 tools/install_skill_repos.py` re-installs them all at pinned commits.
  - Unlicensed repos (krusemediallc, tenfoldmarc, iart generative-illustration) are git-ignored: used locally, not re-published.
  - Reference-only clones (After Effects MCP and aftr need the user's desktop After Effects; Claude-Editor) live in `tools/skill-repos/`.
  - Routing when skills overlap: this repo's house rules and playbooks win.
    - Talking-head reels: `branded-ad-edit`, `reel-recut`, `tenfold-video-edit`; QA with `video-qa`.
    - Charts and stats: `chart-animation`, `animated-chart`.
    - Captions: `caption-animation`, `embedded-captions`.
    - Remotion: `remotion-best-practices` (router). Brand system: `brand-intake`, `brand-motion-guidelines`.
    - Critique: `motion-design-critique`.
  - Sound always goes through the pipeline below, not `km-sound-design` or `dsk-elevenlabs`. ElevenLabs, Arcads, RunPod and Ideogram need paid API keys; ask first.
- Nov 2026 skills (7 repos, all MIT, read for hooks / settings / prompt-steering, pinned in `tools/install_skill_repos.py`):
  `huashu-motion`, `rossark-motion-skill`, `take-one`, `reanimate`, `argo-guide`, `explainroo`, `video-director`. earshot (same batch) was already installed.
  - Fresh container: `python3 tools/install_skill_repos.py --only <owner/repo,…>` re-clones them, then `bash tools/setup_skill_clis.sh` builds `om`, `explainroo`, `argo` from those clones (never from npm), installs reanimate's bun deps, links Chromium paths and fixes Pillow.
  - Browsers (no second download): `OM_CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome` for `om`; `EXPLAINROO_CHROME=` the same path for explainroo; `PLAYWRIGHT_BROWSERS_PATH=tools/pw-compat` for reanimate's scripts (never run its `setup.sh`, it downloads Chromium).
  - **Never add huashu-motion's "Made with huashu-motion" end signature** to the user's or a client's film unless the user asks.
  - Use `om` from PATH, not `npx huashu-motion` (that pulls unreviewed code from npm).
  - Paid generation (take-one's Higgsfield/Seedance/Kling/Suno/ElevenLabs routes, argo's OpenAI/ElevenLabs/Gemini TTS): ask first, as for every paid API. Local voices only by default (explainroo Kokoro, argo `kokoro-js`).
  - Routing: launch film from a site → `huashu-motion`; product-in-use / ad / music video with a reviewer → `take-one`; app demo with voiceover → `argo-guide`; word-synced explainer → `explainroo`;
    copy an animation from a site/video/GIF → `reanimate`; mascot/icon/logo idle motion → `rossark-motion-skill`; direction + QA on any coded video → `video-director` (`scripts/qa_video.py`, `check_timeline.py`).
  - House rules still win (sound pipeline, captions, One Loop brief, no fabricated clients). Their sound goes through the pipeline below.
- `directing-stickman-videos` (kaomei/stickman-video-director @ eb4bb37, MIT; Nov 2026). Installed with `python3 tools/install_skill_repos.py --only kaomei/stickman-video-director`.
  - **Director mode (A1–A5):** approved storyboards plus standalone ~10 s prompts for Gemini Omni Flash clips. Free to use here.
  - **Autopilot (B1–B4) and A6:** call Google's Gemini API (`scripts/gemini-media.mjs`, needs `GEMINI_API_KEY`) for images, TTS and video. This is paid generation that uploads prompts and media to Google, so ask first. The key goes through `request_credential`, never the chat.
  - Its sound rules don't replace this repo's sound pipeline.
- **Sound pipeline for EVERY video (user's standing rule):**
  1. Openverse API (`tools/openverse_sfx.py`): search and fetch real recorded SFX (CC0).
  2. Real SFX skill (`real-sfx`): analyse the video and place the sounds on the timeline.
  3. Earshot (`earshot` / `real-sound`): analyse the placed sounds, generate and refine any missing ones, and QA the mix.

  The output is a professionally sound-designed video. Don't hand-synthesise SFX outside this pipeline.
- Real-recording SFX tools (installed Oct 2026):
  - Skills: `real-sfx` (Clipwing: places real sounds on frames), `real-sound` and `earshot` (earshot: measures sounds the agent can't hear).
  - Library: `assets/sfx/openverse/`, CC0 sounds from Openverse/Freesound. Per-file source and licence are in `credits.json`.
    Grow it with `python3 tools/openverse_sfx.py ["query" N]`; the API is flaky, so re-run to fill categories.
  - Fresh container: `bash tools/setup_sfx.sh` installs the earshot package (pinned).
    For real-sfx, set `REAL_SFX_CONFIG=tools/real-sfx.config.json` and `REAL_SFX_INDEX=tools/real-sfx.index.json`.
  - Never run `earshot llm`: it uploads audio to Google's Gemini. Use it only if the user explicitly asks.
  - User's verdict on the story reel: few SFX, real recordings, placed only on moments that matter. 100+ synthesised clicks read as cheap.
