#!/usr/bin/env bash
# Sound tools for the SFX skills (.claude/skills/real-sfx, earshot, real-sound).
# Installs the earshot package (MIT, github.com/Leonxlnx/earshot) at the reviewed commit into tools/earshot.
# Run once per fresh container:  bash tools/setup_sfx.sh
set -euo pipefail
cd "$(dirname "$0")"
REV=591fa3e
if [ ! -d earshot/.git ]; then git clone https://github.com/Leonxlnx/earshot.git earshot; fi
git -C earshot fetch -q origin && git -C earshot checkout -q "$REV"
pip install -q --break-system-packages -e "./earshot[mcp]"
(cd / && earshot doctor) || true   # run from / so the checkout folder does not shadow the package
