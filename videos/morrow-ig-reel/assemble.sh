#!/usr/bin/env bash
# Hook (Prahalad typing, 143 frames = 2.383 s, ends on the beat drop) + profile build (462 frames) → 10.08 s, 1080×1920, 60 fps.
#   MASTER / share : no music — add "DANCE…" (Slayyyter) in Instagram's editor (Use audio from the reference reel = same start point)
#   PREVIEW        : temp track lifted from the reference recording, only to check sync before posting (do not post)
set -euo pipefail
cd "$(dirname "$0")"
SRC="${SRC:-/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/1b171c0e-Adobe_Express_-_MVI_0425_1.mp4}"
REF="${REF:-/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/2324e724-WhatsApp_Video_2026-10-26_at_2.40.15_PM.mp4}"
N=Morrow_IfIHandledYourCafe_ep01_1080x1920_60fps
ffmpeg -nostdin -v error -y -ss 0.25 -i "$SRC" -i out/caption.png -framerate 60 -i out/ui/f_%05d.png -filter_complex "
  [0:v]transpose=2,eq=contrast=1.06:saturation=1.1:gamma=0.97,fps=60,trim=end_frame=143,setpts=PTS-STARTPTS,format=rgba[h];
  [h][1:v]overlay=format=auto[hc];
  [2:v]fps=60,setpts=PTS-STARTPTS,format=rgba[u];
  [hc][u]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 8 -tune film -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 60 -movflags +faststart out/video.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/video.mp4)
ffmpeg -nostdin -v error -y -i out/video.mp4 -f lavfi -t "$D" -i anullsrc=r=48000:cl=stereo -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/${N}_MASTER.mp4 -c:v libx264 -preset slow -crf 17 -maxrate 14M -bufsize 28M -pix_fmt yuv420p -c:a copy -movflags +faststart out/${N}_share.mp4
# temp track: one loop of the reference reel's audio, starting at its hook (3.70 s in the screen recording)
ffmpeg -nostdin -v error -y -i out/video.mp4 -ss 3.70 -t "$D" -i "$REF" -map 0:v -map 1:a -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -c:a aac -b:a 256k -af "afade=t=out:st=$(python3 -c "print($D-0.08)"):d=0.08" -shortest -movflags +faststart out/${N}_PREVIEW-with-reference-audio.mp4
for f in out/${N}_*.mp4; do echo "$f"; ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,r_frame_rate,width,height:format=duration,bit_rate,size -of csv=p=0 "$f"; done
