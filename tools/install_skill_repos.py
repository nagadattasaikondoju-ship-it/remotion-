# Install the motion-graphics / video-editing skill repos the user collected (Oct 2026) into .claude/skills/.
#   python3 tools/install_skill_repos.py            clone (pinned commits) into tools/skill-repos/, then install
#   python3 tools/install_skill_repos.py --src DIR  install from existing clones in DIR (<owner>_<repo>, iart/<pack>)
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
    ("digitalsamba/claude-code-video-toolkit", "eddb488", "dsk", True),
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
]
REFERENCE_ONLY = [("Dakkshin/after-effects-mcp", "88d5fbf"), ("Arman-Luthra/aftr", "628397d"),
                  ("lanayepifanova/Claude-Editor", "b9a2e27"), ("iart-ai/motion-skills", "238dfc5")]
GENERIC = {"editor", "ffmpeg", "remotion", "sound-design", "frontend-design", "video-edit", "elevenlabs"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

def local_dir(src, repo):
    owner, name = repo.split("/")
    return os.path.join(src, "iart", name) if owner == "iart-ai" and name != "motion-skills" else os.path.join(src, f"{owner}_{name}")

def ensure_clone(repo, commit, dest):
    if not os.path.isdir(os.path.join(dest, ".git")):
        subprocess.run(["git", "clone", "-q", "https://github.com/" + repo + ".git", dest], check=True)
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
    found = []  # (repo, prefix, licensed, skill dir, original name)
    for repo, commit, prefix, licensed in REPOS:
        d = local_dir(src, repo) if src else os.path.join(CLONES, repo.replace("/", "_"))
        if not src: ensure_clone(repo, commit, d)
        found += [(repo, prefix, licensed, s, name_of(os.path.join(s, "SKILL.md"))) for s in skill_dirs(d)]
    if not src:
        for repo, commit in REFERENCE_ONLY: ensure_clone(repo, commit, os.path.join(CLONES, repo.replace("/", "_")))
    mpath = os.path.join(ROOT, "tools", "skill-repos.json")  # what an earlier run installed is not "ours"
    prev = {m["skill"] for m in json.load(open(mpath))} if os.path.exists(mpath) else set()
    ours = {n for n in os.listdir(SKILLS)} - prev  # skills that were here before this installer
    counts = {}
    for f in found: counts[f[4]] = counts.get(f[4], 0) + 1
    manifest, ignored = [], []
    for repo, prefix, licensed, sdir, name in found:
        final = f"{prefix}-{name}" if (name in ours or counts[name] > 1 or name in GENERIC) else name
        dest = os.path.join(SKILLS, final)
        if os.path.exists(dest): shutil.rmtree(dest)
        shutil.copytree(sdir, dest, ignore=shutil.ignore_patterns(*SKIP_DIRS))
        if final != name:  # keep frontmatter name and folder in step
            p = os.path.join(dest, "SKILL.md"); t = open(p, encoding="utf-8").read()
            open(p, "w", encoding="utf-8").write(re.sub(r"^(name:\s*['\"]?)[^'\"\n]+", lambda m: m.group(1) + final, t, count=1, flags=re.M))
        manifest.append({"skill": final, "from": repo, "original_name": name, "licensed": licensed})
        if not licensed: ignored.append(f".claude/skills/{final}/")
    json.dump(manifest, open(os.path.join(ROOT, "tools", "skill-repos.json"), "w"), indent=1)
    gi = os.path.join(ROOT, ".gitignore"); text = open(gi).read()
    block = "# Skills from repos without a licence: used locally, not re-published (python3 tools/install_skill_repos.py)\n" + "\n".join(sorted(ignored)) + "\n"
    text = re.sub(r"# Skills from repos without a licence:.*?\n(?:\.claude/skills/[^\n]+\n)*", "", text, flags=re.S)
    open(gi, "w").write(text.rstrip("\n") + "\n\n" + block)
    print(f"installed {len(manifest)} skills ({sum(not m['licensed'] for m in manifest)} unlicensed, git-ignored); "
          f"renamed: {', '.join(m['original_name'] + '→' + m['skill'] for m in manifest if m['skill'] != m['original_name'])}")

if __name__ == "__main__": main()
