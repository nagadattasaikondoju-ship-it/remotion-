#!/usr/bin/env bash
# v3: re-render the snake ring chain (frames 0-353, 0-5.9 s) in 4 parts; the logo sting frames 354-535 are reused from out/v2 (unchanged code path).
set -euo pipefail; cd "$(dirname "$0")"
for r in "0 89" "89 178" "178 266" "266 354"; do set -- $r; F0=$1 F1=$2 OUT=out/v3/p$1.mp4 NODE_PATH=$(npm root -g) node render.cjs > out/v3/p$1.log 2>&1 & done; wait
N=Siyari_YourDesignMadeReal_RingChain_v3; FPS=60; DUR=8.933
ffmpeg -nostdin -v error -y -i out/v3/p0.mp4 -i out/v3/p89.mp4 -i out/v3/p178.mp4 -i out/v3/p266.mp4 -i out/v2/p354.mp4 -i out/v2/p445.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v]concat=n=6:v=1:a=0,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 10 -tune animation -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture_v3.mp4
O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS -movflags +faststart -t $DUR"
ffmpeg -nostdin -v error -y -i out/picture_v3.mp4 -i out/music_v2.wav $O -crf 12 -tune animation -c:a aac -b:a 320k out/${N}_1080x1920_60fps_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture_v3.mp4 -i out/music_v2.wav $O -crf 18 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_1080x1920_60fps_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames:format=duration,size -of csv=p=0 "$f" | tr '\n' ' ')"; done
