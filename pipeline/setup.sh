#!/usr/bin/env bash
# One-time setup: Python deps + models (~480 MB, cached in pipeline/models/).
set -euo pipefail
cd "$(dirname "$0")"
pip3 install -q -r requirements.txt
# MediaPipe's Linux wheel needs libEGL even for CPU inference.
if ! ldconfig -p 2>/dev/null | grep -q libEGL.so.1 && command -v apt-get >/dev/null; then
  apt-get install -y -q libegl1 libgles2 || (apt-get update -q && apt-get install -y -q libegl1 libgles2)
fi
mkdir -p models && cd models
P=sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
if [ ! -d "$P" ]; then
  curl -fL "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/$P.tar.bz2" | tar xj
fi
[ -f blaze_face_short_range.tflite ] || curl -fLo blaze_face_short_range.tflite \
  https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite
echo "models ready in $(pwd)"
