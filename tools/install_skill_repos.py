# Install the motion-graphics / video-editing skill repos the user collected (Oct 2026) into .claude/skills/.
#   python3 tools/install_skill_repos.py            clone (pinned commits) into tools/skill-repos/, then install
#   python3 tools/install_skill_repos.py --src DIR  install from existing clones in DIR (<owner>_<repo>, iart/<pack>)
#   python3 tools/install_skill_repos.py --only owner/repo,owner/repo   (re)install just those repos; the rest of the manifest is kept
# Every SKILL.md folder becomes .claude/skills/<name>. A name that clashes with an installed skill, with another repo's
# skill, or that is too generic next to this repo's own house rules gets the repo's prefix (folder and frontmatter).
# Repos without a licence are installed for use but git-ignored (not re-published); this script restores them.
# Tool repos without skills (After Effects bridges, Claude-Editor) are cloned to tools/skill-repos/ for reference only.
import os, re, shutil, subprocess, sys, json
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SKILLS, CLONES = os.path.join(ROOT, ".claude", "skills"), os.path.join(ROOT, "tools", "skill-repos")
I = "iart-ai/"
REPOS = [  # (owner/repo, commit, prefix, licensed)
    ("charlie947/motion-graphics-skills", "229022e", "cg", True),
    ("howseen-ai/claude-motion-design", "3d90d34", "howseen", True),
    ("LobzyJay/motion-design-with-claude", "a4d48c5", "lobzy", True),
    ("Mort1d/motion-graphics-skills", "7f0c371", "mort1d", True),
    ("krusemediallc/video-editor-agent", "bbbc1a4", "km", False),
    ("tenfoldmarc/video-edit-skill", "3f01f2e", "tenfold", False),
    ("digitalsamba/claude-code-video-toolkit", "9a3e865", "dsk", True, None, {"sparse": ["/.claude/skills/", "/skills/", "/LICENSE"]}),   # Nov 16: updated (adds video-design, blender, parody-short, youtube-stats)
    ("MakeMyClip/editor", "7820598", "makemyclip", True),
    ("Liamrjohnston/remotion-motion-graphics-skill", "b860c79", "liam", True),
    ("diffusionstudio/lottie", "3c72912", "ds", True),
    ("nolangz/pixel2motion", "e9faedb", "p2m", True),
    (I + "tiktok-video-skills", "2a77533", "tiktok", True), (I + "text-message-video-skills", "3a800e1", "textmsg", True),
    (I + "youtube-video-skills", "f3df381", "youtube", True), (I + "ecommerce-video-skills", "2bd0dd1", "ecom", True),
    (I + "ad-video-skills", "0de0f2a", "ad", True), (I + "data-animation-skills", "8ce2709", "data", True),
    (I + "explainer-video-skills", "3e2d411", "explainer", True), (I + "map-animation-skills", "390ca98", "map", True),
    (I + "web-animation-skills", "b6dba3e", "web", True), (I + "motion-design-skills", "3c129f7", "md", True),
    (I + "kinetic-typography-skills", "fccc94b", "kt", True), (I + "freelance-motion-skills", "d85c2b4", "freelance", True),
    (I + "webgl-animation-skills", "50697d6", "webgl", True), (I + "manim-skills", "a15833c", "manim", True),
    (I + "generative-illustration-skills", "e7d6243", "genillus", False),
    (I + "javascript-animation-skills", "f7d0882", "jsanim", True), (I + "lower-thirds-skills", "aa8ef7e", "lt", True),
    (I + "b-roll-skills", "a51e34b", "broll", True), (I + "talking-head-skills", "a315032", "th", True),
    # Nov 2026 batch (all MIT; read for hooks / settings / prompt-steering before pinning). earshot itself comes from tools/setup_sfx.sh.
    ("alchaincyf/huashu-motion", "52467f9", "huashu", True), ("rossark0/rossark-motion-skill", "9b20964", "rossark", True),
    ("talsiach/take-one", "830621c", "takeone", True), ("NiazMorshed2007/reanimate", "3f7a55a", "reanimate", True),
    ("shreyaskarnik/argo", "5f71549", "argo", True), ("vincentsch/explainroo", "e95232c", "explainroo", True),
    ("win4r/video-director", "4747e5c", "vdir", True),
    # Nov 2026: stickman storyboard/prompt director + narrated "Autopilot" videos (MIT). Its Autopilot/A6 modes call the paid Gemini API.
    ("kaomei/stickman-video-director", "eb4bb37", "stickman", True),
    # Nov 13 2026 batch (user's list for split-screen / overlay / caption editing). All MIT (Rajbharti06 states MIT in its README).
    ("Rajbharti06/Ultimate-Video-Editing-Skills", "7d0af0d", "uve", True), ("riecodes/free247editor", "421f8b5", "f247", True),
    ("cth9191/animate", "7e5eb56", "cth", True), ("codie1982/chorono-editor", "7305ba8", "chorono", True),
    # HyperFrames' core skills were installed earlier; only pick the ones this repo doesn't have yet (captions, motion doctrine, seams...).
    ("heygen-com/hyperframes", "d208281", "hf", True, {"captions-overlay", "motion-doctrine", "seam-craft", "cut-the-curve",
        "oversized-cursor", "changelog-video", "style-sampling", "reverse-any-video"}),
    # Nov 16 2026 batch (user's list: core editing, motion graphics, shot design, automatic editing). Each was read for hooks,
    # paid APIs and prompt-steering first. The 6th field is a sparse checkout: only those paths are fetched (disk is tight).
    # Not installed (reasons in docs/skills-knowledge-base.md): the video-shotcraft forks (digitalpublisher, SunCl8, JohnChow90,
    # simpletibr), remotion-dev/remotion (maintainer-only skills), AutoMontage-Agent (needs its own Remotion engine), editor apps.
    ("kajisho5/ffmpeg-skill", "f1c97cb", "kffmpeg", True, {"ffmpeg-skill"}, {"sparse": ["/SKILL.md", "/scripts/", "/references/", "/LICENSE"]}),
    ("kajisho5/remotion-ffmpeg-skill", "e34a10d", "rffmpeg", True, None, {"sparse": ["/*", "!/.github/", "!/assets/"]}),
    ("Vincentwei1021/video-shotcraft", "253ae59", "shotcraft", True, None, {"sparse": ["/*", "!/.github/", "!/gallery/", "!/demos/_legacy/",
        "!/assets/readme/", "!/assets/audio/bgm/", "!/assets/wechat-sponsor.jpg", "!/README_*.md", "!/videos/"]}),   # bgm: Mixkit tracks, not ours to ship
    ("mattypark/Motion-graphics-skill", "5db5896", "mattypark", False, None, {"sparse": ["/skills/"]}),
    ("vibegameengine/video-motion-craft", "c17ab30", "vmc", True, None, {"sparse": ["/*"]}),
    ("sunithvs/video-agent-skill", "6ccc8f2", "sunith", True, None, {"sparse": ["/plugins/", "/LICENSE"]}),
    ("JhontyBarreto/video-editing-skill", "c6f1c43", "jhonty", False, None, {"sparse": ["/video-editing/"]}),
    ("kmilo93sd/agent-video-editor", "8e32c0a", "kmilo", True, None, {"sparse": ["/skills/", "/LICENSE"]}),   # its audio library is CC0
    ("brookejlacey/boring-tools", "fa77504", "boring", True, None, {"sparse": ["/*"]}),
    ("KirttiVushan/claude-code", "b489309", "ecc", True, {"video-editing"}, {"sparse": ["/skills/video-editing/", "/LICENSE"]}),
    ("Sunwood-ai-labs/hyperframes-motion-reel-skill", "be78681", "sunwood", True, None, {"sparse": ["/*"]}),
    ("bestagentkits/motion-video-skill", "a73702b", "bak", True, None, {"sparse": ["/skills/", "/LICENSE"]}),
    ("unclejobs-ai/motion-video-skill", "5fe3cca", "uj", True, None, {"sparse": ["/skills/", "/LICENSE", "/NOTICE.md"]}),
    ("10291124jcjc-dotcom/motion-reel", "be8912b", "jc", True, None, {"sparse": ["/*", "!/docs/"]}),
    ("dev-isaacmello/extreme-motion-design", "5ae5883", "emd", True, None, {"sparse": ["/skills/", "/LICENSE"]}),
    ("adunext/adu-motion-video", "4ae737a", "adu", True, None, {"sparse": ["/*", "!/assets/demos/", "!/assets/tutorials/", "!/assets/cover.*"]}),
    ("av/remotion-bits", "de35fda", "rbits", True, {"remotion-bits"}, {"sparse": ["/skills/", "/LICENSE*", "/package.json"]}),   # MIT per package.json
    ("BayramAnnakov/remotion-video-director", "c16a3a0", "bayram", True, None, {"sparse": ["/*", "!/promo.*"]}),   # MIT per README
    ("Aaryan-Kapoor/video-production-skill", "662738c", "aaryan", True, None, {"sparse": ["/skills/", "/LICENSE"]}),
    ("arthurkatcher/explainer-video", "833c20e", "arthur", False, None, {"sparse": ["/*"]}),
    ("WyattBlue/auto-editor", "1c16002", "ae", True, None, {"sparse": ["/skills/", "/LICENSE"]}),   # Unlicense; CLI: pip install auto-editor
    ("ZiadAbdelkarim/beat-synced-edit", "48c09c9", "ziad", True, None, {"sparse": ["/.claude/", "/*.py", "/requirements.txt", "/LICENSE"],
        "with_root": ["beat_map.py", "clip_tag.py", "plan_edit.py", "render_edit.py", "flash_montage.py", "overunder_stack.py",
                      "vertical_style.py", "requirements.txt", "LICENSE"],
        "note": "The pipeline scripts (beat_map.py, clip_tag.py, plan_edit.py, render_edit.py, flash_montage.py, overunder_stack.py, "
                "vertical_style.py) sit in this skill's folder: run them as `python3 .claude/skills/{name}/<script>.py`."}),
]
REFERENCE_ONLY = [("Dakkshin/after-effects-mcp", "88d5fbf"), ("Arman-Luthra/aftr", "628397d"), ("davidcervinka/vibe-editing", "8faca77"),
                  ("lanayepifanova/Claude-Editor", "b9a2e27"), ("iart-ai/motion-skills", "238dfc5")]
