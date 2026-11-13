#!/usr/bin/env bash
# One Loop "How we scale brands to 7 figures": the reference's PiP grid reel rebuilt for One Loop.
# 7.5 s loop, 1080×1920, 60 fps. Tiles pop on the song's 0.6 s grid (1.4 … 4.4 s); all six labels land at 5.0 s.
set -euo pipefail
cd "$(dirname "$0")"
U=/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e
BASE="${BASE:-$U/c3a69488-Adobe_Express_-_Adobe_Express_-_MVI_0440.mp4}"   # Prahalad, headphones on → typing
REF="${REF:-$U/eaf7a578-WhatsApp_Video_2026-10-28_at_9.03.29_PM.mp4}"     # reference reel (audio for the sync preview only)
BR=../oneloop-day-brolls/out
TILE_SRC=("$U/1b171c0e-Adobe_Express_-_MVI_0425_1.mp4" "$BR/BROLL_05_checking_emails.mp4" "$BR/BROLL_06_scrum_meet.mp4"
          "$BR/BROLL_07_heads_down_coding.mp4" "$BR/BROLL_08_bro_check_this_bug.mp4" "$BR/BROLL_09_testing_what_we_built_DRAFT-small-artifacts.mp4")
POP=(1.4 2.0 2.6 3.2 3.8 4.4); X=(169 426 691 169 426 691); Y=(440 440 440 996 996 996); DUR=7.5
mkdir -p out/tiles
# tiles: exact 228×405, half speed (60 fps sources → smooth), forward-then-reverse so every tile runs to the loop point
for i in 0 1 2 3 4 5; do
  pre="setpts=PTS-STARTPTS"; [ $i -eq 0 ] && pre="transpose=2,setpts=PTS-STARTPTS"
  sp="setpts=2*PTS"; [ $i -eq 0 ] && sp="setpts=PTS"      # the MVI_0425 clip is long enough at normal speed
  ss=0; [ $i -eq 0 ] && ss=0.25
  ffmpeg -nostdin -v error -y -ss $ss -i "${TILE_SRC[$i]}" -filter_complex \
    "[0:v]$pre,$sp,fps=60,scale=228:406:flags=lanczos,setsar=1,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0,trim=duration=6.2,setpts=PTS-STARTPTS[v]" \
    -map "[v]" -an -c:v libx264 -preset slow -crf 10 -pix_fmt yuv420p out/tiles/t$i.mp4
done
# composite
IN=(-ss 1.4 -t $DUR -i "$BASE")
for i in 0 1 2 3 4 5; do IN+=(-i out/tiles/t$i.mp4); done
for s in hook c0 c1 c2 c3 c4 c5 tiles; do IN+=(-loop 1 -framerate 60 -t $DUR -i out/text_$s.png); done
F="[0:v]transpose=2,fps=60,setpts=PTS-STARTPTS,eq=contrast=1.04:saturation=1.03[b0];"
for i in 0 1 2 3 4 5; do F+="[$((i+1)):v]setpts=PTS-STARTPTS+${POP[$i]}/TB[t$i];[b$i][t$i]overlay=${X[$i]}:${Y[$i]}:eof_action=pass:enable='gte(t,${POP[$i]})'[b$((i+1))];"; done
EN=("lt(t,1.4)" "between(t,1.4,1.9999)" "between(t,2.0,2.5999)" "between(t,2.6,3.1999)" "between(t,3.2,3.7999)" "between(t,3.8,4.3999)" "between(t,4.4,4.9999)" "gte(t,5.0)")
L=b6
for k in 0 1 2 3 4 5 6 7; do F+="[$L][$((k+7)):v]overlay=0:0:enable='${EN[$k]}'[x$k];"; L=x$k; done
F+="[$L]trim=duration=$DUR,format=yuv420p[v]"
ffmpeg -nostdin -v error -y "${IN[@]}" -filter_complex "$F" -map "[v]" -r 60 -c:v libx264 -preset slow -crf 8 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart out/video.mp4
N=OneLoop_HowWeScaleBrands_1080x1920_60fps
ffmpeg -nostdin -v error -y -i out/video.mp4 -f lavfi -t $DUR -i anullsrc=r=48000:cl=stereo -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/${N}_MASTER.mp4 -c:v libx264 -preset slow -crf 17 -maxrate 14M -bufsize 28M -pix_fmt yuv420p -c:a copy -movflags +faststart out/${N}_share.mp4
ffmpeg -nostdin -v error -y -i out/video.mp4 -t $DUR -i "$REF" -map 0:v -map 1:a -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -c:a aac -b:a 256k \
  -af "afade=t=out:st=7.42:d=0.08" -shortest -movflags +faststart out/${N}_PREVIEW-with-reference-audio.mp4
for f in out/${N}_*.mp4; do echo "$(basename $f)  $(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,r_frame_rate,width,height:format=duration -of csv=p=0 $f | tr '\n' ' ')"; done
