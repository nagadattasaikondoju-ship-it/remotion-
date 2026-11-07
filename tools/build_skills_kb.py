# Build docs/skills-knowledge-base.md from every .claude/skills/*/SKILL.md (+ tools/skill-repos.json for sources).
#   python3 tools/build_skills_kb.py        (re-run after installing or removing skills)
import os, re, json, datetime
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SK = os.path.join(ROOT, ".claude", "skills")
OUT = os.path.join(ROOT, "docs", "skills-knowledge-base.md")
manifest = {m["skill"]: m for m in json.load(open(os.path.join(ROOT, "tools", "skill-repos.json")))}

def front(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    m = re.match(r"^---\s*\n(.*?)\n---", t, re.S)
    fm = m.group(1) if m else ""
    name = re.search(r"^name:\s*['\"]?([^'\"\n]+)", fm, re.M)
    d = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:\s|\Z)", fm, re.M | re.S)
    desc = d.group(1).strip() if d else ""
    if desc.startswith(("|", ">")): desc = desc[1:]
    desc = " ".join(desc.split()).strip("'\"")
    return (name.group(1).strip() if name else None), desc, len(t.splitlines())

# job categories (first match wins); names are this repo's installed folder names
CATS = [
    ("After Effects, Blender and desktop apps", r"after-?effects|blender|figma|capcut"),
    ("Delivery, export and QA", r"qa|delivery|export|review"),
    ("Sound, music and audio QA", r"sfx|sound|earshot|audio|soundtrack|music|acestep|elevenlabs|audiogram"),
    ("Talking-head and short-form reel editing", r"talking-head|reel|tenfold|branded-ad|edl|hook|short-form|makemyclip|capcut|edit-pipeline|arcads-video|media-use|video_toolkit|general-video|edits-hook"),
    ("Captions, kinetic type and titles", r"caption|kinetic|typograph|lower-third|title|text-message|article-highlights|terminal-inserts|glass-shard|wireframe-portal|canopy"),
    ("Launch, product, ad and promo films", r"launch|product|promo|ad-creative|apple|cinetic|take-one|huashu|lemo|newsletter|pr-to-video|testimonial|recap|wrapped|youtube-intro|model-showdown|milestone|countdown|slideshow|photo|presentation|music-to-video"),
    ("Explainers, data, charts and maps", r"explain|chart|data|diagram|infographic|map|manim|whiteboard|vox|isometric"),
    ("App demos, UI and screen capture", r"argo|demo|playwright|broll-capture|synthetic-ui|micro-interaction"),
    ("Copy and clone a reference", r"reanimate|reference|style-clone|pixel2motion|qwen"),
    ("Web, SVG, Lottie and code animation", r"gsap|lottie|svg|javascript|60fps|accessible|page-transition|loop-cover|orbit|cuboid|code-slice|frost|glassmorph|ascii|particle|motion-background|logo|rossark"),
    ("3D, WebGL and shaders", r"three|webgl|shader|blender|3d|title-sequence"),
    ("Frameworks: HyperFrames and Remotion", r"hyperframes|remotion|dsk-|moviepy"),
    ("AI generation and B-roll (paid APIs: ask first)", r"arcads|openart|ltx2|runpod|ideogram|generative|b-roll"),
    ("Motion principles, art direction and critique", r"principle|critique|art-direction|motion-design|motion-graphics|motion-effects|color|shot-composition|beat-sync|cinematic|camera|brand|naming|video-director|howseen|lobzy|liam|mort1d"),
    ("Briefs, pricing and client work", r"brief|pricing|client|prompt-writer|creative"),
]
def cat(n):
    for c, rx in CATS:
        if re.search(rx, n): return c
    return "Other"