GENERIC = {"editor", "ffmpeg", "remotion", "sound-design", "frontend-design", "video-edit", "elevenlabs"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

def local_dir(src, repo):
    owner, name = repo.split("/")
    return os.path.join(src, "iart", name) if owner == "iart-ai" and name != "motion-skills" else os.path.join(src, f"{owner}_{name}")

def ensure_clone(repo, commit, dest, sparse=None):
    """Clone at a pinned commit. With `sparse` (gitignore-style patterns), only those paths are fetched and checked out."""
    if not os.path.isdir(os.path.join(dest, ".git")):
        extra = ["--filter=blob:none", "--no-checkout"] if sparse else []
        subprocess.run(["git", "clone", "-q", *extra, "https://github.com/" + repo + ".git", dest], check=True)
    if sparse: subprocess.run(["git", "-C", dest, "sparse-checkout", "set", "--no-cone", *sparse], check=True)
    subprocess.run(["git", "-C", dest, "checkout", "-q", commit], check=True)

def skill_dirs(repo_dir):
    for d, subs, files in os.walk(repo_dir):
        subs[:] = [s for s in subs if s not in SKIP_DIRS]
        if "SKILL.md" in files: yield d

def name_of(skill_md):
    m = re.search(r"^name:\s*['\"]?([^'\"\n]+)", open(skill_md, encoding="utf-8").read(), re.M)
    return m.group(1).strip() if m else os.path.basename(os.path.dirname(skill_md))

def main():
    src = sys.argv[sys.argv.index("--src") + 1] if "--src" in sys.argv else None
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    found = []  # (repo, prefix, licensed, skill dir, original name, options, repo dir)
    for repo, commit, prefix, licensed, *rest in REPOS:
        if only and repo not in only: continue
        pick = rest[0] if rest else None; opts = rest[1] if len(rest) > 1 else {}
        d = local_dir(src, repo) if src else os.path.join(CLONES, repo.replace("/", "_"))
        if not src: ensure_clone(repo, commit, d, opts.get("sparse"))
        seen = set()  # a repo may ship the same skill twice (.claude/ and .agents/): keep the first
        for sd in sorted(skill_dirs(d)):
            n = name_of(os.path.join(sd, "SKILL.md"))
            if n in seen or (pick and n not in pick): continue
            seen.add(n); found.append((repo, prefix, licensed, sd, n, opts, d))
    if not src and not only:
        for repo, commit in REFERENCE_ONLY: ensure_clone(repo, commit, os.path.join(CLONES, repo.replace("/", "_")))
    mpath = os.path.join(ROOT, "tools", "skill-repos.json")  # what an earlier run installed is not "ours"
    prev_m = json.load(open(mpath)) if os.path.exists(mpath) else []
    prev = {m["skill"] for m in prev_m}
    ours = {n for n in os.listdir(SKILLS)} - prev  # skills that were here before this installer
    counts = {}
    for f in found: counts[f[4]] = counts.get(f[4], 0) + 1
    manifest = [m for m in prev_m if m["from"] not in only] if only else []
    ignored = [f".claude/skills/{m['skill']}/" for m in manifest if not m["licensed"]]
    taken = ours | {m["skill"] for m in manifest}  # with --only, the other repos' installed skills are taken too
    for repo, prefix, licensed, sdir, name, opts, rdir in found:
        final = f"{prefix}-{name}" if (name in taken or counts[name] > 1 or name in GENERIC) else name
        dest = os.path.join(SKILLS, final)
        if os.path.exists(dest): shutil.rmtree(dest)
        shutil.copytree(sdir, dest, ignore=shutil.ignore_patterns(*SKIP_DIRS))
        for f in opts.get("with_root", []):  # repo-level scripts the skill calls
            if not os.path.exists(os.path.join(dest, f)): shutil.copy2(os.path.join(rdir, f), os.path.join(dest, f))
        p = os.path.join(dest, "SKILL.md"); t = open(p, encoding="utf-8").read()
        if final != name:  # keep frontmatter name and folder in step
            t = re.sub(r"^(name:\s*['\"]?)[^'\"\n]+", lambda m: m.group(1) + final, t, count=1, flags=re.M)
        if opts.get("note"):  # one line after the frontmatter, e.g. where the scripts now live
            t = re.sub(r"\A(---\n.*?\n---\n)", lambda m: m.group(1) + "\n> Installed here: " + opts["note"].format(name=final) + "\n", t, count=1, flags=re.S)
        open(p, "w", encoding="utf-8").write(t)
        manifest.append({"skill": final, "from": repo, "original_name": name, "licensed": licensed})
        if not licensed: ignored.append(f".claude/skills/{final}/")
    json.dump(manifest, open(os.path.join(ROOT, "tools", "skill-repos.json"), "w"), indent=1)
    gi = os.path.join(ROOT, ".gitignore"); text = open(gi).read()
    block = "# Skills from repos without a licence: used locally, not re-published (python3 tools/install_skill_repos.py)\n" + "\n".join(sorted(ignored)) + "\n"
    text = re.sub(r"# Skills from repos without a licence:.*?\n(?:\.claude/skills/[^\n]+\n)*", "", text, flags=re.S)
    open(gi, "w").write(text.rstrip("\n") + "\n\n" + block)
    print(f"manifest: {len(manifest)} skills ({sum(not m['licensed'] for m in manifest)} unlicensed, git-ignored); "
          f"renamed: {', '.join(m['original_name'] + '→' + m['skill'] for m in manifest if m['skill'] != m['original_name'])}")

if __name__ == "__main__": main()
