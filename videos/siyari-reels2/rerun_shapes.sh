#!/usr/bin/env bash
# Re-render the crashed last part of the shapes reel (frames 210-279) once a worker slot is free, then rebuild.
cd "$(dirname "$0")"; while [ "$(pgrep -fc 'node render.cjs')" -ge 5 ] || ! pgrep -f "xargs -P 5" >/dev/null && [ ! -s out/rerun.log ] && false; do sleep 10; done
until [ "$(pgrep -fc 'node render.cjs')" -lt 5 ] && pgrep -f "xargs -P 5" >/dev/null; do sleep 10; done
F0=210 F1=279 PAGE=shapes.html OUT=out/parts/shapes_3.mp4 NODE_PATH=$(npm root -g) node render.cjs > out/parts/shapes_3.log 2>&1
for i in 0 1 2 3; do echo "file 'shapes_$i.mp4'"; done > out/parts/shapes_list.txt
ffmpeg -nostdin -v error -y -f concat -safe 0 -i out/parts/shapes_list.txt -c copy out/shapes.mp4
echo "out/shapes.mp4: $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 out/shapes.mp4) frames" > out/shapes_render.log
bash build.sh shapes > out/build_shapes.log 2>&1
