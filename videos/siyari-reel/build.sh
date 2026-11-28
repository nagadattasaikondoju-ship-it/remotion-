#!/usr/bin/env bash
# Siyari "your design, made real" reel. 16 s, 1080x1920, 60 fps. Picture: reel.html (3D ring chain + logo sting), rendered by render_parallel.sh.
# Sound: real recordings through the house pipeline (real-sfx from_cues + mix -> critique), SFX only (animation gets no music bed),
# mastered to -16 LUFS / -1.5 dBTP.   bash render_parallel.sh && bash build.sh
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=Siyari_YourDesignMadeReal_RingChain; FPS=60; DUR=16.0
ffmpeg -nostdin -v error -y -i out/reel.mp4 -vf "format=yuv420p" -c:v libx264 -preset slow -crf 10 -tune animation -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture.mp4
ffmpeg -nostdin -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t $DUR -c:a pcm_f32le out/silence.wav
python3 sfx_plan.py
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/silence.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/silence.wav" --sfx-trim-db ${SFX_TRIM:-0}) 2>&1 \
 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|Traceback|File \"<|ModuleNotFound|^\s*$" | tail -3
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|headroom|loudness)" "$W/result/critique.txt" || true
rm -f out/_a.mov "$W/result/mix.mp4"
ffmpeg -nostdin -v error -y -i "$W/result/mix_sfx_track.wav" -af "aresample=48000,apad,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad,atrim=0:$DUR" -c:a pcm_s24le out/mix.wav
rm -f out/_pre.wav out/silence.wav
O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS -movflags +faststart -t $DUR"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix.wav $O -crf 12 -tune animation -c:a aac -b:a 320k out/${N}_1080x1920_60fps_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix.wav $O -crf 18 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_1080x1920_60fps_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_1080x1920_60fps_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
