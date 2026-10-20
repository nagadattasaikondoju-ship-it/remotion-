#!/usr/bin/env bash
# 180 fps sub-frames → 3-frame tmix motion blur → 60 fps, then master the soundtrack and mux.
set -euo pipefail
cd "$(dirname "$0")"
# VERT=1 ./assemble.sh → the 1080×1920 Reels cut from out/vertical/sub (same soundtrack)
if [ "${VERT:-0}" = "1" ]; then D=out/vertical; NAME=OneLoop_OneStroke_Reel_1080x1920_60fps.mp4; else D=out; NAME=OneLoop_OneStroke_Showreel_1920x1080_60fps.mp4; fi
ffmpeg -nostdin -v error -y -framerate 180 -i $D/sub/s_%05d.png \
  -vf "tmix=frames=3:weights='1 1 1',select='eq(mod(n\,3)\,2)',setpts=N/(60*TB)" -r 60 \
  -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -movflags +faststart $D/video.mp4
I=$(ffmpeg -nostdin -hide_banner -i out/audio_raw.wav -af ebur128 -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/I:/{print $2; exit}')
G=$(python3 -c "print(f'{-14.0-($I)+0.9:.2f}')")
ffmpeg -nostdin -v error -y -i out/audio_raw.wav -af "volume=${G}dB,alimiter=limit=0.85:attack=2:release=40:level=false" -ar 48000 -c:a pcm_s24le out/audio.wav
ffmpeg -nostdin -v error -y -i $D/video.mp4 -i out/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart \
  $D/$NAME
ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,r_frame_rate,width,height -of csv=p=0 $D/$NAME
ffmpeg -nostdin -hide_banner -i $D/$NAME -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
