#!/bin/bash
# Cuts the EDL from the camera originals (shot sideways, so transpose=2 turns them upright), joins them
# frame-exact at 60 fps, lays the caption overlay on top and writes the master and share copies.
# No music or SFX: the user adds the song in Instagram's editor. A silent audio track is included for compatibility.
set -euo pipefail
cd "$(dirname "$0")"
SRC=${SRC:-/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/ol/drive}
mkdir -p out/seg
node render_overlay.mjs
i=0; list=out/seg/list.txt; : > $list
grep -v '^#' edl.txt | while read -r clip in dur _; do
  [ -z "$clip" ] && continue
  n=$(printf "%02d" $i); frames=$(awk -v d=$dur 'BEGIN{printf "%d", d*60+0.5}')
  ffmpeg -nostdin -v error -y -ss "$in" -i "$SRC/$clip.mp4" -an \
    -vf "transpose=2,fps=60,eq=contrast=1.04:saturation=1.02,format=yuv420p" -frames:v $frames \
    -c:v libx264 -preset slow -crf 8 -g 30 out/seg/$n.mp4
  echo "file '$n.mp4'" >> $list; i=$((i+1))
done
ffmpeg -v error -y -f concat -safe 0 -i $list -c copy out/base.mp4
mk() { ffmpeg -v error -y -i out/base.mp4 -loop 1 -i out/overlay.png -f lavfi -i anullsrc=r=48000:cl=stereo \
  -filter_complex "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]" -map "[v]" -map 2:a -t 10 \
  -c:v libx264 -preset slow -crf $1 -profile:v high -r 60 -c:a aac -b:a 128k -shortest -movflags +faststart "$2"; }
mk 10 out/OneLoop_NetworkReel_1080x1920_60fps_MASTER.mp4
mk 18 out/OneLoop_NetworkReel_1080x1920_60fps_share.mp4
ls -la out/*.mp4
