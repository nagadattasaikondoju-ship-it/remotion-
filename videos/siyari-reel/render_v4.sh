#!/usr/bin/env bash
# v4: chain rebuilt from the reference's measured curve / flow / zoom; whole reel re-rendered (the sting's diamond shares the new gem env).
set -euo pipefail; cd "$(dirname "$0")"
for r in "0 108" "108 216" "216 324" "324 430" "430 536"; do set -- $r; F0=$1 F1=$2 OUT=out/v4/p$1.mp4 NODE_PATH=$(npm root -g) node render.cjs > out/v4/p$1.log 2>&1 & done; wait
N=Siyari_YourDesignMadeReal_RingChain_v4; FPS=60; DUR=8.933
ffmpeg -nostdin -v error -y -i out/v4/p0.mp4 -i out/v4/p108.mp4 -i out/v4/p216.mp4 -i out/v4/p324.mp4 -i out/v4/p430.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v]concat=n=5:v=1:a=0,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 10 -tune animation -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture_v4.mp4
O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS -movflags +faststart -t $DUR"
ffmpeg -nostdin -v error -y -i out/picture_v4.mp4 -i out/music_v2.wav $O -crf 12 -tune animation -c:a aac -b:a 320k out/${N}_1080x1920_60fps_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture_v4.mp4 -i out/music_v2.wav $O -crf 18 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_1080x1920_60fps_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames:format=duration,size -of csv=p=0 "$f" | tr '\n' ' ')"; done
