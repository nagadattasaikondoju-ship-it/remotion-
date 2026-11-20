#!/bin/bash
# "Pink in the sink": anime story reel for Dr. Sri Sushma (gum specialist). Run after:
#   node tts.mjs vo/lines.tsv vo  (+ trim, see README) ; python3 build_vo.py ; echo "window.TL = $(cat timeline.json);" > timeline.js
#   node render.cjs                      -> out/anime_4k.mp4 (2160x3840, 0..33.9 s)
#   endcard: CARD_DUR=5.6 CARD_4K=1 node render.cjs (backdrop = the last anime frame)
# This script: picture (4K) -> voice polish -> SFX through the house pipeline (real-sfx from_cues + mix + critique) ->
# -14 LUFS -> 4K master, 1080x1920 MASTER and share copy.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=DrSriSushma_PinkInTheSink_Anime; FPS=30; DUR=39.5
[ -f out/picture_4k.mp4 ] || ffmpeg -nostdin -v error -y -i out/anime_4k.mp4 -i endcard/out/card.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 12 -tune animation -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture_4k.mp4
[ -f out/picture_hd.mp4 ] || ffmpeg -nostdin -v error -y -i out/picture_4k.mp4 -vf "scale=1080:1920:flags=lanczos" -c:v libx264 -preset medium -crf 14 -tune animation -r $FPS out/picture_hd.mp4
# voice: rumble cut, gentle presence lift and compression so it sits on top of every sound
ffmpeg -nostdin -v error -y -i vo/voice.wav -af "highpass=f=80,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,apad,atrim=0:$DUR" \
  -ac 2 -c:a pcm_f32le out/voice_v.wav
python3 sfx_cues.py
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/picture_hd.mp4 -i out/voice_v.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/voice_v.wav" --sfx-trim-db ${SFX_TRIM:-3}) 2>&1 \
 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|Traceback|File \"<|ModuleNotFound|^\s*$" | tail -4
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness|masking)" "$W/result/critique.txt" || true
rm -f out/_a.mov "$W/result/mix.mp4"
ffmpeg -nostdin -v error -y -i out/voice_v.wav -i "$W/result/mix_sfx_track.wav" -filter_complex "[1:a]apad=whole_dur=$DUR[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad,atrim=0:$DUR" -c:a pcm_s24le out/mix.wav
rm -f out/_pre.wav
ffmpeg -nostdin -v error -y -i out/picture_4k.mp4 -i out/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -t $DUR -movflags +faststart out/${N}_4K_2160x3840_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture_4k.mp4 -i out/mix.wav -map 0:v -map 1:a -vf "scale=1080:1920:flags=lanczos" -c:v libx264 -preset slow -crf 12 -tune animation \
  -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 320k -t $DUR -movflags +faststart out/${N}_1080x1920_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture_4k.mp4 -i out/mix.wav -map 0:v -map 1:a -vf "scale=1080:1920:flags=lanczos" -c:v libx264 -preset slow -crf 18 -tune animation \
  -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -t $DUR -movflags +faststart out/${N}_1080x1920_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_1080x1920_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
