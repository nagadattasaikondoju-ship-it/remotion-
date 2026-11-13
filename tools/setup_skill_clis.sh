#!/usr/bin/env bash
# Command-line tools for the Nov 2026 skills, built from the pinned, reviewed clones in tools/skill-repos/ (never pulled from npm):
#   om (huashu-motion) · explainroo · argo (argo-guide) · reanimate's script deps (bun). Re-run in a fresh container
#   after `python3 tools/install_skill_repos.py --only <repos>` has cloned them. Heavy models download on first use:
#   explainroo voice (`explainroo doctor --fetch`), argo's Kokoro TTS (`npm i kokoro-js@1` in the demo project).
set -euo pipefail
cd "$(dirname "$0")/skill-repos"
npm install -g --ignore-scripts --no-audit --no-fund ./alchaincyf_huashu-motion            # no dependencies
(cd vincentsch_explainroo && npm install --no-audit --no-fund)
npm install -g --ignore-scripts --no-audit --no-fund ./vincentsch_explainroo
(cd shreyaskarnik_argo && npm install --no-audit --no-fund --ignore-scripts && npm run build)
npm install -g --ignore-scripts --no-audit --no-fund ./shreyaskarnik_argo
# reanimate: script deps only; skip its setup.sh browser download, the preinstalled Chromium is used instead
(cd ../../.claude/skills/reanimate/scripts && bun install --silent)
# reanimate's Playwright 1.64 expects Chromium build 1248; point that build's paths at the preinstalled Chromium 1194
# (no second browser). Run reanimate with PLAYWRIGHT_BROWSERS_PATH=tools/pw-compat.
C=../pw-compat; mkdir -p $C/chromium_headless_shell-1248/chrome-headless-shell-linux64 $C/chromium-1248/chrome-linux64
ln -sfn /opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell $C/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell
ln -sfn /opt/pw-browsers/chromium-1194/chrome-linux/chrome $C/chromium-1248/chrome-linux64/chrome
for b in chromium_headless_shell-1248 chromium-1248; do touch $C/$b/INSTALLATION_COMPLETE $C/$b/DEPENDENCIES_VALIDATED; done
# this container's system Pillow is broken for python3.11 (video-director's qa_video.py, tools/grade.py need it)
python3 -c "import PIL.Image" 2>/dev/null || python3 -m pip install -q --user --break-system-packages --ignore-installed pillow
command -v om explainroo argo
