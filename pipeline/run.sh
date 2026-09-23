#!/usr/bin/env bash
# Stages 1-2: transcribe, build the edit-decision list, track the face.
# Usage: pipeline/run.sh <input.mp4> [name]   (name defaults to "source")
# Writes public/media/<name>.{mp4,words.json,edl.json,faces.json}.
# Manual cut overrides are read from pipeline/overrides/<name>.json if present.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IN="$1"; NAME="${2:-source}"
OUT="$ROOT/public/media"; mkdir -p "$OUT"
[ "$(realpath "$IN")" = "$(realpath -m "$OUT/$NAME.mp4")" ] || cp "$IN" "$OUT/$NAME.mp4"
cd "$ROOT"
python3 pipeline/transcribe.py "$OUT/$NAME.mp4" "$OUT/$NAME.words.json"
python3 pipeline/build_edl.py "$OUT/$NAME.mp4" "$OUT/$NAME.words.json" "$OUT/$NAME.edl.json" \
  --overrides "pipeline/overrides/$NAME.json"
python3 pipeline/detect_faces.py "$OUT/$NAME.mp4" "$OUT/$NAME.faces.json" 2> >(grep -vE '^(W0000|I0000|INFO:|WARNING: Logging)' >&2)
