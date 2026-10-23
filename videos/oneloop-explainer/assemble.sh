#!/usr/bin/env bash
# 180 fps sub-frames → 3-frame tmix motion blur → 60 fps master; soundtrack mastered to −14 LUFS; share copy for phones.
set -euo pipefail
cd "$(dirname "$0")"
NAME=OneLoop_Explainer_1080x1920_60fps
ffmpeg -nostdin -v error -y -framerate 180 -i out/sub/s_%05d.png \
  -vf "tmix=frames=3:weights='1 1 1',select='eq(mod(n\,3)\,2)',setpts=N/(60*TB)" -r 60 \
  -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart out/video.mp4
I=$(ffmpeg -nostdin -hide_banner -i out/audio_raw.wav -af ebur128 -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/I:/{print $2; exit}')
G=$(python3 -c "print(f'{-14.0-($I)+0.9:.2f}')")
ffmpeg -nostdin -v error -y -i out/audio_raw.wav -af "volume=${G}dB,alimiter=limit=0.85:attack=2:release=40:level=false" -ar 48000 -c:a pcm_s24le out/audio.wav
# master: high-bitrate 60 fps; share copy: 30 fps-safe bitrate for WhatsApp/Instagram uploads
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart out/${NAME}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/${NAME}_MASTER.mp4 -c:v libx264 -preset slow -b:v 14M -maxrate 18M -bufsize 28M -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart out/${NAME}_share.mp4
for f in out/${NAME}_MASTER.mp4 out/${NAME}_share.mp4; do
  ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,r_frame_rate,width,height:format=duration,bit_rate -of csv=p=0 "$f"
done
ffmpeg -nostdin -hide_banner -i out/${NAME}_MASTER.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
