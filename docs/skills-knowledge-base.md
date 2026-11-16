# Skills knowledge base

Generated 2026-11-16 by `python3 tools/build_skills_kb.py` from every `.claude/skills/*/SKILL.md` in this repo. **209 project skills.** Re-run the script after installing or removing skills.

## How the skills fit together (house rules win)

- **Read first, every job:** `CLAUDE.md`, `docs/playbook/sound-design.md`, `docs/playbook/short-form-editing.md`, and `docs/playbook/oneloop-brand.md` for One Loop work.
- **Sound for every video:**
  1. Openverse (`tools/openverse_sfx.py`, CC0 recordings)
  2. `real-sfx` (place sounds on the frame)
  3. `earshot` / `real-sound` (analyse, refine, QA the mix)
  - Never hand-synthesise SFX outside this pipeline.
  - Never run `earshot llm` (it uploads audio to Gemini) unless asked.
- **Paid APIs, ask first:** ElevenLabs, Arcads, RunPod, Ideogram, OpenArt, LTX, Higgsfield/Seedance/Kling/Suno (take-one), and the cloud TTS options in argo. Local voices by default (explainroo Kokoro, argo `kokoro-js`).
  - Nov 16 batch: ElevenLabs in `jhonty-video-editing`, `extreme-motion-design` (optional; it also offers local TTS) and `motion-video-production` (via composio, or Fish Audio); `motion-video` uses the `multix` CLI (Gemini TTS + ElevenLabs); fal.ai in `ecc-video-editing`; OpenAI/ElevenLabs TTS in `video-production`; YouTube OAuth in `youtube-stats`; Modal/Hugging Face GPUs in `parody-short`.
  - AutoMontage: `ai-promo` spends Higgsfield credits (OAuth MCP); `am-motion-reel` uses ElevenLabs only with `--accept-provider-cost`. Its Anthropic/OpenAI scripts are legacy opt-ins: don't use them.
  - **Never post anywhere** without the user's explicit go: `video-shotcraft` can publish to social platforms (Upload-Post API) and `video-production` can host files over Tailscale.
- **Never add** huashu-motion's "Made with huashu-motion" signature. Use `om` from PATH, never `npx huashu-motion`.
- **Browsers:** use the preinstalled Chromium (`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`):
  - `OM_CHROME` / `EXPLAINROO_CHROME` / `PLAYWRIGHT_CHROME` point at it;
  - for reanimate, `PLAYWRIGHT_BROWSERS_PATH=tools/pw-compat`;
  - never install a second browser.
- **Fresh container:**
  - `python3 tools/install_skill_repos.py` (all pinned repos), or `--only owner/repo,…`;
  - `bash tools/setup_skill_clis.sh` (om, explainroo, argo, reanimate deps, Pillow fix);
  - `bash tools/setup_sfx.sh` (earshot);
  - Lemo-Opuscar library per CLAUDE.md.
- **Deliverables:** always a share copy and a high-bitrate 1080×1920 master, sent as files. Never fabricate clients, payments or press. Ask before name tags.

### Which skill for which job (the routing used in this repo)

