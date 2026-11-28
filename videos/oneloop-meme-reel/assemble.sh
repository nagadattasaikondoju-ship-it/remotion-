#!/usr/bin/env bash
# One Loop meme reel (INTERNAL CONCEPT): reference setup 0-37.667 s + One Loop confession in Naga's cloned voice.
# Needs: out/film.mp4, out/pitch_bg.mp4 (build_picture.py), out/overlay.mov + out/tag.png (render_overlay.cjs), out/full_audio.wav (mix.py)
set -euo pipefail; cd "$(dirname "$0")"
N=OneLoop_ConfessionMeme_INTERNAL_1080x1920_30fps
ffmpeg -nostdin -v error -y -i out/film.mp4 -loop 1 -i out/tag.png -i out/pitch_bg.mp4 -i out/overlay.mov -filter_complex \
 "[0][1]overlay=shortest=1,format=yuv420p,setsar=1[a];[2][3]overlay=eof_action=pass,format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]" \
 -map "[v]" -c:v libx264 -preset slow -crf 10 -r 30 out/picture.mp4
O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -movflags +faststart -shortest"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/full_audio.wav $O -crf 12 -c:a aac -b:a 320k out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/full_audio.wav $O -crf 19 -maxrate 12M -bufsize 24M -c:a aac -b:a 256k out/${N}_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames:format=duration,size -of csv=p=0 "$f" | tr '\n' ' ')"; done