rows = []
for d in sorted(os.listdir(SK)):
    p = os.path.join(SK, d, "SKILL.md")
    if not os.path.isfile(p): continue
    name, desc, lines = front(p)
    m = manifest.get(d)
    src = m["from"] if m else "installed before the manifest (see CLAUDE.md)"
    lic = ("licensed" if m["licensed"] else "no licence: local use only, git-ignored") if m else "see the skill folder"
    files = sum(len(fs) for _, _, fs in os.walk(os.path.join(SK, d)) if "node_modules" not in _)
    has_scripts = os.path.isdir(os.path.join(SK, d, "scripts")) or os.path.isdir(os.path.join(SK, d, "tools")) or os.path.isdir(os.path.join(SK, d, "bin"))
    rows.append(dict(folder=d, name=name or d, desc=desc, cat=cat(d), src=src, lic=lic, lines=lines, files=files, scripts=has_scripts))

def first_sentence(s, n=170):
    s = re.split(r"(?<=[.!?])\s", s, 1)[0]
    return (s[:n - 1] + "…") if len(s) > n else s

L = []
L.append("# Skills knowledge base\n")
L.append(f"Generated {datetime.date.today().isoformat()} by `python3 tools/build_skills_kb.py` from every `.claude/skills/*/SKILL.md` in this repo. "
         f"**{len(rows)} project skills.** Re-run the script after installing or removing skills.\n")
L.append("""## How the skills fit together (house rules win)

- **Read first, every job:** `CLAUDE.md`, `docs/playbook/sound-design.md`, `docs/playbook/short-form-editing.md`, and `docs/playbook/oneloop-brand.md` for One Loop work.
- **Sound for every video:**
  1. Openverse (`tools/openverse_sfx.py`, CC0 recordings)
  2. `real-sfx` (place sounds on the frame)
  3. `earshot` / `real-sound` (analyse, refine, QA the mix)
  - Never hand-synthesise SFX outside this pipeline.
  - Never run `earshot llm` (it uploads audio to Gemini) unless asked.
- **Paid APIs, ask first:** ElevenLabs, Arcads, RunPod, Ideogram, OpenArt, LTX, Higgsfield/Seedance/Kling/Suno (take-one), and the cloud TTS options in argo. Local voices by default (explainroo Kokoro, argo `kokoro-js`).
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
""")

# category index
L.append("## Index by job\n")
by = {}
for r in rows: by.setdefault(r["cat"], []).append(r)
order = [c for c, _ in CATS] + ["Other"]
for c in order:
    if c not in by: continue
    L.append(f"### {c} ({len(by[c])})\n")
    L.append("| Skill | What it does | Source |")
    L.append("|---|---|---|")
    for r in by[c]:
        src = r["src"] if "/" in r["src"] else "earlier install"
        L.append(f"| [`{r['folder']}`](#{r['folder'].lower()}) | {first_sentence(r['desc']).replace('|', '/')} | {src} |")
    L.append("")

# full catalogue
L.append("## Full catalogue (A–Z)\n")
L.append("Each entry gives the skill's own description (its trigger text), where it came from, its licence, and whether it ships scripts or tools.\n")
for r in rows:
    L.append(f"### {r['folder']}")
    meta = [f"**Job:** {r['cat']}", f"**Source:** {r['src']}", f"**Licence:** {r['lic']}",
            f"**Folder:** `.claude/skills/{r['folder']}/` ({r['files']} files, SKILL.md {r['lines']} lines{', with scripts/tools' if r['scripts'] else ''})"]
    if r["name"] != r["folder"]: meta.append(f"**Frontmatter name:** `{r['name']}`")
    L.append("- " + "\n- ".join(meta))
    L.append("")
    L.append(r["desc"] or "_(no description in frontmatter)_")
    L.append("")

L.append("""## Tools and command-line programs these skills use

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

## Skills built into Claude (not in this repo)

These come with the Claude Code environment rather than from `.claude/skills/`:
- `dataviz`, `artifact-design`, `artifact-diagramming`, `artifact-capabilities`
- `session-start-hook`, `update-config`, `keybindings-help`, `code-review`, `simplify`, `fewer-permission-prompts`, `loop`, `claude-api`, `run`, `plugin-authoring`, `init`, `security-review`
- the `anthropic-skills:*` set (docx, pptx, xlsx, pdf, deep-research, skill-creator and others)
""")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(L))
print(OUT, len(rows), "skills;", {c: len(v) for c, v in by.items()})
