#!/bin/bash
# OneLoop "We don't build demos" reel: skit + Tarun's explanation. Rendered in 4K (2160x3840, 30 fps); the HD copies are downscaled from it.
#   bash assemble.sh            full build (timeline -> picture -> overlay -> sound -> deliverables)
#   SKIP_PICTURE=1 bash assemble.sh   re-do only the sound + deliverables (out/video.mp4 must exist)
# Sources (SRC_DIR): skit.mp4, clips/t1..t9.mp4, broll_0640.mp4 (One Loop Drive B-roll), clean/*.wav (cleaned dialogue),
#   up/*.mp4 + up/offsets.json (the takes upscaled x4 with tools/upscale_realesr.py; base_render.py falls back to the originals).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
PY=/usr/bin/python3; N=OneLoop_WeDontBuildDemos
python3 -I timeline.py >/dev/null
DUR=$(python3 -I -c "import json;print(json.load(open('out/timeline.json'))['duration'])" 2>/dev/null)
if [ -z "${SKIP_PICTURE:-}" ]; then
  $PY -P base_render.py | tail -1        # picture: zooms, split, PiP, freezes (out/base.mp4, 4K)
  SC=2 node render.mjs video             # captions + motion graphics over it, drawn at 2x (out/video.mp4, 4K)
fi
# ---- sound ----
$PY -P audio_build.py                    # out/dialogue.wav + out/music.wav (composed in code)
python3 -I sfx_cues.py
# music: playful under the sketch, documentary under Tarun (~19 dB under his voice), pulse under the proofs, out for the slam,
# up for the logo / CTA hold; then ducked by the voice so every word sits on top
VOL=$(python3 -I -c "import json;m=json.load(open('out/timeline.json'))['marks'];print(f\"if(lt(t,{m['frz']}),0.42,if(lt(t,{m['t4b']}),0.52,if(lt(t,{m['t7a']}),0.55,if(lt(t,{m['t9']}),0.0,0.60))))\")" 2>/dev/null)
ffmpeg -nostdin -v error -y -i out/music.wav -i out/dialogue.wav -filter_complex \
 "[0:a]volume='$VOL':eval=frame[m];\
  [1:a]asplit=2[d1][d2];[m][d1]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=350:makeup=1[md];\
  [d2][md]amix=inputs=2:normalize=0:duration=first" -c:a pcm_s24le out/bed.wav
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/bed.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/video_v.mov
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_v.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/bed.wav" --sfx-trim-db ${SFX_TRIM:-0}) 2>&1 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|^\s*$" | tail -4
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness|hook|pacing)" "$W/result/critique.txt" || true
rm -f out/video_v.mov "$W/result/mix.mp4"   # 4K picture copies: free the disk before the deliverables
cp "$W/result/mix_sfx_track.wav" out/stems/sfx.wav; cp out/dialogue.wav out/stems/dialogue.wav; cp out/music.wav out/stems/music_raw.wav
ffmpeg -nostdin -v error -y -i out/bed.wav -i out/stems/sfx.wav -filter_complex "[1:a]apad=whole_dur=$DUR[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,atrim=0:$DUR" -c:a pcm_s24le out/mix_master.wav
# ---- deliverables ----
for q in "1080x1920_30fps_HD_MASTER 12 320k" "1080x1920_30fps_share 17 256k"; do set -- $q   # HD copies: downscaled from the 4K render
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -vf "scale=1080:1920:flags=lanczos" -c:v libx264 -preset slow -crf $2 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -profile:v high -c:a aac -b:a $3 -af apad -t $DUR -movflags +faststart out/${N}_$1.mp4
done
# 4K: 50 Mbit/s keeps the file under the 500 MB the user's app accepts (~345 MB for 61 s)
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset medium -b:v 50M -maxrate 58M -bufsize 100M -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -profile:v high -c:a aac -b:a 320k -af apad -t $DUR -movflags +faststart out/${N}_2160x3840_30fps_4K.mp4
rm -f out/video_v.mov out/_pre.wav out/sfxwork/result/mix.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size:stream=nb_frames -of csv=p=0 "$f" | tr '\n' ' ')"; done
ffmpeg -nostdin -hide_banner -i out/${N}_1080x1920_30fps_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