| Job | First choice | Also useful |
|---|---|---|
| Talking-head reel (captions, punch-ins, overlays) | `branded-ad-edit`, `reel-recut`, `tenfold-video-edit` | `talking-head-recut`, `embedded-captions`, `video-qa` |
| Captions | `caption-animation`, `embedded-captions` | `kinetic-typography`, `tiktok-lower-thirds` |
| Launch film from a website | `huashu-motion` | `cinetic`, `product-film`, `cg-launch-video` |
| Product-in-use film / ad / music video with a reviewer | `take-one` | `ad-creative-video`, `music-to-video` |
| App demo with voiceover | `argo-guide` | `product-demo-video`, `playwright-recording` |
| Word-synced explainer with a free local voice | `explainroo` | `explainer-video`, `vox-explainer`, `whiteboard-animation` |
| Copy an animation from a site / video / GIF | `reanimate` | `reference-to-motion`, `reel-style-clone` |
| Mascot / icon / logo idle motion | `rossark-motion-skill` | `logo-animation`, `svg-animation` |
| Code-made film in a named style (66 styles) | `lemo-opuscar` | `cinetic` |
| Charts and stats | `chart-animation`, `animated-chart` | `animated-infographic`, `diagram-animation` |
| Remotion | `remotion-best-practices` (router) | `remotion-video`, `dsk-remotion` |
| HyperFrames | `hyperframes` | `hyperframes-cli`, `hyperframes-animation` |
| Brand system | `brand-intake`, `brand-motion-guidelines` | `color-motion` |
| Direction and QA of any coded video | `video-director` (`scripts/qa_video.py`, `check_timeline.py`) | `motion-design-critique`, `video-qa` |
| Sound | the pipeline above (`real-sfx`, `earshot`, `real-sound`) | (not `km-sound-design` / `dsk-elevenlabs`) |
| Trim real footage: silence, dead air, motionless stretches | `auto-editor` (CLI) | `auto-editor-effects`, `auto-editor-transitions`, `auto-editor-export` (Premiere/Resolve/FCP XML) |
| Probe, reframe, loudness, platform checks with ffmpeg | `ffmpeg-skill` (`scripts/*.py`, `check.py --platform reels`) | `dsk-ffmpeg`, `boring-tools` (edit-as-text renders) |
| Find the shots inside long clips | `scenedetect` CLI (PySceneDetect) | `beat-sync-edit`'s `clip_tag.py` (motion/energy tags) |
| Montage cut to a song's beats | `beat-sync-edit` (beat map → EDL → render, flashes, speed ramps) | `beat-sync-editing` (principles), `music-to-video` |
| Motion graphics over real footage in Remotion (SRT captions, jump cuts, audio-peak hits) | `remotion-ffmpeg-skill` (needs `ffmpeg-skill`) | `remotion-bits` (ready-made Remotion components) |
| Cinematic product promo from a web page (shot cards, 2.5D camera) | `video-shotcraft` | `huashu-motion`, `cinetic` |
| Editor judgment: pacing, hooks, LUFS, J/L cuts, CC0 SFX and music | `editing-videos` (ships a 128-file CC0 sound library) | `short-form-video` |
| Talking-head reel with face layouts, PiP, kinetic text | `reel-editor` | `boring-tools`, `branded-ad-edit` |
| Long horizontal YouTube edit (chapters, jump cuts, subtitles) | `youtube-editor` | `auto-editor` |
| Match a reference video with measured targets | `motion-video-production` | `reel-style-clone`, `reanimate` |
| Showreel-grade motion in HyperFrames | `hyperframes-motion-reel` | `motion-video`, `hyperframes-animation` |
| How a video looks: palette by act, type scale, contact-sheet critique | `video-design` | `motion-design-critique` |
| Turnkey talking-head reel on an engine (transcript, rough cut for approval, scene brief, render, QA) | `reel-turnkey` (AutoMontage, `automontage` CLI) | `reel-from-donor` (rebuild a useful reel's mechanics as your own cards), `am-motion-reel` (no-camera reel from a script or voice-over) |

## Index by job

### After Effects, Blender and desktop apps (6)

| Skill | What it does | Source |
|---|---|---|
| [`after-effects`](#after-effects) | This skill should be used when the user asks anything about Adobe After Effects — to "write an After Effects expression", "make a wiggle / loopOut / inertial bounce", "r… | iart-ai/motion-design-skills |
| [`aftereffects-motion`](#aftereffects-motion) | Use this skill whenever Adobe After Effects is the working tool. | LobzyJay/motion-design-with-claude |
| [`blender`](#blender) | 3D scenes, character acting and product shots from a shot spec, rendered in Blender, as a finished film, as clips for any other build (moviepy, a video job, an editor), … | digitalsamba/claude-code-video-toolkit |
| [`blender-motion`](#blender-motion) | Use this skill whenever Blender is the working tool. | LobzyJay/motion-design-with-claude |
| [`capcut-export`](#capcut-export) | Export a finished layered edit (footage + graphic cards + alpha fx overlay + captions + SFX/music/VO) into a CapCut desktop draft where EVERY element stays editable — fo… | krusemediallc/video-editor-agent |
| [`figma`](#figma) | Import Figma content into a HyperFrames composition — rendered assets, brand tokens, components, storyboard sections → reconstructed motion (frames read as states, not s… | earlier install |

### Footage editing: cuts, ffmpeg, scenes, beat sync (14)

| Skill | What it does | Source |
|---|---|---|
| [`auto-editor`](#auto-editor) | Record a microphone or edit video/audio with the auto-editor CLI — cut out dead space (silence, motionlessness, black frames), set the pace, make manual cuts, and render… | WyattBlue/auto-editor |
| [`auto-editor-effects`](#auto-editor-effects) | Apply actions and animations to sections of a video/audio with auto-editor — change speed, duck or fade volume, de-ess, zoom/Ken Burns, rotate/spin, draw boxes, overlay … | WyattBlue/auto-editor |
| [`auto-editor-export`](#auto-editor-export) | Export auto-editor's edit or microphone recording to a video editor (Premiere, DaVinci Resolve, Final Cut Pro, ShotCut, Kdenlive), to individual clips, or to auto-editor… | WyattBlue/auto-editor |
| [`auto-editor-transcribe`](#auto-editor-transcribe) | Transcribe a media file or live microphone to text or subtitles with auto-editor's whisper subcommand, then edit by spoken content — cut to keep (or drop) sections whose… | WyattBlue/auto-editor |
| [`auto-editor-transitions`](#auto-editor-transitions) | Add transitions at auto-editor's cuts — cross-dissolves, Premiere Pro's transitions (push, clock-wipe, glitch, page-peel, iris-round, and the rest, including its Legacy … | WyattBlue/auto-editor |
| [`beat-sync-edit`](#beat-sync-edit) | Turn a song + raw footage into a beat-synced edit. | ZiadAbdelkarim/beat-synced-edit |
| [`boring-tools`](#boring-tools) | Edit video as text. | brookejlacey/boring-tools |
| [`dsk-ffmpeg`](#dsk-ffmpeg) | Video and audio processing with FFmpeg. | digitalsamba/claude-code-video-toolkit |
| [`ecc-video-editing`](#ecc-video-editing) | AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. | KirttiVushan/claude-code |
| [`editing-videos`](#editing-videos) | Gives an editor's judgment, with sourced numbers, for cutting and pacing, J and L cuts, jump cuts, b-roll, hooks and retention, captions, on-screen text and graphics, zo… | kmilo93sd/agent-video-editor |
| [`edl-tighten`](#edl-tighten) | - Surgically remove awkward pauses, dead air, and long silences from a FINISHED voiceover-driven cut while keeping video, VO audio, word-synced captions, SFX hits, and t… | krusemediallc/video-editor-agent |
| [`ffmpeg-skill`](#ffmpeg-skill) | Edit video and audio with local FFmpeg: cut, join, reframe, speed, captions, overlays, silence removal, sync, loudness, HDR to SDR, platform exports and checks. | kajisho5/ffmpeg-skill |
| [`jhonty-video-editing`](#jhonty-video-editing) | Make and edit short-form videos (Reels, TikToks, Shorts, video ads, explainers, VSLs) with Remotion, ElevenLabs and 21st.dev. | JhontyBarreto/video-editing-skill |
| [`remotion-ffmpeg-skill`](#remotion-ffmpeg-skill) | Make motion graphics on real footage with Remotion, driven by measurements from ffmpeg-skill: animated captions timed from an SRT/VTT file, automatic jump cuts that drop… | kajisho5/remotion-ffmpeg-skill |

### End-to-end motion-graphics video pipelines (14)

| Skill | What it does | Source |
|---|---|---|
| [`adu-motion-video`](#adu-motion-video) | 使用完整动画工程包，把新口播、文案与自有素材制作成可编辑动效视频和 60fps MP4；也支持轻量 TPL、手绘续接、字幕与改旧片。支持 Windows、macOS、Linux，以及 Codex、Claude Code、豆包、DeepSeek、WorkBuddy 等可读写文件并运行命令的助手。 | adunext/adu-motion-video |
| [`am-motion-reel`](#am-motion-reel) | - Создаёт анимационный Reels/Shorts без камеры из темы, сценария или готовой озвучки в AutoMontage-Agent: script, выбор аудио, таймкоды, motion brief, настоящий preview,… | mcdenil-skills/AutoMontage-Agent |
| [`extreme-motion-design`](#extreme-motion-design) | Cria vídeos de motion design de nível de estúdio por código (Remotion/React), com trilha licenciada, SFX sincronizados, voz opcional (ElevenLabs ou modelo TTS local esco… | dev-isaacmello/extreme-motion-design |
| [`hyperframes-motion-reel`](#hyperframes-motion-reel) | ショーリール品質（Behance / OFFF / Awwwards級）のモーショングラフィックス動画を HyperFrames（HTML + GSAP + SVG + Canvas、Apache-2.0）で制作する。remotion-motion-reel の HyperFrames 版で、Remotion の Company Lic… | Sunwood-ai-labs/hyperframes-motion-reel-skill |
| [`motion-reel`](#motion-reel) | Make motion-graphics videos rendered entirely from code — product ads, brand promos, launch videos, showreels, animated explainers, 抖音/视频号/小红书 竖屏广告, 宣传片, 片头, 动态海报视频 — wi… | 10291124jcjc-dotcom/motion-reel |
| [`motion-video`](#motion-video) | Produce beat-synced 1080p motion-graphic videos in HyperFrames (HTML + GSAP) with an AI voice-over, Vietnamese karaoke captions, SFX and generated music, in one of two p… | bestagentkits/motion-video-skill |
| [`motion-video-director`](#motion-video-director) | Plan, direct, and produce code-drawn 2D/3D motion graphics and edited videos (reels, hooks, SaaS/product explainers, talking-head edits) on the user's local machine thro… | mattypark/Motion-graphics-skill |
| [`motion-video-production`](#motion-video-production) | Plan, build and verify 15–90 second motion graphics, promo and character videos. | unclejobs-ai/motion-video-skill |
| [`parody-short`](#parody-short) | Comedy shorts about a group's own life - a team's launch, quarter end, office move or leaving do; a club's season; a class's year; a family's Christmas - or about a shar… | digitalsamba/claude-code-video-toolkit |
| [`remotion-video`](#remotion-video) | This skill should be used when the user asks to "make a video with Remotion", "create a programmatic/data-driven video in React", "render an MP4/GIF from code", "animate… | iart-ai/motion-design-skills |
| [`remotion-video-director`](#remotion-video-director) | Interactive guide for creating Remotion videos - from strategic concept to rendered MP4. | BayramAnnakov/remotion-video-director |
| [`video-motion-craft`](#video-motion-craft) | Create and edit video with cinematic motion — Remotion (React video) for motion graphics, reels, intros, promos, titles and game trailers, plus FFmpeg/Whisper for editin… | vibegameengine/video-motion-craft |
| [`video-production`](#video-production) | End-to-end narrated video production with research, source extraction, storyboard/script, Manim/ffmpeg visuals, TTS voiceover, QC, archival backups, and optional local/T… | Aaryan-Kapoor/video-production-skill |
| [`video-shotcraft`](#video-shotcraft) | Create cinematic product videos from frontend projects or webpages with Remotion, real page captures, shot cards, the Ink Press template, beat sync and sound design. | Vincentwei1021/video-shotcraft |

### Delivery, export and QA (5)

| Skill | What it does | Source |
|---|---|---|
| [`reel-export`](#reel-export) | Turn any horizontal or square motion video into a 1080 x 1920 Instagram Reel or TikTok that uploads cleanly. | charlie947/motion-graphics-skills |
| [`video-delivery-specs`](#video-delivery-specs) | This skill should be used when the user asks "what are the specs for Instagram Reels / TikTok / YouTube / broadcast", "export settings for social", "what aspect ratio an… | iart-ai/freelance-motion-skills |
| [`video-qa`](#video-qa) | - Four-layer QA for a rendered video edit — run it on any .mp4/.mov you or a pipeline just produced. | krusemediallc/video-editor-agent |
| [`video-review-canvas`](#video-review-canvas) | Publish a finished (or draft) video cut to a frame.io-style review canvas on here.now — a player with a frame-accurate scrubber, persistent timeline notes, version compa… | krusemediallc/video-editor-agent |
| [`youtube-stats`](#youtube-stats) | How published videos are doing on YouTube, and what to learn from it. | digitalsamba/claude-code-video-toolkit |

### Sound, music and audio QA (11)

| Skill | What it does | Source |
|---|---|---|
| [`acestep`](#acestep) | AI music generation with ACE-Step 1.5 — background music, vocal tracks, covers, stem extraction, audio repainting, and continuation for video production. | digitalsamba/claude-code-video-toolkit |
| [`ai-audio-sound-design`](#ai-audio-sound-design) | Rebuild the audio of an AI-generated video (Arcads / AI actors / UGC-gen / any clip whose voices sound like sterile studio AI) so every scene sounds like it was really f… | krusemediallc/video-editor-agent |
| [`audiogram`](#audiogram) | This skill should be used when the user asks to "make an audiogram", "turn a podcast into a video", "create a waveform video", "make a podcast clip video", "convert audi… | iart-ai/youtube-video-skills |
| [`dsk-elevenlabs`](#dsk-elevenlabs) | Generate AI voiceovers, sound effects, and music using ElevenLabs APIs. | digitalsamba/claude-code-video-toolkit |
| [`earshot`](#earshot) | Listen with earshot whenever you must judge, choose, trim, verify or compare sound you cannot hear - picking a sound effect, music or ambience from candidates, finding t… | earlier install |
| [`hyperframes-audio`](#hyperframes-audio) | Use when audio already placed in a HyperFrames composition needs to be mixed: fade-in/fade-out, crossfade, track gain or volume, volume automation, ducking, a music bed … | earlier install |
| [`km-sound-design`](#km-sound-design) | Generate and mix the full audio pass for a video edit with ElevenLabs — an SFX kit (whooshes, pops, impacts, count-ups, sub-drops, risers) generated, audited for the ~1/… | krusemediallc/video-editor-agent |
| [`music-to-video`](#music-to-video) | Turn a music track (an audio file, a video to pull audio from, or a track generated from a mood brief) into a beat-synced video — lyric video, slideshow, or kinetic prom… | earlier install |
| [`real-sfx`](#real-sfx) | Sound design for motion videos with REAL recorded sounds from the user's own libraries (a sorted main pack of whooshes, hits, risers, pops, chimes, keystrokes, foley, am… | earlier install |
| [`real-sound`](#real-sound) | Build premium, realistic soundtracks for code-made videos and animations from real licensed recordings - launch films, product and feature videos, UI walkthroughs, logo … | earlier install |
| [`soundtrack`](#soundtrack) | This skill should be used when the user asks to "add music to the animation", "make the music in code", "synthesize a soundtrack", "compose background music that fits th… | iart-ai/javascript-animation-skills |

### Talking-head and short-form reel editing (22)

| Skill | What it does | Source |
|---|---|---|
| [`arcads-video-edit`](#arcads-video-edit) | Turn a creator's multi-take product-demo recordings (each take = screen recording + camera video + mic WAV, usually the creator walking through Arcads) into a finished 9… | krusemediallc/video-editor-agent |
| [`branded-ad-edit`](#branded-ad-edit) | Turn a RAW talking-head video into a FINISHED, branded, motion-graphics ad for any brand or industry — a designed motion graphic on every spoken line, the brand's real c… | krusemediallc/video-editor-agent |
| [`edits-hook-overlay`](#edits-hook-overlay) | Put Instagram's NATIVE text hook (the Edits app's own font, boxes and styling) on many videos without opening each one in Edits. | krusemediallc/video-editor-agent |
| [`general-video`](#general-video) | Author or edit a custom HyperFrames composition when no specialized workflow fits, or when BRIEF.md sets flow: companion. | earlier install |
| [`hook-splitter`](#hook-splitter) | - Split ONE long recording that contains many separate hooks/takes into a set of standalone videos — one per hook — and tighten each so there is no dead air, no stumble,… | krusemediallc/video-editor-agent |
| [`hook-variations`](#hook-variations) | - Combine ONE finished body cut with MANY hook clips to produce one standalone video per hook — the hook A/B batch you upload as separate ad creatives. | krusemediallc/video-editor-agent |
| [`makemyclip-editor`](#makemyclip-editor) | AI-native video editor for any agent. | MakeMyClip/editor |
| [`media-use`](#media-use) | Agent Media OS, the single skill for every media need in a HyperFrames project. | earlier install |
| [`reel-editor`](#reel-editor) | Edit talking-head / selfie videos into finished Instagram Reels, TikToks and YouTube Shorts with code-rendered motion graphics - face layouts that morph (split screen, p… | sunithvs/video-agent-skill |
| [`reel-from-donor`](#reel-from-donor) | - Превращает полезный разговорный Reels, Short или TikTok в авторский Reels с живыми, конкретными карточками: сначала разбирает донорский материал и проверяет факты, сна… | mcdenil-skills/AutoMontage-Agent |
| [`reel-recut`](#reel-recut) | - Recut a raw vertical talking-head reel into a finished short-form edit: a persistent title banner, word-synced karaoke captions, callout boxes for asides and comment-k… | krusemediallc/video-editor-agent |
| [`reel-style-clone`](#reel-style-clone) | - Reverse-engineer a reference reel's editing style frame-by-frame into a replicable STYLE GUIDE plus per-line BUILD DIRECTIVES, then apply that style to the user's own … | krusemediallc/video-editor-agent |
| [`reel-turnkey`](#reel-turnkey) | - Собирает ролик под ключ в AutoMontage-Agent: проверяет исходник, транскрибирует речь, показывает автору черновую нарезку своей съёмки без графики, готовит один полный … | mcdenil-skills/AutoMontage-Agent |
| [`short-form-video`](#short-form-video) | This skill should be used when the user asks to "make a Reels/TikTok/YouTube Shorts video", "build a short-form video template", "write a hook for a short", "edit for re… | iart-ai/tiktok-video-skills |
| [`talking-head`](#talking-head) | Create an AI talking head from the user's own photos plus a voice sample, or from a self-recorded video by extracting face frames and speech. | iart-ai/talking-head-skills |
| [`talking-head-b-roll`](#talking-head-b-roll) | Add b-roll motion graphics to a talking-head video. | iart-ai/b-roll-skills |
| [`talking-head-image-overlays`](#talking-head-image-overlays) | - Edit a talking-head video in the "uncut take + stacked image overlays" style: ONE continuous take that is never cut, with the entire sense of pace carried by hard-cut … | krusemediallc/video-editor-agent |
| [`talking-head-recut`](#talking-head-recut) | Package an existing talking-head / interview / podcast video with timed, designed GRAPHIC OVERLAY cards — kinetic titles, lower-thirds, data callouts, quotes, side panel… | earlier install |
| [`tenfold-video-edit`](#tenfold-video-edit) | Turns raw 9:16 talking-head clips into a finished, premium Instagram reel end to end: picks the cleanest take of every line across your clips, cuts dead air, punches in … | tenfoldmarc/video-edit-skill |
| [`video-edit-pipeline`](#video-edit-pipeline) | MASTER orchestration skill for producing a finished short-form video from raw talking-head footage. | krusemediallc/video-editor-agent |
| [`video_toolkit`](#video_toolkit) | Make short explainer videos from a brief with claude-code-video-toolkit — submit a scene spec, poll a job, get a QC-checked MP4. | digitalsamba/claude-code-video-toolkit |
| [`youtube-editor`](#youtube-editor) | Edit full-length horizontal YouTube videos (5-60 min talking heads, explainers, tutorials, screen recordings) into finished 1920x1080 uploads - automatic jump cuts that … | sunithvs/video-agent-skill |

### Captions, kinetic type and titles (13)

| Skill | What it does | Source |
|---|---|---|
| [`article-highlights`](#article-highlights) | Editorial Remotion article inserts with mandatory format/background intake, layered highlights, zero neon/glow, and mobile QA. | Liamrjohnston/remotion-motion-graphics-skill |
| [`canopy-part-title`](#canopy-part-title) | Leaves sweep through the frame and part to reveal the headline. | earlier install |
| [`caption-animation`](#caption-animation) | This skill should be used when the user asks to "add animated captions", "make TikTok captions", "karaoke captions", "word-by-word subtitles", "auto subtitles", "highlig… | iart-ai/tiktok-video-skills |
| [`captions-overlay`](#captions-overlay) | Overlay doctrine for captions in HyperFrames videos — the caption MODEL (drop / rail / embed) and the rule that captions are an OVERLAY composited on top of the film, ne… | heygen-com/hyperframes |
| [`embedded-captions`](#embedded-captions) | Add captions or subtitles to an existing single-subject talking-head video without editing the footage. | earlier install |
| [`glass-shard-title`](#glass-shard-title) | Glass shards fly in through fog and tile themselves into the headline. | earlier install |
| [`kinetic-typography`](#kinetic-typography) | This skill should be used when the user asks to "animate a headline", "make a kinetic typography video", "do a split-text reveal", "stagger text by character/word/line",… | iart-ai/kinetic-typography-skills |
| [`lt-lower-thirds`](#lt-lower-thirds) | Make animated lower thirds and other broadcast overlays (name straps, corner bugs, subscribe reminders, scripture or song titles) as transparent video files, drawn frame… | iart-ai/lower-thirds-skills |
| [`terminal-inserts`](#terminal-inserts) | Authentic, restrained Remotion terminal inserts with mandatory format/background intake and zero neon or glow. | Liamrjohnston/remotion-motion-graphics-skill |
| [`text-message-animation`](#text-message-animation) | This skill should be used when the user asks to "make a fake text message video", "animate an iMessage conversation", "create a text story video", "do a chat reply anima… | iart-ai/text-message-video-skills |
| [`tiktok-lower-thirds`](#tiktok-lower-thirds) | This skill should be used when the user asks to "make an animated lower third", "add lower thirds", "create a name tag/name lower third", "build broadcast titles", "anim… | iart-ai/tiktok-video-skills |
| [`title-sequence-3d`](#title-sequence-3d) | Make a cinematic 3D title sequence (8-15 seconds) in code with Claude Code and Three.js. | charlie947/motion-graphics-skills |
| [`wireframe-portal-title`](#wireframe-portal-title) | A wireframe portal bursts open, the title comes through, then its letters swap into a second phrase. | earlier install |

### Launch, product, ad and promo films (25)

| Skill | What it does | Source |
|---|---|---|
| [`ad-creative-video`](#ad-creative-video) | This skill should be used when the user asks to "make a video ad", "create an animated ad", "build a performance/UGC-style ad", "batch-produce ad creative variations", "… | iart-ai/ad-video-skills |
| [`ad-launch-video`](#ad-launch-video) | This skill should be used when the user asks to "make a launch video", "create a product hype/sizzle film", "build a teaser/trailer for a drop", "do a reveal montage wit… | iart-ai/ad-video-skills |
| [`ai-promo`](#ai-promo) | - Собирает безголосый промо-ролик, рекламу или трейлер на 20–30 секунд из AI-кинокадров (сейчас Higgsfield через OAuth MCP) и project-local Remotion-VFX под музыку в Aut… | mcdenil-skills/AutoMontage-Agent |
| [`apple-launch-film`](#apple-launch-film) | Rebuild an Apple-style Mac launch film entirely in code with Claude Code. | charlie947/motion-graphics-skills |
| [`cg-launch-video`](#cg-launch-video) | Make a 30-45 second product launch video in code with Claude Code, the kind SaaS companies post on launch day. | charlie947/motion-graphics-skills |
| [`cinetic`](#cinetic) | Direct, build and render premium cinematic motion design from code — launch films, product and feature videos, looping feature animations for landing pages and social, l… | earlier install |
| [`countdown-video`](#countdown-video) | This skill should be used when the user asks to "make a countdown timer video", "create a countdown animation", "build a stream starting soon countdown", "do an event/la… | iart-ai/tiktok-video-skills |
| [`huashu-motion`](#huashu-motion) | Motion graphics, launch videos and explainers as editable code. | alchaincyf/huashu-motion |
| [`lemo-opuscar`](#lemo-opuscar) | Direct and produce a short film made entirely in code, in one of the styles of the Lemo-Opuscar library (e.g. | earlier install |
| [`milestone-reveal`](#milestone-reveal) | Make a 12-second looping milestone clip in code with Claude Code. | charlie947/motion-graphics-skills |
| [`model-showdown`](#model-showdown) | Give the same motion brief to three AI models, keep each first try, render all three the same way and stack them into one comparison video with model names and logos. | charlie947/motion-graphics-skills |
| [`newsletter-promo`](#newsletter-promo) | Turn a newsletter edition into a 12-20 second promo clip for LinkedIn, Instagram or X that drives people to read and subscribe. | charlie947/motion-graphics-skills |
| [`photo-slideshow`](#photo-slideshow) | This skill should be used when the user asks to "make a photo slideshow", "turn photos into a video", "create a photo montage video", "make a picture slideshow with musi… | iart-ai/ecommerce-video-skills |
| [`pr-to-video`](#pr-to-video) | Turn a GitHub pull request (a PR URL, owner/repo#N, or 'this PR' in a checked-out repo) into a code-change explainer video — changelog, feature reveal, fix, or refactor … | earlier install |
| [`presentation-video`](#presentation-video) | This skill should be used when the user asks to "make an animated presentation", "turn a pitch deck into a video", "convert slides/a deck to video", "make a presentation… | iart-ai/data-animation-skills |
| [`product-demo-video`](#product-demo-video) | This skill should be used when the user asks to "make a product demo video", "create an app demo video", "build a feature announcement video", "do a SaaS demo", "make a … | iart-ai/ecommerce-video-skills |
| [`product-film`](#product-film) | Make a showreel-grade product film (landing-page loop, launch video, promo, demo reel, social cut) in code with Remotion, built on the product's own design system, compo… | earlier install |
| [`product-launch-video`](#product-launch-video) | Turn a product or marketing URL, pasted script, or brief into a product launch / promo video — SaaS promos, feature reveals, product demos, app and company launches. | earlier install |
| [`promo-video`](#promo-video) | This skill should be used when the user asks to "make a sale video", "create a promo video", "build a discount/percentage-off reveal", "animate a was→now price with a st… | iart-ai/ecommerce-video-skills |
| [`recap-video`](#recap-video) | - Edit an event, conference, summit, trip, or behind-the-scenes recap from spoken takes and supplied B-roll. | krusemediallc/video-editor-agent |
| [`slideshow`](#slideshow) | Author a HyperFrames slideshow — a presentation, pitch deck, or interactive deck with discrete slides, fragment reveals, branching, hotspot navigation, and built-in pres… | earlier install |
| [`take-one`](#take-one) | Turn a short request into a finished short film rendered from code, working like a studio team of twelve jobs (strategist, creative director, writer, voice director, art… | talsiach/take-one |
| [`testimonial-video`](#testimonial-video) | This skill should be used when the user asks to "make an animated testimonial", "create a quote video", "build a review video", "turn a customer testimonial into a graph… | iart-ai/ad-video-skills |
| [`wrapped-video`](#wrapped-video) | This skill should be used when the user asks to "make a Spotify Wrapped style video", "build a year in review / year-in-review video", "create a personalized data video"… | iart-ai/explainer-video-skills |
| [`youtube-intro-outro`](#youtube-intro-outro) | This skill should be used when the user asks to "make a YouTube intro", "create a channel intro", "build a logo sting/bumper", "design an outro / end screen / end card",… | iart-ai/youtube-video-skills |

### Explainers, data, charts and maps (13)

| Skill | What it does | Source |
|---|---|---|
| [`animated-chart`](#animated-chart) | Make a looping animated chart for LinkedIn or a newsletter in code with Claude Code. | charlie947/motion-graphics-skills |
| [`animated-infographic`](#animated-infographic) | This skill should be used when the user asks to "make an animated infographic", "create an infographic video", "build an infographic animation", "animate an explainer in… | iart-ai/data-animation-skills |
| [`arthur-explainer-video`](#arthur-explainer-video) | Make a 30-60s motion-graphics explainer or product demo video entirely in code (Remotion + React for picture, numpy synth for music and sound design), rendered to mp4 on… | arthurkatcher/explainer-video |
| [`chart-animation`](#chart-animation) | This skill should be used when the user asks to "make a bar chart race", "turn a CSV into a video", "build an animated data visualization", "create an animated statistic… | iart-ai/data-animation-skills |
| [`diagram-animation`](#diagram-animation) | This skill should be used when the user asks to "animate this diagram", "build a flowchart that reveals step by step", "animate an architecture/sequence diagram", "make … | iart-ai/explainer-video-skills |
| [`explainer-video`](#explainer-video) | This skill should be used when the user asks to "make an explainer video", "turn this into a short explainer", "write a script and storyboard for a product video", "prod… | iart-ai/explainer-video-skills |
| [`explainroo`](#explainroo) | Make an explainer video (MP4) with a voice-over using explainroo. | vincentsch/explainroo |
| [`faceless-explainer`](#faceless-explainer) | Turn arbitrary text — an article, notes, a topic, a brief — into a faceless explainer video: there is no site or footage to capture, so the visuals are invented per scen… | earlier install |
| [`isometric-animation`](#isometric-animation) | This skill should be used when the user asks to "make an isometric animation", "build a 2.5D isometric scene", "create an isometric infographic", "animate an exploded di… | iart-ai/explainer-video-skills |
| [`manim`](#manim) | This skill should be used when the user asks to "make a math animation", "animate an equation", "use Manim", "make a 3Blue1Brown-style video", "plot or animate a graph/f… | iart-ai/manim-skills |
| [`map-animation`](#map-animation) | This skill should be used when the user asks to "make a Vox-style map animation", "animate a map zoom", "draw a route on a map", "highlight a country/region", "use Googl… | iart-ai/map-animation-skills |
| [`vox-explainer`](#vox-explainer) | Make a short Vox-style documentary explainer (30-60 seconds) entirely in code with Claude Code. | charlie947/motion-graphics-skills |
| [`whiteboard-animation`](#whiteboard-animation) | This skill should be used when the user asks to "make a whiteboard animation", "draw-on explainer", "VideoScribe style", "hand-drawn explainer video", "animate a sketch … | iart-ai/explainer-video-skills |

### App demos, UI and screen capture (5)

| Skill | What it does | Source |
|---|---|---|
| [`argo-guide`](#argo-guide) | Guide for using Argo to create polished product demo videos from Playwright scripts with AI voiceover and animated overlays. | shreyaskarnik/argo |
| [`broll-capture`](#broll-capture) | Capture website B-roll and screenshots for a video edit: full-page screenshots of real pages (for shot-cards and "proof" beats), smooth scripted-scroll screen recordings… | krusemediallc/video-editor-agent |
| [`micro-interaction`](#micro-interaction) | This skill should be used when the user asks to "add a hover/press effect", "animate a toggle or switch", "build an animated like button", "make a toast/snackbar slide i… | iart-ai/web-animation-skills |
| [`playwright-recording`](#playwright-recording) | Record browser interactions as video using Playwright. | digitalsamba/claude-code-video-toolkit |
| [`synthetic-ui-demo`](#synthetic-ui-demo) | Product demo and release-notes videos with no screen recording. | digitalsamba/claude-code-video-toolkit |

### Copy and clone a reference (4)

| Skill | What it does | Source |
|---|---|---|
| [`pixel2motion`](#pixel2motion) | Turn a raster logo (PNG/JPG/WebP/screenshot) into a clean minimal SVG with edge smoothness as the primary hard gate and IoU optimized as high as reasonably possible with… | nolangz/pixel2motion |
| [`qwen-edit`](#qwen-edit) | AI image editing prompting patterns for Qwen-Image (Qwen-Image-Edit-2511 by default, Qwen-Image-2.1 as a non-commercial Modal opt-in). | digitalsamba/claude-code-video-toolkit |
| [`reanimate`](#reanimate) | Clone a section, widget, page or animation from any reference (a live website URL, a screen recording, an mp4/mov/webm, a gif, a Lottie file, a prototype export) frame b… | NiazMorshed2007/reanimate |
| [`reference-to-motion`](#reference-to-motion) | Turn references you admire into a scene-by-scene Claude Motion prompt for your own topic and brand. | charlie947/motion-graphics-skills |

### Web, SVG, Lottie and code animation (19)

| Skill | What it does | Source |
|---|---|---|
| [`60fps-animation`](#60fps-animation) | This skill should be used when the user asks to "fix janky CSS animation", "make animation 60fps", "stop layout thrashing", "animate width/height/top/left smoothly", "co… | iart-ai/web-animation-skills |
| [`accessible-animation`](#accessible-animation) | This skill should be used when the user asks to "respect prefers-reduced-motion", "honor reduced motion", "make my animations accessible", "fix vestibular / motion-sickn… | iart-ai/web-animation-skills |
| [`ascii-animation`](#ascii-animation) | This skill should be used when the user asks to "make an ASCII animation", "build a terminal/CLI intro or loader", "convert an image or video to ASCII art", "add an ASCI… | iart-ai/web-animation-skills |
| [`code-slice-hero`](#code-slice-hero) | A tiled headline surface flips cell by cell under a sweeping depth field to reveal the rear headline. | earlier install |
| [`cuboid-carousel`](#cuboid-carousel) | A chain of bevelled cuboids rides a travelling wave as a content carousel. | earlier install |
| [`frost-sequence-camera-orbit`](#frost-sequence-camera-orbit) | An orbiting camera follows an ice logo as it breaks apart, reforms into two text moments, and fades. | earlier install |
| [`glassmorphism`](#glassmorphism) | This skill should be used when the user asks to "add a glassmorphism effect", "frosted glass UI", "Apple liquid glass style", "frosted blur card", "translucent glass pan… | iart-ai/web-animation-skills |
| [`gsap-web`](#gsap-web) | This skill should be used when the user asks to "build a scroll animation", "add ScrollTrigger", "pin a section while scrolling", "scrub an animation to scroll", "create… | iart-ai/web-animation-skills |
| [`javascript-animation`](#javascript-animation) | This skill should be used when the user asks to "draw every frame in JavaScript", "make an animation with no image assets", "animate this in code / on a canvas", "make a… | iart-ai/javascript-animation-skills |
| [`logo-animation`](#logo-animation) | This skill should be used when the user asks to "animate our logo", "make a logo intro/stinger", "build a brand reveal", "create an app splash animation", "loop a loader… | iart-ai/motion-design-skills |
| [`loop-cover`](#loop-cover) | Turn a newsletter or blog cover into a seamless looping GIF at 896 x 640, 180 frames at 20fps. | charlie947/motion-graphics-skills |
| [`lottie-animation`](#lottie-animation) | This skill should be used when the user asks to "add a Lottie animation", "play a .lottie or .json animation", "integrate a Bodymovin/After Effects animation on web or m… | iart-ai/web-animation-skills |
| [`motion-background`](#motion-background) | This skill should be used when the user asks to "add an animated background", "build a mesh/gradient background", "make an aurora/shader background", "add constellation/… | iart-ai/motion-design-skills |
| [`orbit-card`](#orbit-card) | A single feature card orbits a dot sphere on approved Blender camera motion. | earlier install |
| [`page-transition-animation`](#page-transition-animation) | This skill should be used when the user asks to "animate page or route transitions", "add a page transition or crossfade between views", "animate route changes in Next.j… | iart-ai/web-animation-skills |
| [`particle-system`](#particle-system) | This skill should be used when the user asks to "build a particle system", "make confetti/snow/smoke/sparks", "create a connected-dot/constellation network background", … | iart-ai/webgl-animation-skills |
| [`rossark-motion-skill`](#rossark-motion-skill) | Bring anything drawn to life with calm, believable motion. | rossark0/rossark-motion-skill |
| [`svg-animation`](#svg-animation) | This skill should be used when the user asks to "animate an SVG", "make a line draw itself on", "do a stroke draw-on / signature animation", "morph one shape into anothe… | iart-ai/web-animation-skills |
| [`text-to-lottie`](#text-to-lottie) | Create, edit, or fix Lottie/Bodymovin JSON animations for the local Skia Skottie player. | diffusionstudio/lottie |

### 3D, WebGL and shaders (2)

| Skill | What it does | Source |
|---|---|---|
| [`shader-glsl`](#shader-glsl) | This skill should be used when the user asks to "write a fragment shader", "make a GLSL gradient/noise/plasma background", "create an image transition (dissolve, displac… | iart-ai/webgl-animation-skills |
| [`threejs-animation`](#threejs-animation) | This skill should be used when the user asks to "build a 3D hero section or WebGL background", "animate a Three.js scene", "play or crossfade GLTF animation clips", "mov… | iart-ai/webgl-animation-skills |

### Frameworks: HyperFrames and Remotion (13)

| Skill | What it does | Source |
|---|---|---|
| [`dsk-remotion`](#dsk-remotion) | Toolkit-specific Remotion patterns — custom transitions, shared components, and project conventions. | digitalsamba/claude-code-video-toolkit |
| [`hyperframes`](#hyperframes) | Mandatory entry point: read this first for any request to make, create, edit, animate, or render a video, animation, or motion graphic, including a promo, explainer, cap… | earlier install |
| [`hyperframes-animation`](#hyperframes-animation) | All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the seven runtime a… | earlier install |
| [`hyperframes-cli`](#hyperframes-cli) | Use the HyperFrames CLI development loop: init, add, catalog, capture, lint, check, snapshot, compare, grade-compare, preview, play, present, beats, keyframes, single or… | earlier install |
| [`hyperframes-core`](#hyperframes-core) | The HyperFrames composition contract — build one renderable project. | earlier install |
| [`hyperframes-creative`](#hyperframes-creative) | Non-animation creative direction for HyperFrames videos. | earlier install |
| [`hyperframes-keyframes`](#hyperframes-keyframes) | Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe, Ken Burns treatment, camera move, visual match/whip handoff, or other seek-safe 2D/3D keyf… | earlier install |
| [`hyperframes-registry`](#hyperframes-registry) | Search, install, and wire registry blocks and components into HyperFrames compositions. | earlier install |
| [`hyperframes-studio`](#hyperframes-studio) | Use when building or editing a HyperFrames project that people open in Studio: how the timeline should be laid out so it reads well (one caption track, one element kind … | earlier install |
| [`moviepy`](#moviepy) | Python video composition with moviepy 2.x — overlaying deterministic text on AI-generated video (LTX-2, SadTalker), compositing clips, single-file build.py video project… | digitalsamba/claude-code-video-toolkit |
| [`remotion-best-practices`](#remotion-best-practices) | Router for all Remotion skills | digitalsamba/claude-code-video-toolkit |
| [`remotion-bits`](#remotion-bits) | Animation components and utilities for Remotion video projects. | av/remotion-bits |
| [`remotion-to-hyperframes`](#remotion-to-hyperframes) | Port an existing Remotion (React) composition''s source to HyperFrames HTML. | earlier install |

### AI generation and B-roll (paid APIs: ask first) (6)

| Skill | What it does | Source |
|---|---|---|
| [`arcads-broll`](#arcads-broll) | GENERATE B-roll and motion-graphic elements for an edit with AI video/image models via the Arcads external API (Seedance, Sora 2, Veo 3.1, Kling, Grok Video, Nano Banana… | krusemediallc/video-editor-agent |
| [`generative-illustration`](#generative-illustration) | This skill should be used when the user asks to "make an animated illustration", "animate an illustration", "make a generative motion piece" / "动态平面", "turn AI-generated… | iart-ai/generative-illustration-skills |
| [`ideogram4`](#ideogram4) | Prompting patterns for Ideogram 4 text-to-image — best-in-class in-image text rendering and exact color/layout control via structured JSON captions. | digitalsamba/claude-code-video-toolkit |
| [`ltx2`](#ltx2) | AI video generation with LTX-2.3 22B — text-to-video, image-to-video clips for video production. | digitalsamba/claude-code-video-toolkit |
| [`openart-broll`](#openart-broll) | GENERATE B-roll, talking-head clips, and screen-blend motion-graphic overlays for an edit through the OpenArt MCP (Seedance, Kling, Wan, Gemini Omni, Grok Imagine, Nano … | krusemediallc/video-editor-agent |
| [`runpod`](#runpod) | Cloud GPU processing via RunPod serverless. | digitalsamba/claude-code-video-toolkit |

### Motion principles, art direction and critique (18)

| Skill | What it does | Source |
|---|---|---|
| [`animation-principles`](#animation-principles) | This skill should be used when the user asks to "make this animation feel natural", "fix motion that feels stiff/floaty/cheap", "my animation looks robotic", "choose an … | iart-ai/motion-design-skills |
| [`beat-sync-editing`](#beat-sync-editing) | This skill should be used when the user asks to "cut to the beat", "fix the pacing", "edit this sequence", "sync cuts to music/BPM", "add a match cut / J-cut / L-cut", "… | iart-ai/motion-design-skills |
| [`brand-intake`](#brand-intake) | The setup step every other skill in this pack reads. | charlie947/motion-graphics-skills |
| [`brand-motion-guidelines`](#brand-motion-guidelines) | This skill should be used when the user asks to "write motion guidelines", "create a brand motion system", "define easing and timing tokens", "document our animation pri… | iart-ai/freelance-motion-skills |
| [`cinematic-camera`](#cinematic-camera) | Continuous-scene Remotion camera system with mandatory intake, approved-reference review, anti-neon rules, and first-pass QA. | Liamrjohnston/remotion-motion-graphics-skill |
| [`color-motion`](#color-motion) | This skill should be used when the user asks to "build a color palette for a motion piece", "make a gradient background", "animate a color transition", "interpolate colo… | iart-ai/motion-design-skills |
| [`howseen-motion-design`](#howseen-motion-design) | Code-only motion design pipeline (no After Effects) for Raphaël / Howseen: launch films, showreels, product promos, LinkedIn/X videos, meme clips. | howseen-ai/claude-motion-design |
| [`liam-motion-graphics`](#liam-motion-graphics) | Add cached official-asset and product research preflight before reference selection and build authorization. | Liamrjohnston/remotion-motion-graphics-skill |
| [`lobzy-motion-design`](#lobzy-motion-design) | Use this skill whenever motion, animation, timing, easing, or composition over time is the subject. | LobzyJay/motion-design-with-claude |
| [`mort1d-motion-graphics`](#mort1d-motion-graphics) | Creates showreel-grade motion graphics videos entirely from code — HTML scenes rendered frame by frame in headless Chrome with real motion blur, plus an original score c… | Mort1d/motion-graphics-skills |
| [`motion-art-direction`](#motion-art-direction) | This skill should be used when the user asks to "direct a motion graphics video", "do creative/art direction for a video", "define a motion language", "set the tone and … | iart-ai/motion-design-skills |
| [`motion-design-critique`](#motion-design-critique) | Use this skill when something has gone wrong, looks wrong, or needs a second opinion. | LobzyJay/motion-design-with-claude |
| [`motion-effects`](#motion-effects) | Build any of 16 premium motion effects from scratch in your own brand, as one 8-second looping HTML file with window.seek(seconds) so it exports frame-exact to MP4 or GI… | charlie947/motion-graphics-skills |
| [`motion-graphics`](#motion-graphics) | A short, design-led motion graphic where motion is the message — kinetic typography, stat count-up, chart/data-viz hit, logo sting / brand lockup, lower-third / callout … | earlier install |
| [`naming-convention`](#naming-convention) | - Name a batch of video deliverables so each filename says what the file actually is — subject, variant axis, and treatment — instead of `render-final-v3.mp4`. | krusemediallc/video-editor-agent |
| [`shot-composition`](#shot-composition) | This skill should be used when the user asks to "compose a frame", "set up a grid", "plan shot composition", "place the focal point", "decide where elements enter and ex… | iart-ai/motion-design-skills |
| [`video-design`](#video-design) | Visual design for videos - colour by act, type scale, chart and layout rules for 16:9 and 9:16 scenes, a design.md handoff that any design skill can fill, and a contact-… | digitalsamba/claude-code-video-toolkit |
| [`video-director`](#video-director) | Direct, build and verify short videos that are written as code and rendered frame by frame (HTML/Canvas/SVG/Three.js, GSAP or Remotion → MP4 or a live page). | win4r/video-director |

### Briefs, pricing and client work (6)

| Skill | What it does | Source |
|---|---|---|
| [`client-revisions`](#client-revisions) | This skill should be used when the user asks to "stop scope creep", "limit revision rounds", "write SOW revision language", "the client keeps asking for changes", "how d… | iart-ai/freelance-motion-skills |
| [`creative-brief`](#creative-brief) | This skill should be used when the user asks to "write a creative brief", "build a motion brief", "the client doesn't know what they want", "turn this vague client reque… | iart-ai/freelance-motion-skills |
| [`lead-magnet`](#lead-magnet) | - Собирает лид-магнит к ролику в AutoMontage-Agent по запросу из «Пульта роликов»: дословное обещание, страница из заготовки бренд-пака, проверка фактов, PDF, тексты для… | mcdenil-skills/AutoMontage-Agent |
| [`motion-brief-writer`](#motion-brief-writer) | Turns a rough idea for an animated graphic into a precise build brief for Claude Code, in your own brand. | charlie947/motion-graphics-skills |
| [`motion-pricing`](#motion-pricing) | This skill should be used when the user asks to "quote a motion project", "estimate this animation job", "how much should I charge for this video", "what's my day rate",… | iart-ai/freelance-motion-skills |
| [`motion-prompt-writer`](#motion-prompt-writer) | Write a complete 8-part Claude Motion prompt (The bar, Format, The one rule, Look, Motion, Never, Before you finish, The scene) for one short looping motion graphic, in … | charlie947/motion-graphics-skills |

### Other (13)

| Skill | What it does | Source |
|---|---|---|
| [`animate`](#animate) | Make a short procedural animation in any style — an explainer, a history, a little story — as a single-file canvas video with a synthesized score, rendered to MP4. | cth9191/animate |
| [`changelog-video`](#changelog-video) | Turn a weekly changelog .md into a finished branded changelog video (square 1080, ~45-60s, Annie VO, animated brand background, mock-UI visualizations, lowkey captions). | heygen-com/hyperframes |
| [`chorono`](#chorono) | Create, edit and preview editable 2D animations in a connected Chorono editor through its MCP tools. | codie1982/chorono-editor |
| [`chorono-setup`](#chorono-setup) | Install, start and troubleshoot the local Chorono editor, MCP connection and agent skills for Claude Code, Claude Desktop and Codex. | codie1982/chorono-editor |
| [`cut-the-curve`](#cut-the-curve) | The technique catalog: five velocity-matched SEAMS (zoom-through, INVERSE zoom-through, cut-the-curve, waterfall cut, rack-focus blur-cut) plus the two in-scene techniqu… | heygen-com/hyperframes |
| [`directing-stickman-videos`](#directing-stickman-videos) | Turn topics, requirements, articles or scripts into stickman videos. | kaomei/stickman-video-director |
| [`free247editor`](#free247editor) | The user's personal video editor in this free247editor folder. | riecodes/free247editor |
| [`motion-doctrine`](#motion-doctrine) | GATEWAY — load FIRST before composing any HyperFrames animation or video. | heygen-com/hyperframes |
| [`oversized-cursor`](#oversized-cursor) | House-style oversized macOS cursor technique for HyperFrames launch videos. | heygen-com/hyperframes |
| [`reverse-any-video`](#reverse-any-video) | Rebuild any video file as an editable HyperFrames project - motion graphics, talking heads, live action or AI-generated footage - checked against the original frame by f… | heygen-com/hyperframes |
| [`seam-craft`](#seam-craft) | Render-correctness doctrine for scene-to-scene seams in HyperFrames launch videos — the prerequisites that make transitions composite correctly on the master timeline. | heygen-com/hyperframes |
| [`style-sampling`](#style-sampling) | Make a new episode in a proven video style - Collage Explainer, Finance Explainer, Animated Science Explainer, 3D Brand Explainer, 3D True Crime - on the person's topic. | heygen-com/hyperframes |
| [`ultimate-video-editor`](#ultimate-video-editor) | Transforms any AI code editor into a god-level video editor with 50+ years of craft. | Rajbharti06/Ultimate-Video-Editing-Skills |

## Full catalogue (A–Z)

Each entry gives the skill's own description (its trigger text), where it came from, its licence, and whether it ships scripts or tools.

### 60fps-animation
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/web-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/60fps-animation/` (3 files, SKILL.md 210 lines)

This skill should be used when the user asks to "fix janky CSS animation", "make animation 60fps", "stop layout thrashing", "animate width/height/top/left smoothly", "convert animation to transform", "animate box-shadow performantly", "animate height auto", "FLIP animation", or "why is my scroll/hover animation choppy".

### accessible-animation
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/web-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/accessible-animation/` (3 files, SKILL.md 231 lines)

This skill should be used when the user asks to "respect prefers-reduced-motion", "honor reduced motion", "make my animations accessible", "fix vestibular / motion-sickness issues", "add a useReducedMotion hook", "gate GSAP / Framer Motion / Lenis for reduced motion", or "meet WCAG 2.3.3 / C39". Provides tiered (not all-or-nothing) reduced-motion patterns in CSS and JS.

### acestep
- **Job:** Sound, music and audio QA
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/acestep/` (1 files, SKILL.md 351 lines)

AI music generation with ACE-Step 1.5 — background music, vocal tracks, covers, stem extraction, audio repainting, and continuation for video production. Use when generating music, soundtracks, jingles, or working with audio stems. Triggers include background music, soundtrack, jingle, music generation, stem extraction, cover, style transfer, repaint, continuation, or musical composition tasks.

### ad-creative-video
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/ad-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/ad-creative-video/` (4 files, SKILL.md 163 lines)

This skill should be used when the user asks to "make a video ad", "create an animated ad", "build a performance/UGC-style ad", "batch-produce ad creative variations", "generate ad variants for A/B testing", "swap headline/offer/CTA across many ad versions", or "export one ad in multiple aspect ratios for Meta/TikTok/Reels". Covers ad hook structures, hook→CTA message-match, data-driven variant generation (1 template × CSV = N ads), multi-aspect export, and platform specs.

### ad-launch-video
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/ad-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/ad-launch-video/` (3 files, SKILL.md 137 lines)

This skill should be used when the user asks to "make a launch video", "create a product hype/sizzle film", "build a teaser/trailer for a drop", "do a reveal montage with an end-card CTA", "cut a hero video to the beat", or "export a launch film in 16:9/9:16/1:1". Covers the hook→tease→reveal→feature-montage→end-card arc and multi-aspect export.

### adu-motion-video
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** adunext/adu-motion-video
- **Licence:** licensed
- **Folder:** `.claude/skills/adu-motion-video/` (1000 files, SKILL.md 96 lines, with scripts/tools)

使用完整动画工程包，把新口播、文案与自有素材制作成可编辑动效视频和 60fps MP4；也支持轻量 TPL、手绘续接、字幕与改旧片。支持 Windows、macOS、Linux，以及 Codex、Claude Code、豆包、DeepSeek、WorkBuddy 等可读写文件并运行命令的助手。

### after-effects
- **Job:** After Effects, Blender and desktop apps
- **Source:** iart-ai/motion-design-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/after-effects/` (10 files, SKILL.md 84 lines, with scripts/tools)

This skill should be used when the user asks anything about Adobe After Effects — to "write an After Effects expression", "make a wiggle / loopOut / inertial bounce", "rig a control with a slider / null", "build a MOGRT / Essential Graphics template", "export AE to Lottie or Media Encoder"; OR to "export from After Effects", "export with transparency / an alpha channel", "fix a black background on export", "choose ProRes vs H.264", "which codec / what bitrate for 1080p / 4K", "stop H.264 disappearing from the Render Queue"; OR when "After Effects is slow / laggy / crashing / froze", "RAM preview won't play in real time", "AE is using all my memory / render takes forever", "how do I speed up After Effects"; OR to "organize my After Effects project", "relink missing footage", "fix broken links after moving files", "set a folder structure / naming conventions", "batch rename layers", or "write an ExtendScript / .jsx script". Covers expressions & rigging, export recipes, performance triage, and project hygiene.

### aftereffects-motion
- **Job:** After Effects, Blender and desktop apps
- **Source:** LobzyJay/motion-design-with-claude
- **Licence:** licensed
- **Folder:** `.claude/skills/aftereffects-motion/` (11 files, SKILL.md 69 lines)

Use this skill whenever Adobe After Effects is the working tool. Triggers on "After Effects", "AE", ".aep", "ExtendScript", "JSX", "composition", "comp", "keyframe in AE", "AE expression", "render queue", "wiggle", "loopOut", "Trim Paths", or any AE-driven motion graphics task. Also triggers when the user is mid-session with the AE MCP bridge active (mcp-bridge-auto.jsx), or mentions "Higgsfield", "remove background", "reframe", "upscale", "Draw to Edit", or "generate footage" in an AE context. Pair with motion-design (foundation skill) for principles, timing, and taste. AE MCP server: TheLlamainator/after-effects-mcp. Optional Higgsfield Bridge MCP: bridge.higgsfield.ai/mcp.

### ai-audio-sound-design
- **Job:** Sound, music and audio QA
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/ai-audio-sound-design/` (3 files, SKILL.md 154 lines, with scripts/tools)

Rebuild the audio of an AI-generated video (Arcads / AI actors / UGC-gen / any clip whose voices sound like sterile studio AI) so every scene sounds like it was really filmed in the location shown — location-matched ambience beds, room-matched convolution reverb, outdoor distance treatment, censor bleeps over swears, removal of the AI high-frequency watermark whine, and a social loudness master, all with the video stream untouched. Use whenever someone says clips "sound AI / fake / sterile / like a voiceover", asks to "add ambient sounds / background noise", "make it sound like the location they're in", "add reverb to match the room", "bleep the swears / curse words", or hands over AI-actor footage for an audio pass — even if they never say "sound design". Also for revision rounds on an existing pass ("make the lawnmower louder", "add a car driving by", "make it sound like it's outside"). NOT for captions (embedded-captions), cutting footage (reel-recut), or full branded motion-graphic edits (branded-ad-edit).

### ai-promo
- **Job:** Launch, product, ad and promo films
- **Source:** mcdenil-skills/AutoMontage-Agent
- **Licence:** licensed
- **Folder:** `.claude/skills/ai-promo/` (19 files, SKILL.md 176 lines)

- Собирает безголосый промо-ролик, рекламу или трейлер на 20–30 секунд из AI-кинокадров (сейчас Higgsfield через OAuth MCP) и project-local Remotion-VFX под музыку в AutoMontage-Agent: согласованный текст, бюджет кредитов с явным согласием, ключевые кадры, оживление, VFX-пакет, саундтрек, `automontage motion --music-only`, настоящий preview, ручной QA, явное «утверждаю» и final. Используй для «промо-ролик», «рекламный ролик», «трейлер», «ролик из AI-кадров», «Higgsfield», «ролик под музыку без голоса», даже если навык не назван.

### am-motion-reel
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** mcdenil-skills/AutoMontage-Agent
- **Licence:** licensed
- **Folder:** `.claude/skills/am-motion-reel/` (2 files, SKILL.md 337 lines)

- Создаёт анимационный Reels/Shorts без камеры из темы, сценария или готовой озвучки в AutoMontage-Agent: script, выбор аудио, таймкоды, motion brief, настоящий preview, явное утверждение, MotionReel final и QA. Используй для «ролик без камеры», «анимационный рилс», «кинетический текст», «motion-reel» и «видео из озвучки»; в новом чате предлагает готовый стиль, уникальный Creative Motion или работу по референсу.

### animate
- **Job:** Other
- **Source:** cth9191/animate
- **Licence:** licensed
- **Folder:** `.claude/skills/animate/` (107 files, SKILL.md 134 lines, with scripts/tools)

Make a short procedural animation in any style — an explainer, a history, a little story — as a single-file canvas video with a synthesized score, rendered to MP4. Ships with styles (cut paper, crosshatch ink, riso print, sketchbook, manim-style math, pixel art, isometric line art) and makes new ones from the user's references. Walks the user through intake, then three check-ins (story, look, storyboard) before animating, and proves the result with measured review checks. Use when the user asks for an animated video, short, explainer or reel made in code, or wants a look matched from references.

### animated-chart
- **Job:** Explainers, data, charts and maps
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/animated-chart/` (1 files, SKILL.md 54 lines)

Make a looping animated chart for LinkedIn or a newsletter in code with Claude Code. Bars that become a line, a number that counts up, a before and after. Every value stays exactly as given. Use when someone says "animate my chart", "animated graph", "make my results move", "stat animation" or wants a data graphic that loops.

### animated-infographic
- **Job:** Explainers, data, charts and maps
- **Source:** iart-ai/data-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/animated-infographic/` (3 files, SKILL.md 170 lines)

This skill should be used when the user asks to "make an animated infographic", "create an infographic video", "build an infographic animation", "animate an explainer infographic", "do a sequenced reveal of icons and stats", "animate icons with key numbers and connectors", or "lay out a designed infographic that animates in sequence". Covers infographic layout & visual hierarchy, staggered element reveals, animating icons/pictograms, key-number counters, connectors/flow, and section pacing. For heavy charting (bar chart race, charts from a CSV) use the chart-animation skill instead.

### animation-principles
- **Job:** Motion principles, art direction and critique
- **Source:** iart-ai/motion-design-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/animation-principles/` (5 files, SKILL.md 114 lines)

This skill should be used when the user asks to "make this animation feel natural", "fix motion that feels stiff/floaty/cheap", "my animation looks robotic", "choose an easing curve", "how do I use the Graph Editor", "add overshoot or bounce", "Easy Ease isn't enough", "make snappy motion", "pick a duration for this transition", "stagger a list animation", "sync animation to a beat", or "review motion for good timing". It is the tech-agnostic foundation for deciding how something should move.

### apple-launch-film
- **Job:** Launch, product, ad and promo films
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/apple-launch-film/` (1 files, SKILL.md 59 lines)

Rebuild an Apple-style Mac launch film entirely in code with Claude Code. A thin menu bar, the black notch growing into widgets one scene at a time, full-screen gradient wallpapers and one short caption per scene. No screen recording, no After Effects. Use when someone says "Apple-style launch", "Mac launch video", "notch animation", "make it look like an Apple keynote", "macOS UI launch film" or wants a product launch that looks like native Mac interface.

### arcads-broll
- **Job:** AI generation and B-roll (paid APIs: ask first)
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/arcads-broll/` (1 files, SKILL.md 96 lines)

GENERATE B-roll and motion-graphic elements for an edit with AI video/image models via the Arcads external API (Seedance, Sora 2, Veo 3.1, Kling, Grok Video, Nano Banana) — product b-roll clips, scene beats, UGC-style inserts, shot-card stills, and screen-blend motion-graphic overlays. Use when an edit needs footage that cannot be captured: "generate b-roll of the product", "make an AI clip for this beat", "motion graphic overlay for this line", "AI insert shot". NOT for capturing real websites/screens (broll-capture) or authoring composition cards (branded-ad-edit).

### arcads-video-edit
- **Job:** Talking-head and short-form reel editing
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/arcads-video-edit/` (22 files, SKILL.md 166 lines, with scripts/tools)

Turn a creator's multi-take product-demo recordings (each take = screen recording + camera video + mic WAV, usually the creator walking through Arcads) into a finished 9:16 ad: an EDL-driven base cut rotating three layouts (the speaker full screen / split with the screen on top / full-screen product with the speaker in a circle), every pause cut so they talk over their own pauses, retakes dropped; then a HyperFrames motion-graphics pass with full-screen takeovers, the base video moving into splits and circles, real generated footage in cards and montages, word-synced captions, SFX and music, reviewed on a here.now canvas and gated by a copy review and the 4-layer video QA. Use whenever the user hands over a folder of takes and says "edit these together", "make the base edit", "cut this into an ad", "add motion graphics / takeovers / captions / music", or leaves timeline notes on an Arcads-style edit, even if they never say Arcads or multicam. Not for reel-recut, embedded-captions, or a talking head with no screen footage (branded-ad-edit).

### argo-guide
- **Job:** App demos, UI and screen capture
- **Source:** shreyaskarnik/argo
- **Licence:** licensed
- **Folder:** `.claude/skills/argo-guide/` (9 files, SKILL.md 596 lines)

Guide for using Argo to create polished product demo videos from Playwright scripts with AI voiceover and animated overlays. Use this skill whenever the user mentions Argo, demo videos, product demos, screen recordings with narration, Playwright video demos, voiceover generation, or wants to automate creating marketing/sales/onboarding videos from a web app. Also use when you see imports from '@argo-video/cli', files named '*.demo.ts' or '*.scenes.json', or an 'argo.config.js' in the project. Even if the user just says "record a demo" or "make a video of my app", this skill applies.

### arthur-explainer-video
- **Job:** Explainers, data, charts and maps
- **Source:** arthurkatcher/explainer-video
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/arthur-explainer-video/` (10 files, SKILL.md 29 lines, with scripts/tools)

Make a 30-60s motion-graphics explainer or product demo video entirely in code (Remotion + React for picture, numpy synth for music and sound design), rendered to mp4 on a laptop. Use when asked for an explainer, demo video, launch video, animated "how X works", or motion graphics.

### article-highlights
- **Job:** Captions, kinetic type and titles
- **Source:** Liamrjohnston/remotion-motion-graphics-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/article-highlights/` (2 files, SKILL.md 110 lines)

Editorial Remotion article inserts with mandatory format/background intake, layered highlights, zero neon/glow, and mobile QA.

### ascii-animation
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/web-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/ascii-animation/` (4 files, SKILL.md 179 lines, with scripts/tools)

This skill should be used when the user asks to "make an ASCII animation", "build a terminal/CLI intro or loader", "convert an image or video to ASCII art", "add an ASCII shader/post-effect to a canvas or Three.js scene", "create retro/hacker text-character motion", or "animate text characters with a brightness ramp". Covers generative ASCII fields, image/video/3D-to-ASCII, and animated character art for both web and terminal.

### audiogram
- **Job:** Sound, music and audio QA
- **Source:** iart-ai/youtube-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/audiogram/` (3 files, SKILL.md 145 lines)

This skill should be used when the user asks to "make an audiogram", "turn a podcast into a video", "create a waveform video", "make a podcast clip video", "convert audio to video", "animate a waveform/audio bars", "add a moving waveform to my voiceover", or "make a square/vertical clip for a podcast quote". Covers amplitude-driven waveforms, frequency bars, synced captions, cover-art layout, a progress bar, and 1:1 / 9:16 social framing.

### auto-editor
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** WyattBlue/auto-editor
- **Licence:** licensed
- **Folder:** `.claude/skills/auto-editor/` (1 files, SKILL.md 145 lines)

Record a microphone or edit video/audio with the auto-editor CLI — cut out dead space (silence, motionlessness, black frames), set the pace, make manual cuts, and render the result. Use when someone wants to capture and trim a microphone, remove silence, shorten a recording, speed through quiet parts, or otherwise edit media with auto-editor.

### auto-editor-effects
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** WyattBlue/auto-editor
- **Licence:** licensed
- **Folder:** `.claude/skills/auto-editor-effects/` (1 files, SKILL.md 144 lines)

Apply actions and animations to sections of a video/audio with auto-editor — change speed, duck or fade volume, de-ess, zoom/Ken Burns, rotate/spin, draw boxes, overlay logos or picture-in-picture, and animate any of these with ramps and easing. Use when someone wants creative effects or per-section behavior rather than plain silence-cutting.

### auto-editor-export
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** WyattBlue/auto-editor
- **Licence:** licensed
- **Folder:** `.claude/skills/auto-editor-export/` (1 files, SKILL.md 123 lines)

Export auto-editor's edit or microphone recording to a video editor (Premiere, DaVinci Resolve, Final Cut Pro, ShotCut, Kdenlive), to individual clips, or to auto-editor timeline files (.v1/.v2/.v3); and import timeline/XML files to render them. Use when someone wants an editor-ready project, a preserved microphone source, split clips, or timeline files instead of a finished video.

### auto-editor-transcribe
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** WyattBlue/auto-editor
- **Licence:** licensed
- **Folder:** `.claude/skills/auto-editor-transcribe/` (1 files, SKILL.md 120 lines)

Transcribe a media file or live microphone to text or subtitles with auto-editor's whisper subcommand, then edit by spoken content — cut to keep (or drop) sections whose subtitles match a word or regex. Use when someone wants a transcript, captions, live speech transcription, or to cut a video based on what is said rather than on loudness.

### auto-editor-transitions
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** WyattBlue/auto-editor
- **Licence:** licensed
- **Folder:** `.claude/skills/auto-editor-transitions/` (1 files, SKILL.md 123 lines)

Add transitions at auto-editor's cuts — cross-dissolves, Premiere Pro's transitions (push, clock-wipe, glitch, page-peel, iris-round, and the rest, including its Legacy folder), and audio crossfades — and carry them into Premiere, DaVinci Resolve, Final Cut Pro, Shotcut or Kdenlive. Use when someone wants smoother cuts, fades at the start and end, a particular transition, or transitions that survive an editor export or import.

### beat-sync-edit
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** ZiadAbdelkarim/beat-synced-edit
- **Licence:** licensed
- **Folder:** `.claude/skills/beat-sync-edit/` (10 files, SKILL.md 109 lines)

Turn a song + raw footage into a beat-synced edit. Runs the four-stage pipeline (beat analysis, scene tagging, EDL planning, render) and applies user-described ffmpeg effects — white flashes, stretch punches, hue shifts, speed ramps — at beat-accurate timestamps.

### beat-sync-editing
- **Job:** Motion principles, art direction and critique
- **Source:** iart-ai/motion-design-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/beat-sync-editing/` (3 files, SKILL.md 229 lines)

This skill should be used when the user asks to "cut to the beat", "fix the pacing", "edit this sequence", "sync cuts to music/BPM", "add a match cut / J-cut / L-cut", "build a speed ramp", or "plan a shot sequence / edit timeline". Covers editing rhythm, transitions, retiming, and translating an edit plan to an NLE or a code timeline (Remotion/AE frames).

### blender
- **Job:** After Effects, Blender and desktop apps
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/blender/` (1 files, SKILL.md 578 lines)

3D scenes, character acting and product shots from a shot spec, rendered in Blender, as a finished film, as clips for any other build (moviepy, a video job, an editor), or as elements of a Remotion video (transparent characters over a scene, a Remotion render on a 3D laptop, phone or floating card that the camera pulls back from, an imported 3D model on a studio stage). A rigged cartoon cast described in JSON (build, face, hair, clothes, a seed), sets, shots by type, acting beats in seconds or on narration words, every camera checked by geometry, sound placed on the motion. Use when a video needs a consistent directable character (parody, explainer gag, reaction shot), a 3D reveal or element in a Remotion video, a device or product shot of an app or a model, or exact acting timing that AI video clips can't hold. Triggers include Blender, 3D, character animation, rigged character, cast, shot spec, acting, camera angles, transparent clip, alpha, pull out from the screen, phone mockup, device mockup, product shot, turntable, orbit, glTF, GLB, BlenderClip.

### blender-motion
- **Job:** After Effects, Blender and desktop apps
- **Source:** LobzyJay/motion-design-with-claude
- **Licence:** licensed
- **Folder:** `.claude/skills/blender-motion/` (12 files, SKILL.md 76 lines)

Use this skill whenever Blender is the working tool. Triggers on "Blender", "bpy", "geometry nodes", "Cycles", "EEVEE", "Principled BSDF", "F-curve", "NLA", "keyframe in Blender", "3D motion graphics", "Blender render", "shape keys", "drivers", or any Blender-driven motion or rendering task. Also triggers on "Higgsfield", "Scene Builder", "blockout", "generate a mesh", "rigged character", "Seedance" in a Blender context. Pair with motion-design (foundation skill) for principles, timing, and taste. Blender MCP server: official Blender Lab MCP at projects.blender.org/lab/blender_mcp. Optional Higgsfield Bridge MCP: bridge.higgsfield.ai/mcp.

### boring-tools
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** brookejlacey/boring-tools
- **Licence:** licensed
- **Folder:** `.claude/skills/boring-tools/` (35 files, SKILL.md 101 lines, with scripts/tools)

Edit video as text. Cut a long take into finished social or ad renders using ffmpeg, whisper, and python, where every cut, caption, and graphic placement is a number in a file you can read and re-render. Use when the user hands you raw footage, says "cut this", "make the cards bigger", "put the screen beside my head", "remove that thing on the wall", "give me a 15 and a 30", or asks for captions, vertical and landscape versions, or a rebuild after a note.

### brand-intake
- **Job:** Motion principles, art direction and critique
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/brand-intake/` (1 files, SKILL.md 94 lines)

The setup step every other skill in this pack reads. A short interview plus 3 to 5 reference frames becomes two files in your project, brand.md (who you are, what you sell, your assets) and MOTION.md (your colours, type, timing and motion rules), plus a rule in CLAUDE.md so Claude reads them before it animates anything. Use at the start of any motion project, or when someone says "set up my brand", "brand intake", "build my motion design system", "make it look like my brand", "onboard me", "write my MOTION.md" or drops a batch of brand frames into chat.

### brand-motion-guidelines
- **Job:** Motion principles, art direction and critique
- **Source:** iart-ai/freelance-motion-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/brand-motion-guidelines/` (5 files, SKILL.md 220 lines)

This skill should be used when the user asks to "write motion guidelines", "create a brand motion system", "define easing and timing tokens", "document our animation principles", "build a motion language like Slack/IBM/Klarna", "set up entrance/exit/transition rules", or "add a reduced-motion / accessibility section". It outputs a fill-in-ready brand motion guidelines document.

### branded-ad-edit
- **Job:** Talking-head and short-form reel editing
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/branded-ad-edit/` (10 files, SKILL.md 216 lines, with scripts/tools)

Turn a RAW talking-head video into a FINISHED, branded, motion-graphics ad for any brand or industry — a designed motion graphic on every spoken line, the brand's real colors/logo/screenshots, word-synced karaoke captions, ElevenLabs SFX + a low music bed, website B-roll in browser frames, dramatic full-bleed cuts, and optional hook A/B variants. Renders 9:16 MP4s via HyperFrames. Use this whenever someone hands over raw talking-head footage plus a brand and wants "the full edit", "motion graphics on every line", "make it look like their winning ads", "the brand-deal edit", "edit this like that winning ad", or an ad-ready version of a talking video — even if they never say "motion graphics". NOT for plain subtitles (embedded-captions), a personal signature reel style (reel-recut), or unbranded overlay cards (talking-head-recut) — this skill owns the brand-research → design → sound-design → A/B pipeline end to end.

### broll-capture
- **Job:** App demos, UI and screen capture
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/broll-capture/` (2 files, SKILL.md 136 lines, with scripts/tools)

Capture website B-roll and screenshots for a video edit: full-page screenshots of real pages (for shot-cards and "proof" beats), smooth scripted-scroll screen recordings, and high-fidelity Screen Studio recordings of the user's real browser for sites that block automation. Use whenever an edit needs real screenshots, a screen recording of a website/app, "capture the site", or B-roll of a product. NOT for generating graphics (branded-ad-edit cards) or editing footage.

### canopy-part-title
- **Job:** Captions, kinetic type and titles
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/canopy-part-title/` (5 files, SKILL.md 70 lines)

Leaves sweep through the frame and part to reveal the headline. HyperFrames block, 1920×1080, 12s, 11 variables.

### capcut-export
- **Job:** After Effects, Blender and desktop apps
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/capcut-export/` (2 files, SKILL.md 173 lines, with scripts/tools)

Export a finished layered edit (footage + graphic cards + alpha fx overlay + captions + SFX/music/VO) into a CapCut desktop draft where EVERY element stays editable — footage segments split at zoom boundaries, per-card graphic clips, a true-alpha fx overlay, native text captions, per-hit SFX clips, and separate music/VO tracks. Use when someone says "export to CapCut", "make this editable in CapCut", "CapCut draft", "hand the edit off to a human editor", "open my render in CapCut with layers", or mentions pyJianYingDraft / JianYing drafts / draft_content.json / draft_info.json / root_meta_info.json. Builds the draft via pyJianYingDraft, then applies a work-in-progress schema patch for modern CapCut (~181.x) and registers the draft. NOT for rendering the video itself (that is the edit skill's job) — this consumes an already-finished layered edit and its render passes.

### caption-animation
- **Job:** Captions, kinetic type and titles
- **Source:** iart-ai/tiktok-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/caption-animation/` (3 files, SKILL.md 177 lines)

This skill should be used when the user asks to "add animated captions", "make TikTok captions", "karaoke captions", "word-by-word subtitles", "auto subtitles", "highlight the active word", "burn in captions to a video", "sync captions to a voiceover/narration", or "turn an SRT/transcript into animated text". Covers word-level timing from Whisper, per-word pop/scale-in, active-word highlight, 9:16 safe-area placement, readable type, and burn-in vs sidecar SRT/VTT.

### captions-overlay
- **Job:** Captions, kinetic type and titles
- **Source:** heygen-com/hyperframes
- **Licence:** licensed
- **Folder:** `.claude/skills/captions-overlay/` (1 files, SKILL.md 80 lines)

Overlay doctrine for captions in HyperFrames videos — the caption MODEL (drop / rail / embed) and the rule that captions are an OVERLAY composited on top of the film, never a reserved bottom band you shift content up to avoid. Load when adding captions/subtitles to a talking-head or launch video, when deciding whether a phrase should be dropped, ride the verbatim rail, or be promoted to a scarce embedded climax, when laying out a composition that will carry captions (do NOT reserve a keep-out band), or when centering a composition on the true frame center under captions. Applies ON TOP of the `/hyperframes` skill's references/captions.md.

### cg-launch-video
- **Job:** Launch, product, ad and promo films
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/cg-launch-video/` (1 files, SKILL.md 74 lines)

Make a 30-45 second product launch video in code with Claude Code, the kind SaaS companies post on launch day. One sentence split across scenes, real product screens with slow camera moves, a typed prompt, a proof beat and a clear call to action. Use when someone says "launch video", "promo video for my product", "announce my course/cohort/offer", "make a launch reel" or "trailer for my product".

### changelog-video
- **Job:** Other
- **Source:** heygen-com/hyperframes
- **Licence:** licensed
- **Folder:** `.claude/skills/changelog-video/` (15 files, SKILL.md 197 lines, with scripts/tools)

Turn a weekly changelog .md into a finished branded changelog video (square 1080, ~45-60s, Annie VO, animated brand background, mock-UI visualizations, lowkey captions). Use when the user provides a changelog/digest markdown and wants the weekly video, or says "changelog video". Self-contained — fonts, background, lexicon, and scripts ship in this skill.

### chart-animation
- **Job:** Explainers, data, charts and maps
- **Source:** iart-ai/data-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/chart-animation/` (4 files, SKILL.md 173 lines)

This skill should be used when the user asks to "make a bar chart race", "turn a CSV into a video", "build an animated data visualization", "create an animated statistics video", "animate a chart/graph", "make a number counter/ticker", "animate a ranking over time", or "batch-render one chart template across many datasets". Covers data-driven keyframing, value interpolation, rank transitions, counters, pacing, annotation, and template×data batch output.

### chorono
- **Job:** Other
- **Source:** codie1982/chorono-editor
- **Licence:** licensed
- **Folder:** `.claude/skills/chorono/` (9 files, SKILL.md 45 lines)

Create, edit and preview editable 2D animations in a connected Chorono editor through its MCP tools. Use for Chorono scenes, objects, timelines, particles and interactive animations.

### chorono-setup
- **Job:** Other
- **Source:** codie1982/chorono-editor
- **Licence:** licensed
- **Folder:** `.claude/skills/chorono-setup/` (2 files, SKILL.md 38 lines)

Install, start and troubleshoot the local Chorono editor, MCP connection and agent skills for Claude Code, Claude Desktop and Codex.

### cinematic-camera
- **Job:** Motion principles, art direction and critique
- **Source:** Liamrjohnston/remotion-motion-graphics-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/cinematic-camera/` (1 files, SKILL.md 143 lines)

Continuous-scene Remotion camera system with mandatory intake, approved-reference review, anti-neon rules, and first-pass QA.

### cinetic
- **Job:** Launch, product, ad and promo films
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/cinetic/` (146 files, SKILL.md 532 lines, with scripts/tools)

Direct, build and render premium cinematic motion design from code — launch films, product and feature videos, looping feature animations for landing pages and social, logo stings and reveals, UI walkthroughs, app demos, kinetic type, teasers, trailers, intros and promo clips. Use this whenever the user wants any video, animation, motion graphic or animated demo made with Remotion, HyperFrames, HTML/GSAP or React, or asks to storyboard, time, score, render, polish or critique one — even if they only say "make a video about X", "animate this feature" or "we need a launch clip". It supplies concept and copy discipline, type and colour taste that defers to a supplied brand, a beat-locked timeline that drives both picture and a code-made soundtrack, choreography and transition craft, real product UI in motion, film-grade finishing (true motion blur, no banding, BT.709, sync-checked mux) and a measured self-critique loop on contact sheets and renders.

### client-revisions
- **Job:** Briefs, pricing and client work
- **Source:** iart-ai/freelance-motion-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/client-revisions/` (5 files, SKILL.md 205 lines)

This skill should be used when the user asks to "stop scope creep", "limit revision rounds", "write SOW revision language", "the client keeps asking for changes", "how do I say this is out of scope", "translate vague feedback", "client said make it pop", or "write a change-order email". It provides revision-cap contract language, a consolidated-feedback request, a vague-feedback translator, and a polite out-of-scope email.

### code-slice-hero
- **Job:** Web, SVG, Lottie and code animation
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/code-slice-hero/` (9 files, SKILL.md 81 lines)

A tiled headline surface flips cell by cell under a sweeping depth field to reveal the rear headline. HyperFrames block, 1920×1080, 8s, 18 variables.

### color-motion
- **Job:** Motion principles, art direction and critique
- **Source:** iart-ai/motion-design-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/color-motion/` (4 files, SKILL.md 175 lines)

This skill should be used when the user asks to "build a color palette for a motion piece", "make a gradient background", "animate a color transition", "interpolate colors smoothly", "fix muddy/gray gradients", "convert colors to OKLCH", "color-grade a video for mood", "fix washed-out After Effects renders", "gamma shift", "Rec.709 vs sRGB", "colors shifted after rendering", or "match preview to final video". Covers palette construction, gradients, perceptual interpolation (OKLCH/Lab), grading order, and video/render color management.

### countdown-video
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/tiktok-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/countdown-video/` (4 files, SKILL.md 152 lines)

This skill should be used when the user asks to "make a countdown timer video", "create a countdown animation", "build a stream starting soon countdown", "do an event/launch/sale countdown", "animate a mm:ss or dd:hh:mm:ss timer", "add digit roll/flip transitions to a counter", or "loop a countdown background". Covers frame-accurate (drift-free) timers, digit flip/roll motion, time formatting, and a configurable duration prop.

### creative-brief
- **Job:** Briefs, pricing and client work
- **Source:** iart-ai/freelance-motion-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/creative-brief/` (5 files, SKILL.md 215 lines)

This skill should be used when the user asks to "write a creative brief", "build a motion brief", "the client doesn't know what they want", "turn this vague client request into a brief", "what questions should I ask the client", or "make a brief I can get sign-off on". It turns a fuzzy client ask into a structured, sign-off-ready motion design brief and the exact clarifying questions to send back.

### cuboid-carousel
- **Job:** Web, SVG, Lottie and code animation
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/cuboid-carousel/` (11 files, SKILL.md 105 lines)

A chain of bevelled cuboids rides a travelling wave as a content carousel. HyperFrames block, 1920×1080, 6.666666666666667s, 40 variables.

### cut-the-curve
- **Job:** Other
- **Source:** heygen-com/hyperframes
- **Licence:** licensed
- **Folder:** `.claude/skills/cut-the-curve/` (2 files, SKILL.md 260 lines)

The technique catalog: five velocity-matched SEAMS (zoom-through, INVERSE zoom-through, cut-the-curve, waterfall cut, rack-focus blur-cut) plus the two in-scene techniques — waterfall ENTRY (staggered arrival cascades for title cards / segment openers) and the nudge curve (slow-fast-slow three-phase group slides). Covers partial-travel (~12% of frame) velocity matching via mirrored power4 eases, the Z scale-sign rule, size-scaled blur (10px text / 18-20px full-frame), word-by-word staggered cuts, cascade pacing by element weight, and the 10/65/25 slide ratio. Read before authoring any transition, text-beat handoff, kinetic text entry, or group reposition. [depth, zoom, inverse-zoom, scale-sign, mirrored-zoom, rack-focus, pacing, velocity, cut-the-curve, waterfall, stagger, cascade, kinetic-text, title-card, segment-opener, nudge, slide, easing, group-motion, z-depth, motion-graphics, cinematic, transition, blur, directional-continuity]

### diagram-animation
- **Job:** Explainers, data, charts and maps
- **Source:** iart-ai/explainer-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/diagram-animation/` (3 files, SKILL.md 163 lines)

This skill should be used when the user asks to "animate this diagram", "build a flowchart that reveals step by step", "animate an architecture/sequence diagram", "make a chart animate in", "grow the bars / draw the line / count up the number", "show data flowing along a connector", or "turn a static diagram into a guided reveal". Covers SVG, Framer Motion, D3, and Remotion.

### directing-stickman-videos
- **Job:** Other
- **Source:** kaomei/stickman-video-director
- **Licence:** licensed
- **Folder:** `.claude/skills/directing-stickman-videos/` (98 files, SKILL.md 110 lines, with scripts/tools)

Turn topics, requirements, articles or scripts into stickman videos. Director mode creates approved storyboards and standalone video prompts; Autopilot mode produces narrated, captioned illustration-and-micro-animation videos through configured generation tools and a local renderer. Also guide installation handoff, first use and setup of this specific Skill.

### dsk-elevenlabs
- **Job:** Sound, music and audio QA
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/dsk-elevenlabs/` (2 files, SKILL.md 446 lines)

Generate AI voiceovers, sound effects, and music using ElevenLabs APIs. Use when creating audio content for videos, podcasts, or games. Triggers include generating voiceovers, narration, dialogue, sound effects from descriptions, background music, soundtrack generation, voice cloning, or any audio synthesis task.

### dsk-ffmpeg
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/dsk-ffmpeg/` (2 files, SKILL.md 432 lines)

Video and audio processing with FFmpeg. Use for format conversion, resizing, compression, audio extraction, and preparing assets for Remotion. Triggers include converting GIF to MP4, resizing video, extracting audio, compressing files, or any media transformation task.

### dsk-remotion
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/dsk-remotion/` (3 files, SKILL.md 164 lines)

Toolkit-specific Remotion patterns — custom transitions, shared components, and project conventions. For core Remotion framework knowledge (hooks, animations, rendering, etc.), see the `remotion-official` skill.

### earshot
- **Job:** Sound, music and audio QA
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/earshot/` (1 files, SKILL.md 237 lines)

Listen with earshot whenever you must judge, choose, trim, verify or compare sound you cannot hear - picking a sound effect, music or ambience from candidates, finding the cleanest moment in a recording, checking whether audio reads as a real recording or as code-synthesized, reviewing a soundtrack or a video's audio (what happens when, sync to picture, loudness, mix), A/B-ing a mix change, making a sound in code and improving it by listening (earshot forge), or giving a code-made film its sound effects from the shipped bank (earshot sfx / kit). Use it before telling anyone how audio sounds.

### ecc-video-editing
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** KirttiVushan/claude-code
- **Licence:** licensed
- **Folder:** `.claude/skills/ecc-video-editing/` (1 files, SKILL.md 310 lines)

AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pipeline from raw capture through FFmpeg, Remotion, ElevenLabs, fal.ai, and final polish in Descript or CapCut. Use when the user wants to edit video, cut footage, create vlogs, or build video content.

### editing-videos
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** kmilo93sd/agent-video-editor
- **Licence:** licensed
- **Folder:** `.claude/skills/editing-videos/` (204 files, SKILL.md 182 lines)

Gives an editor's judgment, with sourced numbers, for cutting and pacing, J and L cuts, jump cuts, b-roll, hooks and retention, captions, on-screen text and graphics, zoom and punch-in, audio levels in LUFS, music ducking, sound effects, basic color, thumbnails, titles, chapters and licensing. Use it when planning, scripting, editing, reviewing or publishing any video for YouTube, Shorts, Reels or TikTok: a talking head, a vlog, a podcast or interview, a screen tutorial, an explainer or a vertical clip from a long video, or when looking for royalty-free sound effects, music, animated graphics or a meme to recreate. Works with any tool (Premiere Pro, DaVinci Resolve, Final Cut Pro, CapCut, ffmpeg, Remotion, HyperFrames). Ships recipes per video type, a review checklist, a CC0 sound library, a CC0 graphics kit for HyperFrames, a meme reference with Content ID risk, and tested templates for narrated screen tutorials.

### edits-hook-overlay
- **Job:** Talking-head and short-form reel editing
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/edits-hook-overlay/` (6 files, SKILL.md 127 lines, with scripts/tools)

Put Instagram's NATIVE text hook (the Edits app's own font, boxes and styling) on many videos without opening each one in Edits. Type each hook once in Edits on a USB-connected iPhone over a black/white plate, export it, lift the text out as an exact transparent PNG (difference matte), and burn it onto any number of videos, keeping HDR (HLG) phone footage untouched. Use for "put my IG text hook on these videos", "native Instagram title on all of these", "same hook overlay on 100 clips", "make the Edits text once and reuse it", "hook text in my feed style on this batch", or a batch of clips that each need a native-looking title. Not for animated text, auto-captions (use the platform's own captions), posting, or designed motion-graphic titles (branded-ad-edit / reel-recut).

### edl-tighten
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/edl-tighten/` (2 files, SKILL.md 315 lines, with scripts/tools)

- Surgically remove awkward pauses, dead air, and long silences from a FINISHED voiceover-driven cut while keeping video, VO audio, word-synced captions, SFX hits, and the composition timeline in sync. Use when asked to "tighten the cut", "remove the pause at 0:41", "cut the dead air", "the gap between sentences is too long", "shave the silences", "it drags here", or when a revision round adds new cuts to an already-tightened edit. Finds gaps two ways (silencedetect + RMS envelope), chooses frame-quantized cut windows that never clip speech onsets, masks splices at cuts or attention magnets, executes ONE trim/concat filtergraph per stream from the original source, remaps the transcript through the EDL with scripts/remap-transcript.py (never re-whisper), and verifies with a re-scan plus frame extraction. Needs ffmpeg/ffprobe + python3 only. Not for building the edit itself (branded-ad-edit / talking-head-recut) or QA of a render you didn't cut (video-qa).

### embedded-captions
- **Job:** Captions, kinetic type and titles
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/embedded-captions/` (141 files, SKILL.md 260 lines, with scripts/tools)

Add captions or subtitles to an existing single-subject talking-head video without editing the footage. Use for plain verbatim captions, cinematic captions embedded behind the subject, VFX captions, “炸/特效/酷炫字幕,” or a named identity from the 35-style catalog. Route by visual identity, not by backend engine. The quiet `anchor` rail is the default; embed every word only when the user explicitly wants a fully cinematic treatment. The workflow runs locally end to end, including transcription and subject matting; split multi-shot footage before applying it.

### explainer-video
- **Job:** Explainers, data, charts and maps
- **Source:** iart-ai/explainer-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/explainer-video/` (3 files, SKILL.md 180 lines)

This skill should be used when the user asks to "make an explainer video", "turn this into a short explainer", "write a script and storyboard for a product video", "produce a how-it-works/onboarding video", "sync narration and captions", or "build a 30–90s animated explainer". Covers script→storyboard→scene build→narration/caption sync→edit→polish.

### explainroo
- **Job:** Explainers, data, charts and maps
- **Source:** vincentsch/explainroo
- **Licence:** licensed
- **Folder:** `.claude/skills/explainroo/` (1 files, SKILL.md 51 lines)

Make an explainer video (MP4) with a voice-over using explainroo. The voice is made on this computer and no API key is needed. Use when the user asks for an explainer, how-to, walkthrough, launch or tutorial video, an animated diagram with a voice-over, or a short for YouTube, Reels or TikTok.

### extreme-motion-design
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** dev-isaacmello/extreme-motion-design
- **Licence:** licensed
- **Folder:** `.claude/skills/extreme-motion-design/` (93 files, SKILL.md 113 lines, with scripts/tools)

Cria vídeos de motion design de nível de estúdio por código (Remotion/React), com trilha licenciada, SFX sincronizados, voz opcional (ElevenLabs ou modelo TTS local escolhido pelo hardware) e gates automáticos de lint e QA antes da entrega. Use quando pedirem motion design, motion graphics, vídeo animado, explainer, vídeo de produto ou lançamento, reel ou TikTok animado, tipografia cinética, logo animado, animação de UI, loop, narração ou voiceover para vídeo, ou técnicas como keyframing, zoom in e zoom out, motion smooth, morphing, rigging, frame a frame, cel animation, stop motion, rotoscopia, motion tracking, match moving, compositing, motion 3D, speed ramp, match cut, overshoot, parallax e transições. Also for animated video, kinetic typography, product launch video, explainer with voiceover, text to speech narration.

### faceless-explainer
- **Job:** Explainers, data, charts and maps
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/faceless-explainer/` (24 files, SKILL.md 235 lines, with scripts/tools)

Turn arbitrary text — an article, notes, a topic, a brief — into a faceless explainer video: there is no site or footage to capture, so the visuals are invented per scene (typography, abstract graphics, diagrams, data-viz). Use for topic explainers, concept breakdowns, how-tos, listicles. Not a video built from a website (/product-launch-video — promo or tour). Unclear → /hyperframes.

### ffmpeg-skill
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** kajisho5/ffmpeg-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/ffmpeg-skill/` (85 files, SKILL.md 218 lines, with scripts/tools)

Edit video and audio with local FFmpeg: cut, join, reframe, speed, captions, overlays, silence removal, sync, loudness, HDR to SDR, platform exports and checks. Use whenever the user mentions a video or audio file (mp4, mov, wav, m4a), footage, captions, a reel or short, YouTube/TikTok delivery, LUFS or ffmpeg, even without saying "edit". Needs FFmpeg 6.1+ and Python 3.10+; stdlib only, no cloud.

### figma
- **Job:** After Effects, Blender and desktop apps
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/figma/` (2 files, SKILL.md 132 lines, with scripts/tools)

Import Figma content into a HyperFrames composition — rendered assets, brand tokens, components, storyboard sections → reconstructed motion (frames read as states, not slides) (REST/CLI), connector-assisted motion when available, and shaders from a connector or native export. Use when the user pastes a figma.com link or asks to bring a Figma design, frame, logo, brand, or animation into a video/composition.

### free247editor
- **Job:** Other
- **Source:** riecodes/free247editor
- **Licence:** licensed
- **Folder:** `.claude/skills/free247editor/` (1 files, SKILL.md 129 lines)

The user's personal video editor in this free247editor folder. Use for "start" or first-time setup; "edit this", "edit mo to", or a video dropped in or added to inbox/; notes on a draft ("faster", "bigger captions", "approved", "final"); a horizontal or YouTube version; or changing the user's style or rules. Runs setup.mjs, free transcription, and the Herk Edit Kit pipeline in kit/, renders drafts to outbox/, and saves lasting notes to my-rules.md.

### frost-sequence-camera-orbit
- **Job:** Web, SVG, Lottie and code animation
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/frost-sequence-camera-orbit/` (83 files, SKILL.md 289 lines)

An orbiting camera follows an ice logo as it breaks apart, reforms into two text moments, and fades. HyperFrames block, 1920×1080, 22.5s, 216 variables.

### general-video
- **Job:** Talking-head and short-form reel editing
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/general-video/` (4 files, SKILL.md 165 lines, with scripts/tools)

Author or edit a custom HyperFrames composition when no specialized workflow fits, or when BRIEF.md sets flow: companion. Use for longer or multi-scene pieces, brand and sizzle reels, montages, static loops, static title cards, footage remixes, and freeform builds. Use motion-graphics instead for a short unnarrated motion-first unit, including an animated title. Route fresh creation through hyperframes before using this skill.

### generative-illustration
- **Job:** AI generation and B-roll (paid APIs: ask first)
- **Source:** iart-ai/generative-illustration-skills
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/generative-illustration/` (4 files, SKILL.md 120 lines)

This skill should be used when the user asks to "make an animated illustration", "animate an illustration", "make a generative motion piece" / "动态平面", "turn AI-generated art into something that moves", "make a poetic or ambient motion piece / motion poem", "make a visual metaphor", or "combine AI-generated visuals with code-driven motion". Covers generating isolated illustration assets with AI, compositing them as sprites, frame-accurate deterministic rendering, and the craft of expressive, concept-driven motion. NOT for data charts (use chart-animation), pure text (use kinetic-typography), or 3D/particles (use webgl-animation).

### glass-shard-title
- **Job:** Captions, kinetic type and titles
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/glass-shard-title/` (14 files, SKILL.md 87 lines)

Glass shards fly in through fog and tile themselves into the headline. HyperFrames block, 1920×1080, 12.16s, 19 variables.

### glassmorphism
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/web-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/glassmorphism/` (3 files, SKILL.md 177 lines)

This skill should be used when the user asks to "add a glassmorphism effect", "frosted glass UI", "Apple liquid glass style", "frosted blur card", "translucent glass panel animation", "make a frosted nav bar", "build a glass modal/dialog", "animate a glass card on hover", or "add a refracting liquid-glass hero". Covers frosted translucent panels with backdrop-filter blur, edge/specular highlights, SVG liquid-glass refraction, motion on hover/scroll/enter, and accessible reduced-transparency fallbacks.

### gsap-web
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/web-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/gsap-web/` (6 files, SKILL.md 225 lines)

This skill should be used when the user asks to "build a scroll animation", "add ScrollTrigger", "pin a section while scrolling", "scrub an animation to scroll", "create a hero timeline", "do a horizontal scroll section", "split text and animate words", "animate a layout change with GSAP Flip", "sync ScrollTrigger with Lenis", "Lenis smooth scroll jittery", "ScrollTrigger markers drift", "ScrollTrigger pins break with Lenis/Locomotive", or "set up smooth scroll with GSAP pinning". Covers GSAP timelines, ScrollTrigger, SplitText, Flip, and Lenis/Locomotive smooth-scroll sync for code-driven web motion.

### hook-splitter
- **Job:** Talking-head and short-form reel editing
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/hook-splitter/` (18 files, SKILL.md 98 lines, with scripts/tools)

- Split ONE long recording that contains many separate hooks/takes into a set of standalone videos — one per hook — and tighten each so there is no dead air, no stumble, and nothing said twice. Use whenever the user hands over a single long file and wants the pieces cut out: "split these hooks out", "there are 20+ hooks in here, make them each their own video", "cut these into individual clips", "one video per example", "chop this composite up", "tighten these and send them to me". Also use for the follow-up rounds — reading the reviewer's timeline notes back off the review canvas and applying them. Built for the prompt→result demo shape (the creator sets up a prompt, plays an AI-generated video, reacts) but the machinery is general: any long recording of repeated takes. NOT for styling a single finished reel with banners/captions (reel-recut), NOT for a brand-deal graphics edit (branded-ad-edit), and NOT the canvas itself for a single cut (video-review-canvas — this skill ships its own 21-up gallery variant).

### hook-variations
- **Job:** Talking-head and short-form reel editing
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/hook-variations/` (8 files, SKILL.md 226 lines, with scripts/tools)

- Combine ONE finished body cut with MANY hook clips to produce one standalone video per hook — the hook A/B batch you upload as separate ad creatives. Use whenever someone wants to "add all these hooks to this body", "combine this video with every hook in that folder", "make 21 versions with different openers", "swap the hook", "build hook variants", "test these hooks against the same body", or hands over one body file plus a folder of hooks and expects N finished videos out. Also use for the same shape with different words: intro variants, opener tests, cold-open A/B sets, or re-running an existing variant batch against a NEW cut of the body. Joins losslessly (body frames stay bit-identical), matches hook loudness to the body so the seam does not jump, and verifies with AVFoundation because an ffmpeg-only check cannot catch the parameter-set freeze that makes these files play fine in ffmpeg and stall in QuickTime. Do NOT use for editing a single video, adding captions, or cutting the hooks themselves out of a longer recording.

### howseen-motion-design
- **Job:** Motion principles, art direction and critique
- **Source:** howseen-ai/claude-motion-design
- **Licence:** licensed
- **Folder:** `.claude/skills/howseen-motion-design/` (15 files, SKILL.md 175 lines, with scripts/tools)

Code-only motion design pipeline (no After Effects) for Raphaël / Howseen: launch films, showreels, product promos, LinkedIn/X videos, meme clips. Use when asked to make a motion design video, a promo/launch film, a showreel, "remake this video", a video from a prompt (e.g. "make a 15s motion graphics video…"), to change a video's music/SFX, or to prepare memes for posts. Covers the brief → beat map → stills → seek(t) HTML engine → Playwright render → ffmpeg → music/SFX → QA flow, plus asset sourcing (Mixkit, Pexels, Unsplash, svgl, 21st.dev) and every gotcha hit so far.

### huashu-motion
- **Job:** Launch, product, ad and promo films
- **Source:** alchaincyf/huashu-motion
- **Licence:** licensed
- **Folder:** `.claude/skills/huashu-motion/` (45 files, SKILL.md 133 lines, with scripts/tools)

Motion graphics, launch videos and explainers as editable code. A director picks the motion language for your product; you point at frames to change them. 动画、发布片、解说视频，指着画面改。

### hyperframes
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/hyperframes/` (26 files, SKILL.md 129 lines, with scripts/tools)

Mandatory entry point: read this first for any request to make, create, edit, animate, or render a video, animation, or motion graphic, including a promo, explainer, captioned clip, title card, overlay, slideshow or interactive deck, Remotion port, or any HyperFrames HTML composition. Also use it to inspect, diagnose, validate, preview, publish, or batch-render an existing HyperFrames project. Inputs may be a website URL, GitHub PR, Figma design or URL, text or brief, existing footage, or music. It resumes project state, captures intent when applicable, selects and installs the owning workflow, and routes domain capabilities. HyperFrames is the default output framework unless the user explicitly chooses another framework for the deliverable or asks only to record a browser session.

### hyperframes-animation
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/hyperframes-animation/` (122 files, SKILL.md 85 lines, with scripts/tools)

All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the seven runtime adapters (GSAP default, plus Lottie, Three.js, Anime.js, CSS keyframes, Web Animations API, TypeGPU). Use for any motion or animation task: pick 2-4 rules and compose, or load a blueprint, or look up runtime-specific API (e.g. GSAP eases / Lottie player / Three.js mixer). Also covers auditing an existing composition's choreography (animation map) and 24 named text-animation effects. HyperFrames-native: single paused timeline, seek-safe, deterministic.

### hyperframes-audio
- **Job:** Sound, music and audio QA
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/hyperframes-audio/` (7 files, SKILL.md 476 lines, with scripts/tools)

Use when audio already placed in a HyperFrames composition needs to be mixed: fade-in/fade-out, crossfade, track gain or volume, volume automation, ducking, a music bed that fights a voiceover (voiceover carve), effects on a track (EQ, compressor, limiter, gate, saturation, delay, reverb, chorus, phaser, bitcrush), automation envelopes drawn on a track's volume or any effect parameter, or one submix bus carrying a chain, a fader and an automation clock for several tracks at once (`<hf-audio-group>`). Don't use for sourcing or generating audio — finding BGM, SFX, or making a voiceover is `/media-use`. Don't use for clip timing or track layout, which is `/hyperframes-core`.

### hyperframes-cli
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/hyperframes-cli/` (11 files, SKILL.md 164 lines)

Use the HyperFrames CLI development loop: init, add, catalog, capture, lint, check, snapshot, compare, grade-compare, preview, play, present, beats, keyframes, single or batch render, publish, cloud, cloudrun, feedback, lambda, doctor, browser, info, upgrade, skills, compositions, timeline, docs, benchmark, telemetry, transcribe, auth, tts, and remove-background. Also use when diagnosing build or render failures. validate, inspect, and layout are deprecated aliases; use check. Covers local, HeyGen-hosted cloud, AWS Lambda, and Google Cloud Run rendering.

### hyperframes-core
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/hyperframes-core/` (11 files, SKILL.md 97 lines)

The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class="clip"`, tracks, sub-compositions, variables, framework-owned media playback, deterministic-render rules, and validation. Read before writing composition HTML.

### hyperframes-creative
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/hyperframes-creative/` (79 files, SKILL.md 71 lines, with scripts/tools)

Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat planning, audio-reactive visuals, composition patterns, and brand / style decisions. For atomic motion patterns and scene blueprints, use `hyperframes-animation`.

### hyperframes-keyframes
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/hyperframes-keyframes/` (3 files, SKILL.md 262 lines)

Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe, Ken Burns treatment, camera move, visual match/whip handoff, or other seek-safe 2D/3D keyframes; also for GSAP, CSS keyframes, Anime.js, WAAPI, FLIP, paths, masks, SVG morph/draw, text trails, 3D depth, or `hyperframes keyframes` diagnostics. Don't use for broad scene strategy, brand design, media sourcing, captions, or general video planning.

### hyperframes-motion-reel
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** Sunwood-ai-labs/hyperframes-motion-reel-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/hyperframes-motion-reel/` (29 files, SKILL.md 412 lines)

ショーリール品質（Behance / OFFF / Awwwards級）のモーショングラフィックス動画を HyperFrames（HTML + GSAP + SVG + Canvas、Apache-2.0）で制作する。remotion-motion-reel の HyperFrames 版で、Remotion の Company License が不要な構成。テーマ・素材（キャラクター画像、音声など）から世界観・コピー・デザインシステム・タイムライン・サウンドを補完し、120BPM/60fps で拍同期した映像を実装・レンダリングまで行う。「HyperFramesでかっこいい動画」「ライセンスフリーでモーショングラフィックス」「ショーリールをHTMLで」などの依頼時に使用。

### hyperframes-registry
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/hyperframes-registry/` (12 files, SKILL.md 145 lines)

Search, install, and wire registry blocks and components into HyperFrames compositions. Use BEFORE hand-building any named visual — whenever a brief, a user, or a storyboard names a look, effect, treatment, or transition such as CRT scanlines, glitch, chromatic aberration, film grain, a shimmer sweep, a chart, a code or terminal window, a map, or a confetti burst — because roughly 400 hosted items already cover many of them and the search ranks all of them with nothing installed, no project, and no account. Also use when running hyperframes add or hyperframes catalog, installing one item or every block matching a tag, wiring an installed item into index.html, or working with hyperframes.json. Covers discovery, install locations, block sub-composition wiring, component snippet merging, and authoring a new block or component to contribute upstream (idea → scaffold → validate → PR).

### hyperframes-studio
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/hyperframes-studio/` (1 files, SKILL.md 75 lines)

Use when building or editing a HyperFrames project that people open in Studio: how the timeline should be laid out so it reads well (one caption track, one element kind per track, every scene a sub-composition) and where captions and key content may sit (safe zones). Don't use for how to perform an individual edit (split, trim, retime, volume, copy, swap): that is `creator-editing-recipes.md` in `/hyperframes-core`.

### ideogram4
- **Job:** AI generation and B-roll (paid APIs: ask first)
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/ideogram4/` (3 files, SKILL.md 130 lines)

Prompting patterns for Ideogram 4 text-to-image — best-in-class in-image text rendering and exact color/layout control via structured JSON captions. Use when generating images that need legible on-image text (title cards, thumbnails, logos, signage, CTAs), precise brand colors, or controlled spatial layout. Triggers include title slide image, thumbnail with text, on-image text, legible text in image, brand color palette image, bounding-box layout, Ideogram.

### isometric-animation
- **Job:** Explainers, data, charts and maps
- **Source:** iart-ai/explainer-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/isometric-animation/` (3 files, SKILL.md 178 lines)

This skill should be used when the user asks to "make an isometric animation", "build a 2.5D isometric scene", "create an isometric infographic", "animate an exploded diagram", "do an isometric city/stack build", "show stacked layers in iso", "extrude blocks with depth", or "add a gentle camera drift to an iso scene". Covers CSS 3D transforms, SVG iso planes, and Three.js OrthographicCamera for true 3D iso — no build step.

### javascript-animation
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/javascript-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/javascript-animation/` (10 files, SKILL.md 77 lines, with scripts/tools)

This skill should be used when the user asks to "draw every frame in JavaScript", "make an animation with no image assets", "animate this in code / on a canvas", "make a hand-drawn style animated video", "turn this into a short animated film", "make an animated explainer drawn in code", "make an animated story / picture book of my photos", or "make a zero-asset animation like the Opus 5.5 ones". Produces a single self-contained HTML file whose frames are computed on an HTML canvas (seekable, deterministic), renders it to MP4, and self-checks the result. Pairs with the soundtrack skill for code-synthesized music. NOT for charts from data (use chart-animation) or 3D/WebGL (use threejs-animation / shader-glsl from webgl-animation-skills); pure text motion and depth drawn by projection on the 2D canvas are in scope.

### jhonty-video-editing
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** JhontyBarreto/video-editing-skill
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/jhonty-video-editing/` (26 files, SKILL.md 82 lines, with scripts/tools)

Make and edit short-form videos (Reels, TikToks, Shorts, video ads, explainers, VSLs) with Remotion, ElevenLabs and 21st.dev. Covers the script, ElevenLabs voiceover with word timestamps, a speech-to-text check of every take, ElevenLabs music beds and sound effects, 21st.dev UI components and brand logos ported into Remotion scenes, captions synced to the voice, rendering, loudness normalising to -14 LUFS and a QA pass. Use when someone asks to make, edit, re-cut, resize or render a reel, short, video ad, VSL or any Remotion video, or to add a voiceover, captions, music or sound effects to one.

### kinetic-typography
- **Job:** Captions, kinetic type and titles
- **Source:** iart-ai/kinetic-typography-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/kinetic-typography/` (3 files, SKILL.md 156 lines)

This skill should be used when the user asks to "animate a headline", "make a kinetic typography video", "do a split-text reveal", "stagger text by character/word/line", "make a lyric or caption video", "animate a variable font weight", "put text on a path", or "create an animated title card". Covers reveal techniques in CSS, GSAP SplitText, Framer Motion, and Remotion.

### km-sound-design
- **Job:** Sound, music and audio QA
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/km-sound-design/` (5 files, SKILL.md 218 lines, with scripts/tools)

Generate and mix the full audio pass for a video edit with ElevenLabs — an SFX kit (whooshes, pops, impacts, count-ups, sub-drops, risers) generated, audited for the ~1/3 near-silent duds, and peak-normalized to −3dB; a music bed prompted by style descriptors (optionally style-matched to a reference track via spectrogram + BPM estimation); and the proven mix levels + ffmpeg verification recipe to sit it all under a spoken voiceover. Use when the user asks for "sound design", "SFX", "sound effects on this edit", "a music bed", "background music under the VO", "add whooshes/impacts", "a sub drop opener", "make the music feel like this track", or "mix/verify the audio" — and as the sound pass inside larger edit skills (branded-ad-edit, cinematic edits). Produces audited audio files + mix numbers; voiceover generation and clip placement live in the edit skills.

### lead-magnet
- **Job:** Briefs, pricing and client work
- **Source:** mcdenil-skills/AutoMontage-Agent
- **Licence:** licensed
- **Folder:** `.claude/skills/lead-magnet/` (4 files, SKILL.md 107 lines)

- Собирает лид-магнит к ролику в AutoMontage-Agent по запросу из «Пульта роликов»: дословное обещание, страница из заготовки бренд-пака, проверка фактов, PDF, тексты для раздачи, автопроверка и показ в пульте. Используй, когда во входящих есть строка «Лид-магнит: …», когда пользователь просит «сделай лид-магнит», «материал по кодовому слову», «гайд к ролику».

### lemo-opuscar
- **Job:** Launch, product, ad and promo films
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/lemo-opuscar/` (2 files, SKILL.md 24 lines, with scripts/tools)

Direct and produce a short film made entirely in code, in one of the styles of the Lemo-Opuscar library (e.g. Impasto Oil Painting 油画厚涂, Watercolor Brush 水彩笔刷, Ukiyo-e 浮世绘, Satellite Briefing 卫星简报, Exploded Teardown 产品拆解). Use when the user asks for a video, film, short, promo, explainer or animation (视频、短片、动画、宣传片) in a named style, including explainers built from real material such as satellite imagery, laser scans, CAD files or archive scans (数据解说、科普、产品拆解), and new films cut from real archive footage and documents (剪辑与纪实, e.g. 用档案影像剪一支新闻片); when they want a film about their own topic and haven't chosen a style (help them choose); when they want to change a style into their own, make their own style from a blank page, or use a style they saved (改风格、从空白开始、我的风格); when they start the skill without saying what they want; or when they ask which film styles there are. Not for plain editing, trimming or converting the user's existing video files.

### liam-motion-graphics
- **Job:** Motion principles, art direction and critique
- **Source:** Liamrjohnston/remotion-motion-graphics-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/liam-motion-graphics/` (30 files, SKILL.md 184 lines, with scripts/tools)

Add cached official-asset and product research preflight before reference selection and build authorization.

### lobzy-motion-design
- **Job:** Motion principles, art direction and critique
- **Source:** LobzyJay/motion-design-with-claude
- **Licence:** licensed
- **Folder:** `.claude/skills/lobzy-motion-design/` (6 files, SKILL.md 54 lines)

Use this skill whenever motion, animation, timing, easing, or composition over time is the subject. Triggers on "animate", "motion", "easing", "timing", "keyframe", "transition", "stagger", "loop", "bounce", "overshoot", "follow-through", "anticipation", "12 principles", "motion hierarchy", "composition for motion". Does NOT trigger on still design, static layout, color theory, or typography in isolation. Pair with aftereffects-motion or blender-motion when a tool is named. Load this first; specialists layer on top.

### logo-animation
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/motion-design-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/logo-animation/` (3 files, SKILL.md 148 lines)

This skill should be used when the user asks to "animate our logo", "make a logo intro/stinger", "build a brand reveal", "create an app splash animation", "loop a loader logo", "draw on our SVG mark", "morph an icon into the wordmark", or "sync the logo to a sound-logo". Covers web (SVG/Lottie), video, and app-splash delivery.

### loop-cover
- **Job:** Web, SVG, Lottie and code animation
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/loop-cover/` (1 files, SKILL.md 58 lines)

Turn a newsletter or blog cover into a seamless looping GIF at 896 x 640, 180 frames at 20fps. Only the one element you name moves, the loop is rotated so frame 1 shows the finished picture, and the seam is measured, not eyeballed. Use when someone says "animated cover", "make my cover move", "looping GIF cover", "newsletter cover GIF", "animate my thumbnail" or wants a cover that moves in the inbox without looking busy.

### lottie-animation
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/web-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/lottie-animation/` (3 files, SKILL.md 180 lines)

This skill should be used when the user asks to "add a Lottie animation", "play a .lottie or .json animation", "integrate a Bodymovin/After Effects animation on web or mobile", "control Lottie playback / segments", "make a scroll-driven Lottie", "recolor a Lottie at runtime", or "export an AE animation to Lottie". Covers dotLottie/lottie-web integration, playback control, interactivity, theming, and the AE export checklist.

### lt-lower-thirds
- **Job:** Captions, kinetic type and titles
- **Source:** iart-ai/lower-thirds-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/lt-lower-thirds/` (4 files, SKILL.md 57 lines, with scripts/tools)

Make animated lower thirds and other broadcast overlays (name straps, corner bugs, subscribe reminders, scripture or song titles) as transparent video files, drawn frame by frame in JavaScript on a canvas and rendered to WebM with alpha for OBS and browsers, or ProRes 4444 for Premiere Pro, DaVinci Resolve and Final Cut. Use when someone wants a lower third, a name title, a chyron, a stream overlay, a corner bug, or any graphic with a transparent background to lay over their own footage or livestream.

### ltx2
- **Job:** AI generation and B-roll (paid APIs: ask first)
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/ltx2/` (1 files, SKILL.md 256 lines)

AI video generation with LTX-2.3 22B — text-to-video, image-to-video clips for video production. Use when generating video clips, animating images, creating b-roll, animated backgrounds, or motion content. Triggers include video generation, animate image, b-roll, motion, video clip, text-to-video, image-to-video.

### makemyclip-editor
- **Job:** Talking-head and short-form reel editing
- **Source:** MakeMyClip/editor
- **Licence:** licensed
- **Folder:** `.claude/skills/makemyclip-editor/` (166 files, SKILL.md 355 lines)

AI-native video editor for any agent. Use when the user asks to edit, trim, splice, caption, zoom into, add a title card, transition between, remove silence from, chroma-key, stabilize, or render video files. Wraps FFmpeg in 19 deterministic tools and a session log; runs locally; no generative AI.

### manim
- **Job:** Explainers, data, charts and maps
- **Source:** iart-ai/manim-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/manim/` (5 files, SKILL.md 136 lines)

This skill should be used when the user asks to "make a math animation", "animate an equation", "use Manim", "make a 3Blue1Brown-style video", "plot or animate a graph/function", "visualize a math/physics/CS concept", "morph one formula into another", "animate a geometric proof", or "render a math explainer". Covers Manim Community Edition — Scenes, Mobjects, animations, LaTeX/MathTex, graphs, updaters/ValueTracker, 3D, and rendering to MP4/GIF via the CLI.

### map-animation
- **Job:** Explainers, data, charts and maps
- **Source:** iart-ai/map-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/map-animation/` (4 files, SKILL.md 184 lines)

This skill should be used when the user asks to "make a Vox-style map animation", "animate a map zoom", "draw a route on a map", "highlight a country/region", "use Google Earth Studio", "drop pins on a map and animate them", "pan/orbit a camera over a map", or "add map graphics to an explainer video". Covers Earth Studio→After Effects camera import, GeoJSON/SVG vector map motion, pins/routes/highlights/labels, the 12fps stutter cadence, and data-driven Remotion renders.

### media-use
- **Job:** Talking-head and short-form reel editing
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/media-use/` (90 files, SKILL.md 96 lines, with scripts/tools)

Agent Media OS, the single skill for every media need in a HyperFrames project. Resolve BGM, SFX, image, icon, brand logo, voice, color grade, or LUT into a frozen local file or paste-ready block + ledger record (one verb, `resolve`); generate via TTS / music / image models when the catalog misses; produce voiceover, transcription, captions, and background removal through one shared audio engine; operate on media (cut / reframe / transform); and reuse assets across projects. Also use for vague feedback that real footage looks dark, flat, boring, should feel retro/camcorder/print/ASCII, needs privacy, or needs a media reveal.

### micro-interaction
- **Job:** App demos, UI and screen capture
- **Source:** iart-ai/web-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/micro-interaction/` (4 files, SKILL.md 173 lines)

This skill should be used when the user asks to "add a hover/press effect", "animate a toggle or switch", "build an animated like button", "make a toast/snackbar slide in", "animate a drawer or modal", "animate list reordering or add/remove", "do a shared-element layout transition", or "polish UI feedback". Covers UI motion with Framer Motion (motion/react) and modern CSS.

### milestone-reveal
- **Job:** Launch, product, ad and promo films
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/milestone-reveal/` (1 files, SKILL.md 54 lines)

Make a 12-second looping milestone clip in code with Claude Code. Thousands of tiny points drift like a night sky, pull together into your real number (followers, subscribers, revenue, customers), a line draws underneath and the label settles in. Premium, not a party. Use when someone says "milestone video", "celebrate 10k followers", "animate my subscriber count", "number reveal", "particle number animation" or wants to mark a result on LinkedIn or Instagram.

### model-showdown
- **Job:** Launch, product, ad and promo films
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/model-showdown/` (1 files, SKILL.md 53 lines)

Give the same motion brief to three AI models, keep each first try, render all three the same way and stack them into one comparison video with model names and logos. Makes a 16:9 side-by-side for a newsletter and a 1080 x 1920 stacked reel for Instagram and TikTok. Use when someone says "compare three models", "same prompt three AIs", "model showdown", "which AI is the best motion designer", "side by side comparison video" or wants a fair head-to-head of AI outputs.

### mort1d-motion-graphics
- **Job:** Motion principles, art direction and critique
- **Source:** Mort1d/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/mort1d-motion-graphics/` (72 files, SKILL.md 447 lines, with scripts/tools)

Creates showreel-grade motion graphics videos entirely from code — HTML scenes rendered frame by frame in headless Chrome with real motion blur, plus an original score composed for each video on the same beat grid. It directs the film itself from whatever the person gives — their words, a site, a GitHub repository, an app, screenshots, their own video clips and photos, or reference clips — and sets the pace and the energy of the music from them. Use for any promo, ad, launch video, explainer, reel, Shorts or TikTok, intro, kinetic type or logo animation for a business, product, app, site, bot, channel or person, even when all you have is a link or a name.

### motion-art-direction
- **Job:** Motion principles, art direction and critique
- **Source:** iart-ai/motion-design-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-art-direction/` (3 files, SKILL.md 114 lines)

This skill should be used when the user asks to "direct a motion graphics video", "do creative/art direction for a video", "define a motion language", "set the tone and pacing", "make the animation feel consistent", "decide what to animate (and what not to)", "turn a brief/brand into motion choices", or needs the senior creative judgment that sits above specific techniques (gsap/lottie/shader). Covers motion language, tone & energy, pacing/rhythm, motion hierarchy, restraint, and cross-shot consistency.

### motion-background
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/motion-design-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-background/` (3 files, SKILL.md 279 lines)

This skill should be used when the user asks to "add an animated background", "build a mesh/gradient background", "make an aurora/shader background", "add constellation/particle background", "animated hero background", or "a subtle looping background behind content". Covers CSS mesh gradients, GLSL shader gradients (Three.js), canvas particle constellations, seamless loops, and reduced-motion/performance handling — fully self-contained.

### motion-brief-writer
- **Job:** Briefs, pricing and client work
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-brief-writer/` (1 files, SKILL.md 61 lines)

Turns a rough idea for an animated graphic into a precise build brief for Claude Code, in your own brand. Asks for anything essential first (exact numbers, size, length, brand), keeps real results apart from sample data, and never invents a figure. Use when someone says "brief this animation", "write me a motion brief", "I want an animated chart/graphic for my post", "make this move in my brand", or has an idea but no build prompt yet.

### motion-design-critique
- **Job:** Motion principles, art direction and critique
- **Source:** LobzyJay/motion-design-with-claude
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-design-critique/` (4 files, SKILL.md 54 lines)

Use this skill when something has gone wrong, looks wrong, or needs a second opinion. Triggers on: "something looks off", "this doesn't look right", "why is this happening", "script error", "render artifact", "the timing feels wrong", "animation looks robotic", "AE error", "bpy error", "Blender crashed", "nothing is moving", "wrong position", "wrong keyframe", "expression error", "the material looks fake", "shadows are wrong", "why does this look cheap", "critique this", "review this", "what's wrong with". Also triggers when the user is stuck and doesn't know why. Works with or without MCP attached.

### motion-doctrine
- **Job:** Other
- **Source:** heygen-com/hyperframes
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-doctrine/` (4 files, SKILL.md 175 lines, with scripts/tools)

GATEWAY — load FIRST before composing any HyperFrames animation or video. The high-level motion law that makes a multi-scene video feel like ONE continuous camera move instead of a stack of independently-animated slides. Covers the vector law (how you exit determines how you enter, incl. the Z scale-sign rule), the film's current, carrier elements, causal motion, the Seam Gate (build-gate enforcement), the ban on idle wobble (motion must PERFORM, not breathe), stillness-before-climax, and the sustained-motion routes. Routes to the low-level technique skills (cut-the-curve — the full catalog incl. waterfall entry + nudge curve, oversized-cursor, seam-craft). These rules SUPERSEDE generic / upstream motion guidance. [continuity, direction, vector, momentum, seam, transition, ease, performance, idle-motion, narrative-motion, film-grammar]

### motion-effects
- **Job:** Motion principles, art direction and critique
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-effects/` (2 files, SKILL.md 89 lines)

Build any of 16 premium motion effects from scratch in your own brand, as one 8-second looping HTML file with window.seek(seconds) so it exports frame-exact to MP4 or GIF. Interfaces (button to player, search to results, card to workspace, tabs to panels), data (chart morph, dashboard zoom, spring stack, magnetic dock), type (masked type, elastic type, text to layout, image reveal) and systems (perspective shift, glass focus, flowing paths, particle logo). Use when someone says "build the chart morph", "make a button that turns into a video player", "animate my logo with particles", "motion effect", "UI animation", "product animation", "animated dashboard", "kinetic type" or names any of the 16 effects.

### motion-graphics
- **Job:** Motion principles, art direction and critique
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/motion-graphics/` (23 files, SKILL.md 176 lines)

A short, design-led motion graphic where motion is the message — kinetic typography, stat count-up, chart/data-viz hit, logo sting / brand lockup, lower-third / callout / social overlay, animated map (highlight regions, connect places, zoom to a location), animated tweet / news-article / headline, webpage / UI animation (scroll, cursor, callouts), or fusing a real image's geometry into a chart. Usually under 10s (up to ~30s), no narration or live-action subject; renders to MP4 or transparent overlay. Longer / narrated / multi-scene → /general-video. Unclear → /hyperframes.

### motion-pricing
- **Job:** Briefs, pricing and client work
- **Source:** iart-ai/freelance-motion-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-pricing/` (5 files, SKILL.md 210 lines)

This skill should be used when the user asks to "quote a motion project", "estimate this animation job", "how much should I charge for this video", "what's my day rate", "build a quote", "price a 30-second explainer", or "is this estimate fair". It explains motion-design pricing models, the day-rate math, the cost drivers, and outputs a line-itemed quote with a worked example.

### motion-prompt-writer
- **Job:** Briefs, pricing and client work
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-prompt-writer/` (2 files, SKILL.md 56 lines)

Write a complete 8-part Claude Motion prompt (The bar, Format, The one rule, Look, Motion, Never, Before you finish, The scene) for one short looping motion graphic, in your own brand. Takes your brand (a website screenshot, a logo, hex codes, or nothing for the Apple-style default) and one moment you want to show, in plain words. Use when someone says "write me a Motion prompt", "turn this idea into a motion graphic", "fill in the 8 parts" or "make my motion brief". Outputs parts 1 to 7 as a reusable brief and part 8 as the scene, in one paste-ready code block.

### motion-reel
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** 10291124jcjc-dotcom/motion-reel
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-reel/` (23 files, SKILL.md 162 lines, with scripts/tools)

Make motion-graphics videos rendered entirely from code — product ads, brand promos, launch videos, showreels, animated explainers, 抖音/视频号/小红书 竖屏广告, 宣传片, 片头, 动态海报视频 — with original beat-synced music, exported as MP4 in 9:16, 1:1 and 16:9 from one timeline. Use this whenever the user asks for a 动态视频, 广告视频, 宣传视频, 动效, motion graphics, showreel, promo/launch/ad video, or wants a company, product, PPT, PDF or website turned into a video, even if they don't say "motion" or name this skill. Also use it to revise such a video (change copy, cut a scene, retime, new format). Not for editing camera footage, and not for 硅基废话 whiteboard episodes (use guiji-feihua-video).

### motion-video
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** bestagentkits/motion-video-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-video/` (22 files, SKILL.md 102 lines, with scripts/tools)

Produce beat-synced 1080p motion-graphic videos in HyperFrames (HTML + GSAP) with an AI voice-over, Vietnamese karaoke captions, SFX and generated music, in one of two proven styles (glass keynote or Spider-Verse-style comic). Use when the user asks for a launch/release/feature video, motion graphic, animated explainer or promo clip, or a restyle of an existing one.

### motion-video-director
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** mattypark/Motion-graphics-skill
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/motion-video-director/` (6 files, SKILL.md 440 lines, with scripts/tools)

Plan, direct, and produce code-drawn 2D/3D motion graphics and edited videos (reels, hooks, SaaS/product explainers, talking-head edits) on the user's local machine through any coding agent that has terminal + file access (Claude Code, Codex, Cursor, Claude Desktop, VS Code agents, etc.). Workflow: explain the process → user gives references + story → write a paste-ready ElevenLabs voiceover script → user generates and returns the MP3 → build, preview, render. Uses Canvas/SVG/p5.brush/Three.js/GSAP rendered in headless Chrome, Motion Canvas/Revideo, ffmpeg, small local AI models (cutout, transcription), plus LottieFiles, Freesound, Pexels/Pixabay, Firecrawl and ElevenLabs MCPs, and the Playwright MCP to browse any website visually (Pinterest, Behance, Dribbble, brand sites) and grab image/video assets by itself. Use when the user asks to make, edit, animate, caption, voice, or sound-design a video.

### motion-video-production
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** unclejobs-ai/motion-video-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/motion-video-production/` (89 files, SKILL.md 191 lines, with scripts/tools)

Plan, build and verify 15–90 second motion graphics, promo and character videos. Take a reference video apart with OpenCV into measured targets, then produce through gated stages (story, character, keyframes, clips, voice and music, assembly) on a bundled engine, Remotion (carry oracle, one-word cut template) or HyperFrames, and judge the rendered mp4 against the targets. Voice via ElevenLabs or Fish Audio through the composio CLI, a procedural score, mix and verify. Use for video production, reference matching, keyframes, character consistency and motion graphics assembly. 모션 그래픽·홍보 영상·캐릭터 영상 제작과 레퍼런스 영상 분석에 사용한다.

### moviepy
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/moviepy/` (1 files, SKILL.md 252 lines)

Python video composition with moviepy 2.x — overlaying deterministic text on AI-generated video (LTX-2, SadTalker), compositing clips, single-file build.py video projects. Use when adding labels/captions/lower-thirds to LTX-2 or SadTalker outputs, building short ad-style spots in pure Python without Remotion, or doing programmatic video composition. Triggers include text overlay on video, label LTX-2 clip, caption SadTalker output, lower third, build.py video, moviepy, Python video composition, sub-30s ad spot.

### music-to-video
- **Job:** Sound, music and audio QA
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/music-to-video/` (169 files, SKILL.md 208 lines, with scripts/tools)

Turn a music track (an audio file, a video to pull audio from, or a track generated from a mood brief) into a beat-synced video — lyric video, slideshow, or kinetic promo. The music drives all pacing; any user-supplied images/videos are cut onto the same beat grid, and a complete video needs zero assets. Narrated pieces → the input-matched workflow (see /hyperframes). Unclear → /hyperframes.

### naming-convention
- **Job:** Motion principles, art direction and critique
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/naming-convention/` (3 files, SKILL.md 171 lines, with scripts/tools)

- Name a batch of video deliverables so each filename says what the file actually is — subject, variant axis, and treatment — instead of `render-final-v3.mp4`. Use whenever more than two files are being handed over, and whenever someone says "rename these", "give these descriptive names", "I can't tell these apart", "name them so I know which is which", "put the product in the filename", "which one is the captioned version?", or is about to deliver a folder of variants, renders, exports, or cutdowns. Also use when naming a NEW batch before it ships, not just fixing an existing one — deciding the pattern up front is the cheap moment. Covers choosing the axes that vary, verifying the facts in a name before baking them into 40 files, keeping the subject map as data, and renaming idempotently without breaking a review canvas that already points at the old names.

### newsletter-promo
- **Job:** Launch, product, ad and promo films
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/newsletter-promo/` (1 files, SKILL.md 43 lines)

Turn a newsletter edition into a 12-20 second promo clip for LinkedIn, Instagram or X that drives people to read and subscribe. Hook question, three proof frames from the edition, then the newsletter name and where to read it. Use when someone says "promo for my newsletter", "trailer for this edition", "get people to my Substack", "teaser video" or "promote this issue".

### openart-broll
- **Job:** AI generation and B-roll (paid APIs: ask first)
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/openart-broll/` (1 files, SKILL.md 101 lines)

GENERATE B-roll, talking-head clips, and screen-blend motion-graphic overlays for an edit through the OpenArt MCP (Seedance, Kling, Wan, Gemini Omni, Grok Imagine, Nano Banana and more) — identity-referenced talking heads from a reference video, product/scene beats, and flat-black overlay clips generated per spoken line. Use when an edit needs generated footage or overlays and the OpenArt MCP is connected ("openart", "seedance", "generate an overlay/b-roll clip", "AI clip of me saying X"). NOT for capturing real websites (broll-capture), Arcads-backed generation (arcads-broll), or hand-authored composition cards (branded-ad-edit).

### orbit-card
- **Job:** Web, SVG, Lottie and code animation
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/orbit-card/` (13 files, SKILL.md 71 lines)

A single feature card orbits a dot sphere on approved Blender camera motion. HyperFrames block, 1920×1080, 10s, 4 variables.

### oversized-cursor
- **Job:** Other
- **Source:** heygen-com/hyperframes
- **Licence:** licensed
- **Folder:** `.claude/skills/oversized-cursor/` (1 files, SKILL.md 139 lines)

House-style oversized macOS cursor technique for HyperFrames launch videos. Load whenever a scene involves cursors or a pointer-led action, when kicking off a UI scene, when igniting a morph/transition/typing run with a click, or when a scene reads as static, dead, or stale and needs a cheap high-yield source of motion to carry the viewer's eye and segment them out of the stale state. Covers cursor size/look (incl. brand-motif cursors), the off-screen entry law, tip-targeting and the click tap, click-ignites-the-next-beat, and exit / cross-scene handoff.

### page-transition-animation
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/web-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/page-transition-animation/` (3 files, SKILL.md 218 lines)

This skill should be used when the user asks to "animate page or route transitions", "add a page transition or crossfade between views", "animate route changes in Next.js App Router", "use the View Transitions API", "AnimatePresence exit doesn't fire on navigation", or "Framer Motion exit animation not working / exit animation before unmount in Next.js". Covers enter/exit page-transition animation with the View Transitions API and Framer Motion, for Next.js App Router and general SPA routing.

### parody-short
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/parody-short/` (5 files, SKILL.md 130 lines)

Comedy shorts about a group's own life - a team's launch, quarter end, office move or leaving do; a club's season; a class's year; a family's Christmas - or about a shared topic everyone recognises (video calls, the return to the office), told in a borrowed genre (80s action intro, creature feature, Dickens Christmas ad, heist, nature documentary) and starring the group's real, animated photos or an invented cast. Covers mining the group's own context for in-jokes (chat, email, calendars, shared docs, plus domain tools like a CRM, helpdesk or git), mapping a genre's beats onto the real event, costuming and animating photos (image_edit then LTX), and per-genre look and sound. Use when someone asks for a fun, parody, spoof, holiday or "for the giggles" video about their team, colleagues, club, class or family, a party or all-hands video, or wants people's photos animated into a story.

### particle-system
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/webgl-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/particle-system/` (3 files, SKILL.md 229 lines)

This skill should be used when the user asks to "build a particle system", "make confetti/snow/smoke/sparks", "create a connected-dot/constellation network background", "add a flow-field or curl-noise particle effect", "render thousands of GPU particles with Three.js Points", or "animate emitters with forces". Covers per-particle integration, forces, flow fields, burst/continuous emission, spatial-grid connected dots, and GPU points + shaders.

### photo-slideshow
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/ecommerce-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/photo-slideshow/` (6 files, SKILL.md 167 lines)

This skill should be used when the user asks to "make a photo slideshow", "turn photos into a video", "create a photo montage video", "make a picture slideshow with music", "build a memories/recap video from photos", "add Ken Burns pan/zoom to photos", "sync slide changes to the music beat", or "render a video from a folder of images". Covers per-photo Ken Burns motion, transitions, beat-synced timing, mixed aspect-ratio handling, captions/dates, intro/outro cards, and templating a photo folder into a finished video.

### pixel2motion
- **Job:** Copy and clone a reference
- **Source:** nolangz/pixel2motion
- **Licence:** licensed
- **Folder:** `.claude/skills/pixel2motion/` (39 files, SKILL.md 238 lines, with scripts/tools)

Turn a raster logo (PNG/JPG/WebP/screenshot) into a clean minimal SVG with edge smoothness as the primary hard gate and IoU optimized as high as reasonably possible without a fixed global threshold, then into a choreographed logo animation delivered as standalone JS-rendered HTML, applying Disney's 12 animation principles. Use when asked to animate a logo, build a logo reveal / splash screen / brand intro, convert a logo image into animated SVG or HTML, add motion to a vectorized mark, or create loading/idle/hover motion for a brand mark. v2: also handles self-crossing draw-on choreography (split-fill, exact easing subdivision, tip glint), closed variable-width ribbon fitting, and quantitative motion QA (easing probe, ink-delta continuity sweep).

### playwright-recording
- **Job:** App demos, UI and screen capture
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/playwright-recording/` (2 files, SKILL.md 469 lines)

Record browser interactions as video using Playwright. Use for capturing demo videos, app walkthroughs, and UI flows for Remotion videos. Triggers include recording a demo, capturing browser video, screen recording a website, or creating walkthrough footage.

### pr-to-video
- **Job:** Launch, product, ad and promo films
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/pr-to-video/` (30 files, SKILL.md 271 lines, with scripts/tools)

Turn a GitHub pull request (a PR URL, owner/repo#N, or 'this PR' in a checked-out repo) into a code-change explainer video — changelog, feature reveal, fix, or refactor walkthrough built from the diff, commits, and files: the input is a code change, not a website. Not a product promo (/product-launch-video) or a no-PR topic explainer (/faceless-explainer). Unclear → /hyperframes.

### presentation-video
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/data-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/presentation-video/` (4 files, SKILL.md 201 lines)

This skill should be used when the user asks to "make an animated presentation", "turn a pitch deck into a video", "convert slides/a deck to video", "make a presentation video", "build a deck video", "narrate a slide deck as a video", or "auto-advance slides synced to a voiceover". Covers rebuilding slides as motion graphics with staggered build reveals, slide-to-slide transitions, and timing locked to per-slide narration.

### product-demo-video
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/ecommerce-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/product-demo-video/` (4 files, SKILL.md 203 lines)

This skill should be used when the user asks to "make a product demo video", "create an app demo video", "build a feature announcement video", "do a SaaS demo", "make a UI walkthrough video", "animate product screenshots into a demo", "add an animated cursor/click to a screenshot", or "zoom into part of a UI". Covers turning static screenshots/designs (not screen recordings) into a clean animated demo: device/browser frames, animated cursor + click ripple, zoom/pan to focal UI, callout annotations, step pacing, screen-to-screen transitions, and feature captions.

### product-film
- **Job:** Launch, product, ad and promo films
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/product-film/` (25 files, SKILL.md 60 lines, with scripts/tools)

Make a showreel-grade product film (landing-page loop, launch video, promo, demo reel, social cut) in code with Remotion, built on the product's own design system, components and voice. Use when someone asks for a product video, landing video, promo, launch film, explainer or "motion design video" for their app, SaaS or codebase. It asks what to include, then covers design discovery, story, music sync, transitions, review loops and a verified final render.

### product-launch-video
- **Job:** Launch, product, ad and promo films
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/product-launch-video/` (30 files, SKILL.md 262 lines, with scripts/tools)

Turn a product or marketing URL, pasted script, or brief into a product launch / promo video — SaaS promos, feature reveals, product demos, app and company launches. Use when the user wants to market, launch, promote, or reveal a product; the default for any commercial URL. Site tours / showcases of a website route here too — the brief carries the show-it-as-is intent. Unclear → /hyperframes.

### promo-video
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/ecommerce-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/promo-video/` (3 files, SKILL.md 172 lines)

This skill should be used when the user asks to "make a sale video", "create a promo video", "build a discount/percentage-off reveal", "animate a was→now price with a strike-through", "do a Black Friday / flash-sale / clearance video", "make a promo-code reveal with a countdown", or "batch a promo template across many products". Covers the offer-announcement arc — discount reveal, price strike-through, promo code, urgency, product shot, CTA — and product+offer data → many videos.

### qwen-edit
- **Job:** Copy and clone a reference
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/qwen-edit/` (4 files, SKILL.md 119 lines)

AI image editing prompting patterns for Qwen-Image (Qwen-Image-Edit-2511 by default, Qwen-Image-2.1 as a non-commercial Modal opt-in). Use when editing photos while preserving identity, reframing cropped images, changing clothing or accessories, adjusting poses, applying style transfers, or character transformations. Provides prompt patterns, parameter tuning, and examples.

### real-sfx
- **Job:** Sound, music and audio QA
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/real-sfx/` (1945 files, SKILL.md 498 lines, with scripts/tools)

Sound design for motion videos with REAL recorded sounds from the user's own libraries (a sorted main pack of whooshes, hits, risers, pops, chimes, keystrokes, foley, ambiences plus fallback libraries) and UI cues from uisfx, never synthesized. Finds the moments from the project's own cue list or from the synthesizer script that makes its sound, from a HyperFrames composition, from a screen recording (regions: typing, toasts, scrolls, clicks) or from the picture itself, picks and processes the sounds, places them on the exact frame at the level the author's own sounds had, keeps the music and voice, takes a synthesized layer baked into the render OUT instead of doubling it, and returns a new MP4, a separate SFX WAV track, a cue report and a self-critique scoreboard. Use whenever the user asks to add sound effects or SFX, sound-design, "озвучь", "добавь звуки", "сфх", whoosh/hit/riser/click/typing sounds, UI sounds, to replace synthesized or generated sounds with real ones, or to make a motion graphic, promo, explainer, UI animation, screencast, HyperFrames render, After Effects or Premiere project sound better, or complains the sound is synthetic, generic or out of sync, even if they do not say "skill" or name a library.

### real-sound
- **Job:** Sound, music and audio QA
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/real-sound/` (33 files, SKILL.md 199 lines, with scripts/tools)

Build premium, realistic soundtracks for code-made videos and animations from real licensed recordings - launch films, product and feature videos, UI walkthroughs, logo stings, explainers, trailers and animated shorts made with Remotion, HyperFrames, three.js, GSAP or any renderer. Use this whenever a video or animation needs sound design, SFX, foley, ambience, music, a soundtrack, a score, UI click / whoosh / riser / impact / logo-sting sounds, or a music edit to picture; whenever a synthesized or "random" sounding soundtrack must be replaced with real recordings; or when the user asks to source, license, credit, mix, master, critique or mux audio for a film. It covers cue lists from the picture, sourcing from Freesound / Mixkit / composer libraries with licence checks, a music edit at bar lines, a JSON sound design rendered by a deterministic mixer, measured QA (clicks, masking, harshness, sync, loudness) plus earshot listening, a multi-agent critique, mastering, credits and the mux.

### reanimate
- **Job:** Copy and clone a reference
- **Source:** NiazMorshed2007/reanimate
- **Licence:** licensed
- **Folder:** `.claude/skills/reanimate/` (439 files, SKILL.md 105 lines, with scripts/tools)

Clone a section, widget, page or animation from any reference (a live website URL, a screen recording, an mp4/mov/webm, a gif, a Lottie file, a prototype export) frame by frame into the user's own codebase, then record the clone and verify it against the reference frame by frame, iterating until timing, easing, sequence and layout match. Use whenever the user wants to clone, copy, replicate, recreate, reverse-engineer, port or "steal" a hero, section, widget, marquee, carousel, hover effect, page transition, loader, scroll animation or interaction from a site or video, says "make it look/feel/move like this", "same animation as", "match this exactly", or hands over a gif/video and asks to build it, including when they also want to add their own content, colours or extra features on top, or only want part of the reference (one section, one widget, a few seconds). Covers canvas, WebGL, WebGPU and three.js / 3D scenes (shaders, particles, globes, glTF models) as well as CSS and JS motion. Pixel-level matching of fonts, colours and spacing is done only when they ask for it.

### recap-video
- **Job:** Launch, product, ad and promo films
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/recap-video/` (8 files, SKILL.md 131 lines, with scripts/tools)

- Edit an event, conference, summit, trip, or behind-the-scenes recap from spoken takes and supplied B-roll. Choose the strongest take for each line, remove pauses and restarts, match footage to the narration, mix full-screen and split layouts, add captions and selective graphics, then render, verify and revise. Use for "recap video", "event recap", or "edit this summit like this reference"; not for a text summary or a product screen-demo edit.

### reel-editor
- **Job:** Talking-head and short-form reel editing
- **Source:** sunithvs/video-agent-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/reel-editor/` (34 files, SKILL.md 179 lines, with scripts/tools)

Edit talking-head / selfie videos into finished Instagram Reels, TikToks and YouTube Shorts with code-rendered motion graphics - face layouts that morph (split screen, picture-in-picture, punch-ins), kinetic text, captions (including English captions for Malayalam, Hindi or other non-English speech), b-roll from X/Twitter posts, websites and screen recordings, synced sound effects, and loudness mastering. Everything is drawn by one HTML file as a pure function of time and rendered frame by frame with Playwright + ffmpeg. Use this whenever the user drops a video into a folder and wants it edited, asks for a reel / short / TikTok, wants captions, subtitles, b-roll, motion graphics or sound design on a clip, or shares tweet / X links, product URLs or clips "to use when editing" - even if they only say "edit this video", "check the new video" or "make it like the last one".

### reel-export
- **Job:** Delivery, export and QA
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/reel-export/` (1 files, SKILL.md 50 lines)

Turn any horizontal or square motion video into a 1080 x 1920 Instagram Reel or TikTok that uploads cleanly. Headline and logos inside the safe zone, H.264, yuv420p, limited colour range, bt709, a silent audio track when there is no sound, and an ffprobe check before upload. Use when someone says "make this a reel", "vertical version", "export for Instagram", "TikTok version", "9:16 cut", "reel export" or has a 16:9 or 4:5 video that needs to go on a vertical feed.

### reel-from-donor
- **Job:** Talking-head and short-form reel editing
- **Source:** mcdenil-skills/AutoMontage-Agent
- **Licence:** licensed
- **Folder:** `.claude/skills/reel-from-donor/` (5 files, SKILL.md 316 lines)

- Превращает полезный разговорный Reels, Short или TikTok в авторский Reels с живыми, конкретными карточками: сначала разбирает донорский материал и проверяет факты, сначала предлагает готовый стиль, уникальный Creative Motion или монтаж по референсу, согласует CTA, дизайн и формат, затем показывает тексты карточек и лишь после утверждения создаёт анимацию и монтаж. Используй, когда пользователь даёт ссылку, видео или транскрипт чужого ролика и просит адаптировать, переделать, разобрать в карточки, сделать лайфхаки или ролик по донору.

### reel-recut
- **Job:** Talking-head and short-form reel editing
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/reel-recut/` (10 files, SKILL.md 200 lines, with scripts/tools)

- Recut a raw vertical talking-head reel into a finished short-form edit: a persistent title banner, word-synced karaoke captions, callout boxes for asides and comment-keyword CTAs, and tight silence-cut "talking over myself" pacing — all described in ONE JSON spec and rendered deterministically. Use when the user supplies a talking-head video and wants it edited, styled, or "made to match my other videos / this reference reel" — including "add my captions", "put the banner on it", "tighten the cuts / make it punchier", "cut the dead air", "add a callout when I say X", or "fix the part where I trip over my words". Also use to revise a reel-recut edit (change banner text, add/move a callout, remove a stumble, re-time captions), and for a graphics-free raw cut (pacing only) on brand-deal footage a client's editor will finish. Not for plain subtitles on untouched footage (embedded-captions), overlay graphic cards with the clip untouched (talking-head-recut), or a fully branded motion-graphics ad (branded-ad-edit).

### reel-style-clone
- **Job:** Talking-head and short-form reel editing
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/reel-style-clone/` (2 files, SKILL.md 144 lines)

- Reverse-engineer a reference reel's editing style frame-by-frame into a replicable STYLE GUIDE plus per-line BUILD DIRECTIVES, then apply that style to the user's own footage. Use whenever someone hands over (or points at) an existing short-form video and says "edit mine like this", "clone this editing style", "match this reel", "why does this edit feel so good — copy it", "break down how this video is edited", "steal this creator's style", or "make my video look like [reference]". The output is analysis + a build plan, not a rendered video — the actual edit is built by branded-ad-edit (or reel-recut for the simple banner/caption look) from the directives this skill produces. Not for cloning a STATIC image ad (image-ad-clone), plain subtitles (embedded-captions), or an edit with no reference to match.

### reel-turnkey
- **Job:** Talking-head and short-form reel editing
- **Source:** mcdenil-skills/AutoMontage-Agent
- **Licence:** licensed
- **Folder:** `.claude/skills/reel-turnkey/` (10 files, SKILL.md 523 lines)

- Собирает ролик под ключ в AutoMontage-Agent: проверяет исходник, транскрибирует речь, показывает автору черновую нарезку своей съёмки без графики, готовит один полный пакет ТЗ со сценами, текстами, кадрированием, анимацией и аудиопробой, ждёт явного утверждения, рендерит ReelScenes и сам проводит визуальный и звуковой QA. Обязательно используй, когда пользователь просит «смонтируй ролик», «ролик под ключ», «сделай Reels/Shorts», «собери lesson» или даёт видео для монтажа, даже если не называет навык. В новом чате сначала предлагает готовый стиль, уникальный Creative Motion или монтаж по референсу. Запросы анимации без камеры направляет в motion-reel.

### reference-to-motion
- **Job:** Copy and clone a reference
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/reference-to-motion/` (1 files, SKILL.md 43 lines)

Turn references you admire into a scene-by-scene Claude Motion prompt for your own topic and brand. Takes a video for the moves (screenshots, frames or a contact sheet of a reel or ad) and, optionally, a look reference for the style (a website, a brand, a moodboard). Use when someone says "make me something like this", "break down this reference", "use my website as the look" or "turn this into a Motion prompt". Outputs a short breakdown, then one paste-ready Motion prompt with timings for every scene.

### remotion-best-practices
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/remotion-best-practices/` (148 files, SKILL.md 116 lines)

Router for all Remotion skills

### remotion-bits
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** av/remotion-bits
- **Licence:** licensed
- **Folder:** `.claude/skills/remotion-bits/` (4 files, SKILL.md 144 lines)

Animation components and utilities for Remotion video projects. Use when building Remotion compositions with text animations, gradient transitions, particle effects, 3D scenes, or staggered motion effects. Provides example bits (complete compositions) and reusable components that can be installed via jsrepo.

### remotion-ffmpeg-skill
- **Job:** Footage editing: cuts, ffmpeg, scenes, beat sync
- **Source:** kajisho5/remotion-ffmpeg-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/remotion-ffmpeg-skill/` (76 files, SKILL.md 89 lines, with scripts/tools)

Make motion graphics on real footage with Remotion, driven by measurements from ffmpeg-skill: animated captions timed from an SRT/VTT file, automatic jump cuts that drop the silences ffmpeg-skill measured (with punch-in zooms and captions re-timed), and motion that hits on measured audio peaks and scene cuts. Every composition takes its length, fps and frame size from the probed source; every render is verified (frame count, fps, size, audio) and inspected with a contact sheet, then delivered through ffmpeg-skill templates (YouTube, Reels, TikTok, Shorts, X) and its compliance check. Use this skill when the user wants Remotion, React video, motion graphics, animated captions or titles over a video, jump cuts / silence removal with motion, audio-reactive or beat-synced graphics, or a programmatic video built from a real recording -- even when they do not say "Remotion". Needs Node.js and ffmpeg-skill; local, no API keys.

### remotion-to-hyperframes
- **Job:** Frameworks: HyperFrames and Remotion
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/remotion-to-hyperframes/` (77 files, SKILL.md 130 lines, with scripts/tools)

Port an existing Remotion (React) composition''s source to HyperFrames HTML. Use ONLY on an explicit ask to port/convert/migrate/translate a Remotion source — one-way, Remotion-only. A passing Remotion mention, reference-only code, or "make something like my Remotion video" is a fresh build (/general-video). Unclear → /hyperframes.

### remotion-video
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** iart-ai/motion-design-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/remotion-video/` (3 files, SKILL.md 194 lines)

This skill should be used when the user asks to "make a video with Remotion", "create a programmatic/data-driven video in React", "render an MP4/GIF from code", "animate with useCurrentFrame/interpolate/spring", "sync video to audio/beats", or "render a templated video per record headlessly". Covers building React compositions and rendering them via CLI or @remotion/renderer.

### remotion-video-director
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** BayramAnnakov/remotion-video-director
- **Licence:** licensed
- **Folder:** `.claude/skills/remotion-video-director/` (7 files, SKILL.md 391 lines)

Interactive guide for creating Remotion videos - from strategic concept to rendered MP4. Use when the user wants to create a video, make a Remotion project, build a product demo video, generate a launch video, make a recurring content template, create a marketing video, or says "I need a video for...", "help me make a video", "video for my product", "remotion video". Covers the full creative process: expert deliberation, scenario design, build, and review. Works alongside the official remotion-dev/skills for API-level guidance.

### reverse-any-video
- **Job:** Other
- **Source:** heygen-com/hyperframes
- **Licence:** licensed
- **Folder:** `.claude/skills/reverse-any-video/` (5 files, SKILL.md 39 lines)

Rebuild any video file as an editable HyperFrames project - motion graphics, talking heads, live action or AI-generated footage - checked against the original frame by frame. Use to reverse, recreate, remake, replicate or copy a video, or 「复刻这个视频」「照着这个视频做一个」.

### rossark-motion-skill
- **Job:** Web, SVG, Lottie and code animation
- **Source:** rossark0/rossark-motion-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/rossark-motion-skill/` (26 files, SKILL.md 410 lines, with scripts/tools)

Bring anything drawn to life with calm, believable motion. It covers characters and creatures (gliding pupils, blinks, breathing, head tilts), full-body acting (landing, waving, leaning, levitating, kicking a ball), plants, fabric, fire, smoke, water, weather, lights, machines, vehicles, icons, logos, charts and whole scenes. Use it whenever someone asks to animate an illustration, an icon, a mascot or a scene, to make something "feel alive", to add idle motion, to turn a static drawing into a living one, or to recreate the motion of a reference video. Comes with a small motion engine and templates for React Native (react-native-svg + Reanimated) and SwiftUI (TimelineView + Canvas), tools that measure a reference video frame by frame, and offline rendering to video, in a phone frame too. The method also works on the web.

### runpod
- **Job:** AI generation and B-roll (paid APIs: ask first)
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/runpod/` (1 files, SKILL.md 232 lines)

Cloud GPU processing via RunPod serverless. Use when setting up RunPod endpoints, deploying Docker images, managing GPU resources, troubleshooting endpoint issues, or understanding costs. Covers all 5 toolkit images (qwen-edit, realesrgan, propainter, sadtalker, qwen3-tts).

### seam-craft
- **Job:** Other
- **Source:** heygen-com/hyperframes
- **Licence:** licensed
- **Folder:** `.claude/skills/seam-craft/` (1 files, SKILL.md 70 lines)

Render-correctness doctrine for scene-to-scene seams in HyperFrames launch videos — the prerequisites that make transitions composite correctly on the master timeline. Load when assembling the master timeline / index.html, when a white flash appears at a cut or crossfade seam (especially on dark films), when reasoning about why a transition opacity dip shows through, or when verifying the render-side mechanics of how overlapping scene wrappers blend. Covers the opaque stage-ground (#root background) white-flash guard and how the injector overlaps wrappers, holds final frames, ping-pongs tracks, and stamps lint-clean template code onto the master timeline. Does NOT contain the per-transition catalog — see the transition registry for individual transition entries.

### shader-glsl
- **Job:** 3D, WebGL and shaders
- **Source:** iart-ai/webgl-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/shader-glsl/` (3 files, SKILL.md 210 lines)

This skill should be used when the user asks to "write a fragment shader", "make a GLSL gradient/noise/plasma background", "create an image transition (dissolve, displacement, glitch)", "add distortion or chromatic aberration", "build an SDF shape shader", "wire up a Three.js ShaderMaterial with uniforms", or "do GPU post-processing". Covers GLSL fragment shaders, noise/fbm, SDFs, domain warping, transitions, and Three.js integration.

### short-form-video
- **Job:** Talking-head and short-form reel editing
- **Source:** iart-ai/tiktok-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/short-form-video/` (3 files, SKILL.md 155 lines)

This skill should be used when the user asks to "make a Reels/TikTok/YouTube Shorts video", "build a short-form video template", "write a hook for a short", "edit for retention", "add pattern interrupts", "make a video loop", "fix the first 3 seconds", "pace cuts for a vertical video", or "set up 9:16 safe areas". Covers the hook→retention→loop grammar of vertical short-form (distinct from a launch hype film).

### shot-composition
- **Job:** Motion principles, art direction and critique
- **Source:** iart-ai/motion-design-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/shot-composition/` (3 files, SKILL.md 185 lines)

This skill should be used when the user asks to "compose a frame", "set up a grid", "plan shot composition", "place the focal point", "decide where elements enter and exit", "add a parallax/camera move", "adapt a layout for 16:9 / 9:16 / 1:1", or "keep content inside safe areas". Covers grids, safe areas, focal hierarchy, and 2D/3D camera framing.

### slideshow
- **Job:** Launch, product, ad and promo films
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/slideshow/` (2 files, SKILL.md 530 lines)

Author a HyperFrames slideshow — a presentation, pitch deck, or interactive deck with discrete slides, fragment reveals, branching, hotspot navigation, and built-in presenter mode with speaker notes; also converts an existing page into a deck. Output is a navigable deck, not a rendered MP4. If the user didn't explicitly ask for a slideshow, confirm before authoring. Unclear → /hyperframes.

### soundtrack
- **Job:** Sound, music and audio QA
- **Source:** iart-ai/javascript-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/soundtrack/` (5 files, SKILL.md 46 lines, with scripts/tools)

This skill should be used when the user asks to "add music to the animation", "make the music in code", "synthesize a soundtrack", "compose background music that fits the cuts", "sync the music to the video", "check if the audio lines up with the picture", or "the music is too sudden / startling". Covers a code-synthesized score that lives inside the animation page (Web Audio API, rendered offline to WAV), AI-generated or user-supplied music, and an automatic check that cuts land on the beat without a startling jump in loudness.

### style-sampling
- **Job:** Other
- **Source:** heygen-com/hyperframes
- **Licence:** licensed
- **Folder:** `.claude/skills/style-sampling/` (2 files, SKILL.md 54 lines)

Make a new episode in a proven video style - Collage Explainer, Finance Explainer, Animated Science Explainer, 3D Brand Explainer, 3D True Crime - on the person's topic. Use for "an episode of", "in the style of", "sample this style", 「用这个风格做一集」. One video to copy is reverse-any-video.

### svg-animation
- **Job:** Web, SVG, Lottie and code animation
- **Source:** iart-ai/web-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/svg-animation/` (3 files, SKILL.md 167 lines)

This skill should be used when the user asks to "animate an SVG", "make a line draw itself on", "do a stroke draw-on / signature animation", "morph one shape into another", "move an element along a path", "animate an icon/logo", or "animate an SVG gradient or filter". Covers stroke-dashoffset draw-on, path morphing, motion-along-path, and animated icons/gradients/filters via CSS, SMIL, and GSAP.

### synthetic-ui-demo
- **Job:** App demos, UI and screen capture
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/synthetic-ui-demo/` (1 files, SKILL.md 155 lines)

Product demo and release-notes videos with no screen recording. Rebuild the app's screens as static React from its source code, then drive them in Remotion with a scripted cursor and camera (lib/components Stage + Cursor). Use when making a product walkthrough, feature demo, release-notes or changelog video for an app whose source you can read, or when a Playwright recording would be flaky, need test data, or go stale. Triggers include synthetic demo, rebuild the UI, release video, feature walkthrough, product demo from source, scripted cursor, camera zoom on UI, no screen recording.

### take-one
- **Job:** Launch, product, ad and promo films
- **Source:** talsiach/take-one
- **Licence:** licensed
- **Folder:** `.claude/skills/take-one/` (182 files, SKILL.md 259 lines, with scripts/tools)

Turn a short request into a finished short film rendered from code, working like a studio team of twelve jobs (strategist, creative director, writer, voice director, art director, storyboard artist, cinematographer, composer, sound designer, editor, reviewer, social copywriter). For launch and product videos, explainers, music videos, brand and story films. It learns the brand from its site, pitches the best route first (code, real-looking pictures, moving shots from a video model) with prices, asks whether to run to a finished first take or work in stages, always asks before spending money, credits or heavy usage, has a fresh reviewer score the cut against a bar, and takes notes on frames in a local review room.

### talking-head
- **Job:** Talking-head and short-form reel editing
- **Source:** iart-ai/talking-head-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/talking-head/` (11 files, SKILL.md 64 lines, with scripts/tools)

Create an AI talking head from the user's own photos plus a voice sample, or from a self-recorded video by extracting face frames and speech. Use an authorized cloned or existing ElevenLabs voice and a new script to generate speaking shots with fal MiniMax H3, narration and editable motion graphics, then render an MP4. Use for AI avatars, presenter videos, personal explainers and scripted on-camera clips. For a recording that only needs graphics without generating new speech, use a recording-editing workflow instead.

### talking-head-b-roll
- **Job:** Talking-head and short-form reel editing
- **Source:** iart-ai/b-roll-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/talking-head-b-roll/` (6 files, SKILL.md 95 lines, with scripts/tools)

Add b-roll motion graphics to a talking-head video. Transcribes the recording with word timings, decides line by line when the speaker is shown, when a graphic is laid over them and when a full-frame graphic covers them, draws each graphic from what is actually said (numbers, comparisons, steps, key words) in JavaScript on a canvas, and renders the finished MP4 with the original sound, plus the b-roll alone with alpha for an editor. Use when someone has a recording of a person talking to camera (a talking head, a spoken explainer, a course lesson, an ad read, a podcast clip) and wants it more engaging to watch, wants b-roll, or wants motion graphics added to it.

### talking-head-image-overlays
- **Job:** Talking-head and short-form reel editing
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/talking-head-image-overlays/` (5 files, SKILL.md 115 lines, with scripts/tools)

- Edit a talking-head video in the "uncut take + stacked image overlays" style: ONE continuous take that is never cut, with the entire sense of pace carried by hard-cut overlays landing on content nouns — a short serif title plate, found-footage rectangles above the eyeline, opaque full-frame skeleton-UI cards, raw prompt text on black, word-by-word karaoke captions, and a CTA banner that arrives early and never leaves. Use when someone says "edit this like that reel where images pop up while he talks", "add image overlays to my talking head", "make the cards that build themselves", "that style where a graphic appears on every keyword", "uncut talking head with graphics", or hands over a reference reel in this style. Also use to add a single act of it (just the cards, just the inserts) to existing footage. NOT for plain subtitles (embedded-captions), a banner + karaoke reel (reel-recut), unbranded overlay cards on untouched footage (talking-head-recut), or a fully branded motion-graphics ad (branded-ad-edit).

### talking-head-recut
- **Job:** Talking-head and short-form reel editing
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/talking-head-recut/` (28 files, SKILL.md 1218 lines)

Package an existing talking-head / interview / podcast video with timed, designed GRAPHIC OVERLAY cards — kinetic titles, lower-thirds, data callouts, quotes, side panels, picture-in-picture — synced to the transcript, on a 16:9 / 9:16 / 4:5 canvas of your choice; the clip plays untouched underneath. Trigger on "graphic overlays", "on-screen graphics", "package / dress up my video". Not plain subtitles (/embedded-captions). Unclear → /hyperframes.

### tenfold-video-edit
- **Job:** Talking-head and short-form reel editing
- **Source:** tenfoldmarc/video-edit-skill
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/tenfold-video-edit/` (43 files, SKILL.md 169 lines, with scripts/tools)

Turns raw 9:16 talking-head clips into a finished, premium Instagram reel end to end: picks the cleanest take of every line across your clips, cuts dead air, punches in from 4K, cuts you out of the background for words behind your head, applies one of three designed looks (bold kinetic words, cool girl, cool dude), builds animated UI inserts with parallel sub-agents, adds subtle sound design, and checks every cut frame by frame inside the Reels safe zone. Trigger with /video-edit or phrases like 'edit these clips', 'I dropped clips in my downloads', 'cut this into a reel', 'make this reel look fire'.

### terminal-inserts
- **Job:** Captions, kinetic type and titles
- **Source:** Liamrjohnston/remotion-motion-graphics-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/terminal-inserts/` (5 files, SKILL.md 155 lines)

Authentic, restrained Remotion terminal inserts with mandatory format/background intake and zero neon or glow.

### testimonial-video
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/ad-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/testimonial-video/` (4 files, SKILL.md 196 lines)

This skill should be used when the user asks to "make an animated testimonial", "create a quote video", "build a review video", "turn a customer testimonial into a graphic", "animate a customer review", "make a social proof video", "add an animated star rating", or "turn a list of reviews into videos". Covers quote typography, staggered line reveals, kinetic emphasis on key phrases, animated star ratings, the author block (name/role/avatar/company), and templating one card across many quotes.

### text-message-animation
- **Job:** Captions, kinetic type and titles
- **Source:** iart-ai/text-message-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/text-message-animation/` (4 files, SKILL.md 220 lines)

This skill should be used when the user asks to "make a fake text message video", "animate an iMessage conversation", "create a text story video", "do a chat reply animation", "WhatsApp/SMS conversation video", "typing indicator animation", "render a chat thread to a video", or "batch text-message videos from a script/CSV". Covers sent/received bubble layout, staggered appear timing with typing indicators, read receipts/timestamps, per-message pop sound-sync, 9:16 safe-area, and data-driven render from a messages array.

### text-to-lottie
- **Job:** Web, SVG, Lottie and code animation
- **Source:** diffusionstudio/lottie
- **Licence:** licensed
- **Folder:** `.claude/skills/text-to-lottie/` (23 files, SKILL.md 162 lines)

Create, edit, or fix Lottie/Bodymovin JSON animations for the local Skia Skottie player. Use for text-to-Lottie, SVG/logo/type animation, loaders/icons, state feedback, UI microinteractions, lower thirds, diagrams, data/stat/chart animations, product promos, scene/camera motion, visual effects, scene edits, slots/controls, and Skottie debugging.

### threejs-animation
- **Job:** 3D, WebGL and shaders
- **Source:** iart-ai/webgl-animation-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/threejs-animation/` (4 files, SKILL.md 252 lines)

This skill should be used when the user asks to "build a 3D hero section or WebGL background", "animate a Three.js scene", "play or crossfade GLTF animation clips", "move/lerp the camera or link it to scroll", "render thousands of objects with InstancedMesh", "set up React Three Fiber (R3F) motion", "add bloom/DOF post-processing", or "keep a Three.js/R3F animation smooth and leak-free (dispose geometries/materials/textures, free GPU memory on unmount)". Covers scenes, render loops, camera moves, GLTF AnimationMixer, instancing, scroll-linked 3D, R3F, and animation performance/disposal.

### tiktok-lower-thirds
- **Job:** Captions, kinetic type and titles
- **Source:** iart-ai/tiktok-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/tiktok-lower-thirds/` (3 files, SKILL.md 146 lines)

This skill should be used when the user asks to "make an animated lower third", "add lower thirds", "create a name tag/name lower third", "build broadcast titles", "animate a title/name/role caption", "do a speaker name overlay", or "template lower thirds across a list of names". Covers enter/exit animation (slide/wipe/mask reveal), in/out timing & dwell, safe-area & broadcast conventions, name-vs-role type hierarchy, brand styling, and rendering one design across many names.

### title-sequence-3d
- **Job:** Captions, kinetic type and titles
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/title-sequence-3d/` (1 files, SKILL.md 53 lines)

Make a cinematic 3D title sequence (8-15 seconds) in code with Claude Code and Three.js. A camera moves through a lit scene, such as a rainy street at night with brand names as neon signs, then a big question or title lands. Use when someone wants a scroll-stopping opener, a film-style intro, "3D intro", "cinematic opening", "title sequence" or a hook for a video, reel or newsletter.

### ultimate-video-editor
- **Job:** Other
- **Source:** Rajbharti06/Ultimate-Video-Editing-Skills
- **Licence:** licensed
- **Folder:** `.claude/skills/ultimate-video-editor/` (32 files, SKILL.md 600 lines)

Transforms any AI code editor into a god-level video editor with 50+ years of craft. Covers ALL editing disciplines: narrative structure, every cut type, transitions, cinema-grade color grading (including movie-level grading, LUT equivalents, scene matching), sound design, motion graphics (Disney's 12 principles, GSAP, Lottie, Three.js), kinetic typography, compositing, speed ramping, subtitles (5 styles), AI-native workflows, and platform-optimized export. When this skill is active, the agent edits like a veteran — every cut intentional, every frame earning its place. Works with FFmpeg, Remotion, HyperFrames, MoviePy, Manim. READ THIS SKILL for ANY video editing, color grading, animation, or motion design task.

### video-delivery-specs
- **Job:** Delivery, export and QA
- **Source:** iart-ai/freelance-motion-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/video-delivery-specs/` (6 files, SKILL.md 167 lines)

This skill should be used when the user asks "what are the specs for Instagram Reels / TikTok / YouTube / broadcast", "export settings for social", "what aspect ratio and bitrate", "how do I repurpose 16:9 to 9:16", "safe area / title-safe for vertical", "pre-delivery checklist", or "collect files for handover". It outputs per-platform spec sheets, a cutdown matrix, captioning/accessibility notes, and a QC + collect-files checklist.

### video-design
- **Job:** Motion principles, art direction and critique
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/video-design/` (5 files, SKILL.md 126 lines)

Visual design for videos - colour by act, type scale, chart and layout rules for 16:9 and 9:16 scenes, a design.md handoff that any design skill can fill, and a contact-sheet critique of the render. Use when designing or refining how a video looks (title cards, data scenes, slides, a whole video's palette), when a scene looks generic or busy, when choosing colours for a video, or when /design or /scene-review asks for visual work. Works on its own with a brand, or takes direction from a design source such as taste-skill, Anthropic's frontend-design, or the user's own design skill.

### video-director
- **Job:** Motion principles, art direction and critique
- **Source:** win4r/video-director
- **Licence:** licensed
- **Folder:** `.claude/skills/video-director/` (50 files, SKILL.md 389 lines, with scripts/tools)

Direct, build and verify short videos that are written as code and rendered frame by frame (HTML/Canvas/SVG/Three.js, GSAP or Remotion → MP4 or a live page). Covers motion graphics, product launch films, promos, explainers, kinetic typography, data stories, lyric and music videos, character and illustrated shorts, animated loops and social reels. Use this skill whenever someone asks to make, animate, storyboard, prompt for, review or fix a video, trailer, reel, intro, launch film, animated explainer or "motion graphics", even from a one-line request like "make a 15s video for my app" that never mentions code. Also use it when an existing coded video feels slow, out of sync, hard to read, or like generic AI output. It does not cover editing live-action footage or prompting pixel video models, though its story and timing principles still apply to those.

### video-edit-pipeline
- **Job:** Talking-head and short-form reel editing
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/video-edit-pipeline/` (2 files, SKILL.md 320 lines)

MASTER orchestration skill for producing a finished short-form video from raw talking-head footage. Use for ANY request to edit, produce, recut, or "make an ad/reel out of" talking-head footage — with or without a style reference — including "edit this video", "edit this like the reference reel", "turn this clip into a finished reel", "do the full edit", "make this look like their winning ads", or a revision request on a previously delivered edit. It routes every stage to the right specialist skill (reel-style-clone, branded-ad-edit, reel-recut, arcads-video-edit, recap-video, talking-head-image-overlays, hook-splitter, edits-hook-overlay, sound-design, ai-audio-sound-design, video-qa, video-review-canvas, edl-tighten, hook-variations, naming-convention, capcut-export) and owns the intake → style → edit → QA → deliver → revise loop end to end. Do NOT use for plain captions on untouched footage or single generated clips.

### video-motion-craft
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** vibegameengine/video-motion-craft
- **Licence:** licensed
- **Folder:** `.claude/skills/video-motion-craft/` (21 files, SKILL.md 172 lines, with scripts/tools)

Create and edit video with cinematic motion — Remotion (React video) for motion graphics, reels, intros, promos, titles and game trailers, plus FFmpeg/Whisper for editing real footage (trim, jump-cut, captions, overlays, speed). Load ALWAYS before the first line of video code. Triggers — "make a video", "edit this video", "reel", "Shorts/TikTok", "intro", "logo animation", "titles", "captions", "promo video", "cinematic", "sync to music", "hit the beat", "the video looks cheap/generic/AI-made", "game trailer", "store/showcase video", "gameplay capture", Remotion, ffmpeg, motion graphics, video render.

### video-production
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** Aaryan-Kapoor/video-production-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/video-production/` (7 files, SKILL.md 148 lines, with scripts/tools)

End-to-end narrated video production with research, source extraction, storyboard/script, Manim/ffmpeg visuals, TTS voiceover, QC, archival backups, and optional local/Tailscale hosting. Use when the user asks to make, create, generate, render, or produce a video, explainer, paper walkthrough, product demo, briefing, daily summary video, Manim animation, or narrated presentation.

### video-qa
- **Job:** Delivery, export and QA
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/video-qa/` (8 files, SKILL.md 273 lines, with scripts/tools)

- Four-layer QA for a rendered video edit — run it on any .mp4/.mov you or a pipeline just produced. Use when asked to QA / check / verify / audit a render or export, hunt clipped words, duplicate dialogue at cuts, dead air, splice clicks, black / frozen / flash frames, loudness (LUFS) or clipping problems, confirm a fix after a re-render, or build an inspection packet (contact sheet + waveform + transcript) for a suspect timestamp. L1 = ffmpeg/ffprobe technical checks, L2 = transcript edit-boundary checks mapped through the EDL, LF = optional per-frame rule checks (text in the platform-UI zones of a vertical video, a graphic covering a face, likeness against a reference photo for AI clones), L3 = optional Gemini watch+listen pass on a 480p proxy, L4 = targeted inspection packets. Needs only ffmpeg/ffprobe; whisper, TYPESAFE_API_KEY and GEMINI_API_KEY unlock the deeper layers.

### video-review-canvas
- **Job:** Delivery, export and QA
- **Source:** krusemediallc/video-editor-agent
- **Licence:** no licence: local use only, git-ignored
- **Folder:** `.claude/skills/video-review-canvas/` (9 files, SKILL.md 296 lines, with scripts/tools)

Publish a finished (or draft) video cut to a frame.io-style review canvas on here.now — a player with a frame-accurate scrubber, persistent timeline notes, version comparison, replies, resolution and evidence, and a clickable beat map — then read those notes back before the next cut. Use this to DELIVER any video edit for review: reel recuts, brand-deal edits, motion-graphics ads, carousel videos, YouTube cuts, sizzle reels. Trigger whenever a cut is ready to show, or on "send me the video", "put this on a canvas", "let me leave notes on the timeline", "frame.io style", "get me a link to review this", "publish the new version", or "what notes did I leave?" — even if the canvas is never named. Delivering a cut as a bare file attachment or a local preview link instead of a canvas link is the failure this skill exists to prevent. NOT for image or slide galleries (plain here-now publish), and not for making the video itself (branded-ad-edit / hyperframes).

### video-shotcraft
- **Job:** End-to-end motion-graphics video pipelines
- **Source:** Vincentwei1021/video-shotcraft
- **Licence:** licensed
- **Folder:** `.claude/skills/video-shotcraft/` (1070 files, SKILL.md 286 lines)

Create cinematic product videos from frontend projects or webpages with Remotion, real page captures, shot cards, the Ink Press template, beat sync and sound design. Use for full product promos, reproducing Ink Press, single shot-card effects, or finding, adding, replacing and aligning sound effects in an existing product video or shot, including candidate-only SFX searches. 用真实页面、镜头卡与 Ink Press 模板制作产品宣传片；用户要求用 video-shotcraft 做视频、复刻模板、制作单镜头，或给已完成的产品片/镜头找音效候选、加音效、换音效、对齐声音时使用。

### video_toolkit
- **Job:** Talking-head and short-form reel editing
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/video_toolkit/` (1 files, SKILL.md 484 lines)

Make short explainer videos from a brief with claude-code-video-toolkit — submit a scene spec, poll a job, get a QC-checked MP4. Also covers the individual tools (AI voiceover, images, clips, music, talking heads) for custom work.

### vox-explainer
- **Job:** Explainers, data, charts and maps
- **Source:** charlie947/motion-graphics-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/vox-explainer/` (1 files, SKILL.md 87 lines)

Make a short Vox-style documentary explainer (30-60 seconds) entirely in code with Claude Code. Torn paper, halftone texture, bold condensed type, motion on twos. Use when someone says "make a Vox-style video", "explainer video about...", "why does X happen", or wants a documentary-style motion graphic for LinkedIn, Instagram or YouTube without After Effects or a video generator.

### whiteboard-animation
- **Job:** Explainers, data, charts and maps
- **Source:** iart-ai/explainer-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/whiteboard-animation/` (4 files, SKILL.md 154 lines)

This skill should be used when the user asks to "make a whiteboard animation", "draw-on explainer", "VideoScribe style", "hand-drawn explainer video", "animate a sketch being drawn", "do a doodle/scribe video", "show a hand drawing the illustration", or "animate handwriting appearing on a whiteboard". Covers SVG stroke draw-on, a marker hand that follows the path tip, staggered reveal, erase/wipe transitions, and narrated export.

### wireframe-portal-title
- **Job:** Captions, kinetic type and titles
- **Source:** installed before the manifest (see CLAUDE.md)
- **Licence:** see the skill folder
- **Folder:** `.claude/skills/wireframe-portal-title/` (7 files, SKILL.md 70 lines)

A wireframe portal bursts open, the title comes through, then its letters swap into a second phrase. HyperFrames block, 1920×1080, 8s, 9 variables.

### wrapped-video
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/explainer-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/wrapped-video/` (5 files, SKILL.md 207 lines)

This skill should be used when the user asks to "make a Spotify Wrapped style video", "build a year in review / year-in-review video", "create a personalized data video", "generate a recap video", "build a wrapped video generator", "turn a data table into shareable videos", or "make per-user stat videos". Covers the data row → one shareable video pattern, the Wrapped scene grammar (big-number reveals, top-X lists, superlatives), animated data counters, vertical 9:16 framing, and batch-rendering many personalized videos from one template.

### youtube-editor
- **Job:** Talking-head and short-form reel editing
- **Source:** sunithvs/video-agent-skill
- **Licence:** licensed
- **Folder:** `.claude/skills/youtube-editor/` (34 files, SKILL.md 113 lines, with scripts/tools)

Edit full-length horizontal YouTube videos (5-60 min talking heads, explainers, tutorials, screen recordings) into finished 1920x1080 uploads - automatic jump cuts that remove pauses, zoom changes on every cut, chapter cards and YouTube chapter timestamps, lower thirds, stock b-roll and royalty-free music from free APIs, occasional motion graphics, English subtitles (.srt, translated for Malayalam / Hindi / other speech), a description with credits, and a thumbnail. Rendered in resumable chunks with Playwright + ffmpeg. Use this whenever the user wants a YouTube video (not a Short or Reel) edited, drops a long recording or several takes in a folder, asks for jump cuts, chapters, subtitles, b-roll or a thumbnail for YouTube, or says "full length", "long video", "podcast", "tutorial" or "YouTube video". For vertical Shorts / Reels / TikToks use the reel-editor skill instead.

### youtube-intro-outro
- **Job:** Launch, product, ad and promo films
- **Source:** iart-ai/youtube-video-skills
- **Licence:** licensed
- **Folder:** `.claude/skills/youtube-intro-outro/` (3 files, SKILL.md 173 lines)

This skill should be used when the user asks to "make a YouTube intro", "create a channel intro", "build a logo sting/bumper", "design an outro / end screen / end card", "add subscribe and next-video cards", "make an intro animation", "build a reusable intro template", or "sync the logo reveal to an audio sting". Covers the 3-5s branded intro, the last-20s end-screen outro inside YouTube's element safe zones, timing conventions, audio-sting sync, and a swap-the-brand template.

### youtube-stats
- **Job:** Delivery, export and QA
- **Source:** digitalsamba/claude-code-video-toolkit
- **Licence:** licensed
- **Folder:** `.claude/skills/youtube-stats/` (1 files, SKILL.md 70 lines)

How published videos are doing on YouTube, and what to learn from it. Views, likes, comments and subscribers per video, plus watch time, retention and traffic sources (Shorts feed, search, external) with the Analytics scope, saved as snapshots so trends show; GitHub traffic beside it to see whether YouTube sends people to the repo. Use when asked how a video or the channel is doing, which title, cover or genre worked, whether to make more of something, or for a weekly stats check.

## Tools and command-line programs these skills use

| Tool | What it is | Install / location |
|---|---|---|
| `tools/openverse_sfx.py` | CC0 sound-effect fetcher (Openverse/Freesound) → `assets/sfx/openverse/` + `credits.json` | in repo; page size ≤ 10 (larger queries time out) |
| `earshot` | Measures and describes sounds Claude can't hear; ranks, critiques, times | `bash tools/setup_sfx.sh` (pinned) |
| `real-sfx` scripts | Cue list → real recordings placed on frames → mix + critique | `.claude/skills/real-sfx/scripts/`; `REAL_SFX_CONFIG`, `REAL_SFX_INDEX` |
| `om` | huashu-motion CLI (grab, new, check, still, render, studio) | `bash tools/setup_skill_clis.sh`; `OM_CHROME` |
| `explainroo` | Word-synced explainer renderer with an offline Kokoro voice | `bash tools/setup_skill_clis.sh`; `EXPLAINROO_CHROME`; `explainroo doctor --fetch` |
| `argo` | Playwright demo → narrated product video | `bash tools/setup_skill_clis.sh`; add `kokoro-js@1` in the demo project for local TTS |
| reanimate scripts | Capture / compare / sheet (bun + Playwright 1.64) | `PLAYWRIGHT_BROWSERS_PATH=tools/pw-compat` |
| video-director scripts | `qa_video.py` (loudness, flashes, pops, flat frames, sheets), `check_timeline.py` | Python 3 + Pillow (fixed by the setup script) |
| Lemo-Opuscar library | 66 code-made film styles + render tools + real-instrument sampler | `tools/lemo-opuscar` (see CLAUDE.md) |
| Whisper | Word-level transcription for captions (`small` cached; `medium` for hard names) | preinstalled `whisper` |
| DeepFilterNet3 | Speech noise reduction used on talking heads (`videos/*/tools/denoise.py`) | scratch install + `~/.cache/DeepFilterNet/DeepFilterNet3` |
| `auto-editor` | Cuts silence / motionless / black stretches, speed ramps, editor XML export (Unlicense) | `bash tools/setup_skill_clis.sh` (pip, `~/.local/bin`); add `--progress none` to keep logs short |
| `scenedetect` | PySceneDetect: shot boundaries and scene lists from long clips | same (pip) |
| `moviepy`, `ffmpeg-python`, `librosa` | Python video assembly, ffmpeg bindings, beat/tempo analysis (`beat-sync-edit`) | same (pip) |
| `automontage` | AutoMontage-Agent engine: auto-montage of talking heads, motion reels, review UI (Remotion 4.0.536 + faster-whisper) | `bash tools/setup_skill_clis.sh`; engine in `tools/skill-repos/mcdenil-skills_AutoMontage-Agent`; `automontage doctor`, `node scripts/cli.js demo` |
| `ffmpeg-skill` scripts | 87 ffmpeg capabilities; `scripts/_contract.py doctor` checks the machine | in the skill folder, stdlib only |
| `synfig` 1.5 | Synfig Studio's CLI renderer: vector 2D cut-out/bone animation from `.sif`/`.sifz` files to PNG sequences or video (`synfig f.sif -t png -o f.png`) | apt, via `bash tools/setup_skill_clis.sh` |
| `pencil2d` 0.6 | Hand-drawn 2D (bitmap + vector) frame animation; renders `.pclx` from the command line (`QT_QPA_PLATFORM=offscreen pencil2d in.pclx -o out.mp4`) | same (apt) |
| `pyopenvdb` 10 | DreamWorks' OpenVDB sparse volumes (smoke, clouds, fire) from Python: build grids, write `.vdb` for Blender to render | same (apt `python3-openvdb`); `python3.12 -c "import pyopenvdb"` |
| Theatre.js 0.7, SVG.js 3.2 | Keyframed motion with a timeline editor (`@theatre/studio`) and a seekable sequence (`sheet.sequence.position = t`, so frame-exact renders); SVG drawing and animation | `tools/web-anim` (`npm ci`); bundle into a page with the film's own build step |

## Considered and not installed (Nov 16 2026 list)

| Repo | Why not |
|---|---|
| digitalpublisher/video-shotcraft, SunCl8/video-shotcraft-skill, JohnChow90/video-shotcraft, simpletibr/simplicio-remotion | Copies of `video-shotcraft` (Vincentwei1021's is installed) |
| remotion-dev/remotion | Its skills are for Remotion's own maintainers (PRs, releases); `remotion-best-practices` covers using it |
| wendymardigian-prog/Editor-IA-Pro | No licence; its skills are copies of others, and two need the paid inference.sh cloud |
| metiutek/editorvideo-ai (vedit), MartinDelophy/ai-video-editor (Timeline Studio), WeftCut, OpenChatCut, openfilm, OpenTake | Editor apps (desktop or browser UI, some with cloud accounts), not skills; vedit could be added as an MCP server if wanted |
| palmier-io/palmier-pro | Proprietary since v0.7.6 |
| storytold/effectcraft (ArtCraft) | No licence; an AI image/video app |
| artbyjazi/autoclip, Magerko/ReelsMaker-Pro | Apps (long video → clips with an LLM; batch reel converter) |
| mifi/lossless-cut, GraphiteEditor/Graphite | Desktop GUI apps |
| motion-canvas/motion-canvas, midrender/revideo | Frameworks installed per project with npm when a film uses them |
| Zulko/moviepy, kkroening/ffmpeg-python, Breakthrough/PySceneDetect, WyattBlue/auto-editor | Installed as Python tools (above), not cloned |
| heygen-com/hyperframes, charlie947, howseen-ai, Mort1d, iart-ai/motion-skills | Already installed earlier |
| zhuyansen, inginjadipro, sasateguh, devanasolver, Thedurancode, 26medias, BehiSecc, wilwaldon (indexes) | Link lists, nothing to install |
| soyenriquerocha/ai-video-editor | Does not exist on GitHub |

## Open-source animation tools (Nov 16 2026 list)

| Repo | Status |
|---|---|
| synfig/synfig, pencil2d/pencil, AcademySoftwareFoundation/openvdb, theatre-js/theatre, svgdotjs/svg.js | Installed (tools table above), tested here |
| opentoonz/opentoonz | Not installed: a desktop GUI app (Studio Ghibli's base) with no Linux package or headless renderer; building it from source needs ~2 GB and still only gives the GUI |
| NatronGitHub/Natron | Not installed: node compositor, no apt package; the portable Linux build (~600 MB unpacked) includes `NatronRenderer` for headless renders. Ask first; disk is tight. ffmpeg + code compositing cover the same jobs here |
| freemocap/freemocap | Not installed: markerless motion capture needs 2+ camera recordings of a person and ~1.5 GB of PySide6/MediaPipe/OpenCV; useful only with that footage |

## Skills built into Claude (not in this repo)

These come with the Claude Code environment rather than from `.claude/skills/`:
- `dataviz`, `artifact-design`, `artifact-diagramming`, `artifact-capabilities`
- `session-start-hook`, `update-config`, `keybindings-help`, `code-review`, `simplify`, `fewer-permission-prompts`, `loop`, `claude-api`, `run`, `plugin-authoring`, `init`, `security-review`
- the `anthropic-skills:*` set (docx, pptx, xlsx, pdf, deep-research, skill-creator and others)
