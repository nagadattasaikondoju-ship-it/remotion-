#!/bin/bash
# "bobbattu" dog reel: the reference's hook + the kennel shoot's cutest moments, 1080x1920 60 fps.
#   bash assemble.sh                 full build (edit -> picture -> captions -> sound -> deliverables)
#   SKIP_PICTURE=1 bash assemble.sh  sound + deliverables only (out/video.mp4 must exist)
# Sources (SRC_DIR, see edit.py): orig/MVI_*.mp4 (Sony originals from Drive), up/s1_ref.mp4 (the reference's hook, AI-upscaled),
# assets/ref_audio.wav. The footage is encoded once (out/video.mp4, CRF 8, captions included); the MASTER is that picture untouched.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=Bobbattu_KennelReel_1080x1920_60fps
python3 -I edit.py >/dev/null
DUR=$(python3 -I -c "import json;print(json.load(open('out/edit.json'))['duration'])" 2>/dev/null)
if [ -z "${SKIP_PICTURE:-}" ]; then
  node render.mjs overlay                     # captions + emoji as transparent frames (out/ov)
  /usr/bin/python3 -P base.py | tail -1      # footage + captions in one pass (out/video.mp4)
  rm -rf out/ov
fi
python3 -I sfx_cues.py
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/video.mp4 -i assets/ref_audio.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/video_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/assets/ref_audio.wav" --sfx-trim-db ${SFX_TRIM:-22}) 2>&1 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|^\s*$" | tail -3
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness)" "$W/result/critique.txt" || true
rm -f out/video_a.mov "$W/result/mix.mp4"
# with the reel's audio (the reference voice) + SFX, and SFX only (post this one with Instagram's "Use audio" on the reference reel)
ffmpeg -nostdin -v error -y -i assets/ref_audio.wav -i "$W/result/mix_sfx_track.wav" -filter_complex "[1:a]apad=whole_dur=$DUR[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
for src in "_pre.wav:mix_master" "sfxwork/result/mix_sfx_track.wav:sfx_master"; do IN=out/${src%%:*}; OUT=out/${src##*:}.wav
  J=$(ffmpeg -nostdin -hide_banner -i "$IN" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
  ffmpeg -nostdin -v error -y -i "$IN" -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad,atrim=0:$DUR" -c:a pcm_s24le "$OUT"
done
# MASTER: the picture exactly as rendered (no re-encode) + the mix
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -t $DUR -movflags +faststart out/${N}_MASTER.mp4
# share + no-song: one high-quality encode from the master picture
for q in "share mix_master" "share_SFX-only-no-song sfx_master"; do set -- $q
  ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/$2.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 14 -tune film -pix_fmt yuv420p -profile:v high \
    -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -t $DUR -movflags +faststart out/${N}_$1.mp4
done
rm -f out/_pre.wav
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
