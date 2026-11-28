#!/usr/bin/env bash
# PAGE=earrings.html NAME=earrings FRAMES=900 bash render_parallel.sh   -> out/<NAME>.mp4  (4 parallel frame ranges, joined)
set -euo pipefail; cd "$(dirname "$0")"; mkdir -p out/parts
N=${FRAMES}; Q=$(( (N + 3) / 4 ))
for i in 0 1 2 3; do F0=$((i*Q)); F1=$(( (i+1)*Q < N ? (i+1)*Q : N )); PAGE=$PAGE F0=$F0 F1=$F1 OUT=out/parts/${NAME}_$i.mp4 NODE_PATH=$(npm root -g) node render.cjs > out/parts/${NAME}_$i.log 2>&1 & done; wait
for i in 0 1 2 3; do echo "file '${NAME}_$i.mp4'"; done > out/parts/${NAME}_list.txt
ffmpeg -nostdin -v error -y -f concat -safe 0 -i out/parts/${NAME}_list.txt -c copy out/${NAME}.mp4
echo "out/${NAME}.mp4: $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 out/${NAME}.mp4) frames"
