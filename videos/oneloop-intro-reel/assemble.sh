#!/usr/bin/env bash
# One Loop intro reel: 180 fps sub-frames → 3-frame tmix motion blur → 60 fps; the code score (audio.js) as the bed;
# real CC0 interface sounds (Openverse library) placed by Real SFX from sfx_cues.json, checked by its critique;
# two-pass loudnorm to −14 LUFS; master + share copy, 1080×1920 60 fps.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=OneLoop_IntroReel_TheNode_1080x1920_60fps; END=25.0
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
[ -f out/audio_raw.wav ] || { echo "run: node render.mjs audio"; exit 1; }
# ---- picture: mean of the 3 sub-frames of each output frame (frame f = sub-frames 3f..3f+2) ----
if [ -n "${REDO_VIDEO:-}" ] || [ ! -f out/video.mp4 ]; then
ffmpeg -nostdin -v error -y -framerate 180 -i out/sub/s_%05d.png \
  -vf "tmix=frames=3:weights='1 1 1',select='eq(mod(n\,3)\,2)',setpts=N/(60*TB),format=yuv420p" -r 60 \
  -c:v libx264 -preset slow -crf 10 -tune animation -profile:v high -level 5.1 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart out/video.mp4
fi
# ---- score: trimmed to the picture ----
ffmpeg -nostdin -v error -y -i out/audio_raw.wav -af "atrim=0:$END,afade=t=out:st=$(python3 -c "print($END-0.25)"):d=0.25" -ar 48000 -ac 2 -c:a pcm_s24le out/score.wav
# ---- real SFX on the cue sheet's frames ----
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/score.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/video_v.mov
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_v.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/ol_sfx.mp4" --base-audio "$HERE/out/score.wav" --sfx-trim-db -4)
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/ol_sfx_resolved_cues.json" "$W/result/ol_sfx_sfx_track.wav" > "$W/result/critique.txt") || true; head -20 "$W/result/critique.txt"
cp "$W/result/ol_sfx_sfx_track.wav" out/stems/sfx.wav; cp out/score.wav out/stems/score.wav; cp "$W/result/ol_sfx_resolved_cues.json" out/stems/ 2>/dev/null || true
ffmpeg -nostdin -v error -y -i out/score.wav -i out/stems/sfx.wav -filter_complex "amix=inputs=2:normalize=0:duration=first,atrim=0:$END" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,atrim=0:$END" -c:a pcm_s24le out/mix_master.wav
# ---- deliverables ----
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -movflags +faststart -shortest out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 17 -maxrate 20M -bufsize 40M -profile:v high -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -movflags +faststart -shortest out/${N}_share.mp4
for f in out/${N}_*.mp4; do echo "$f"; ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,width,height,r_frame_rate:format=duration,size,bit_rate -of csv=p=0 "$f"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
rm -f out/_pre.wav out/video_v.mov
