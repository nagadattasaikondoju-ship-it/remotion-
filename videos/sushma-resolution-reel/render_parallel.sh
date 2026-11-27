#!/usr/bin/env bash
# Render reel.html in 4 parallel frame ranges (the 3D frames are the slow ones, so the split is weighted toward them) and join them.
set -euo pipefail; cd "$(dirname "$0")"; mkdir -p out/parts
B=(0 135 270 405 669)
for i in 0 1 2 3; do F0=${B[$i]} F1=${B[$((i+1))]} OUT=out/parts/p$i.mp4 NODE_PATH=$(npm root -g) node render.cjs > out/parts/p$i.log 2>&1 & done; wait
for i in 0 1 2 3; do echo "file 'p$i.mp4'"; done > out/parts/list.txt
ffmpeg -nostdin -v error -y -f concat -safe 0 -i out/parts/list.txt -c copy out/reel.mp4
echo "out/reel.mp4: $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 out/reel.mp4) frames"
