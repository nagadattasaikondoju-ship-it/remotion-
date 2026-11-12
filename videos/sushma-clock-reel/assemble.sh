#!/bin/bash
# Picture (render.mjs video) + real CC0 SFX placed by the Real SFX skill from sfx_cues.json → deliverables.
# No music: the user adds the song in Instagram. SFX sit at a modest level so a song can go on top.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=DrSriSushma_ToothClock_1080x1920_60fps; END=21.0
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
[ -f out/video.mp4 ] || node render.mjs video 60
ffmpeg -nostdin -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t $END -c:a pcm_s16le out/silence.wav
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/silence.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/video_v.mov
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_v.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/clk_sfx.mp4" --base-audio "$HERE/out/silence.wav")
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/clk_sfx_resolved_cues.json" "$W/result/clk_sfx_sfx_track.wav" > "$W/result/critique.txt") || true; sed -n 1,14p "$W/result/critique.txt"
cp "$W/result/clk_sfx_sfx_track.wav" out/stems/sfx.wav
# level: peaks to -3 dBTP, integrated around -20 LUFS so a song added in Instagram sits on top
ffmpeg -nostdin -v error -y -i out/stems/sfx.wav -af "apad=whole_dur=$END,atrim=0:$END,loudnorm=I=-20:TP=-3:LRA=15,aresample=48000" -c:a pcm_s24le out/mix_master.wav
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 10 -tune animation -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -profile:v high -c:a aac -b:a 320k -movflags +faststart -shortest out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 15 -tune animation -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -profile:v high -c:a aac -b:a 256k -movflags +faststart -shortest out/${N}_share.mp4
rm -f out/video_v.mov out/silence.wav
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size:stream=nb_frames -of csv=p=0 "$f" | tr '\n' ' ')"; done
