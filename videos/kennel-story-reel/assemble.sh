#!/bin/bash
# Kennel dogs story reel ("to them, you're their whole book"), 1080x1920 60 fps, 43.6 s.
#   bash assemble.sh                 picture (base.py: footage + captions in one pass) -> sound -> deliverables
#   SKIP_PICTURE=1 bash assemble.sh  sound + deliverables only
# The master's picture is out/picture.mp4 untouched (compressed once, CRF 8); the share copy is one more encode from it.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=KennelDogs_WholeBook_1080x1920_60fps
python3 -I edit.py >/dev/null
DUR=$(python3 -I -c "import json;print(json.load(open('out/edit.json'))['duration'])" 2>/dev/null)
[ -z "${SKIP_PICTURE:-}" ] && /usr/bin/python3 -P base.py | tail -1
python3 -I sfx_cues.py
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i assets/ref_audio.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/assets/ref_audio.wav" --sfx-trim-db ${SFX_TRIM:-14}) 2>&1 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|^\s*$" | tail -2
rm -f out/_a.mov "$W/result/mix.mp4"
ffmpeg -nostdin -v error -y -i assets/ref_audio.wav -i "$W/result/mix_sfx_track.wav" -filter_complex "[1:a]apad=whole_dur=$DUR[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
for src in "_pre.wav:mix_master" "sfxwork/result/mix_sfx_track.wav:sfx_master"; do IN=out/${src%%:*}; OUT=out/${src##*:}.wav
  J=$(ffmpeg -nostdin -hide_banner -i "$IN" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
  ffmpeg -nostdin -v error -y -i "$IN" -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad,atrim=0:$DUR" -c:a pcm_s24le "$OUT"
done
# MASTER: the picture exactly as rendered (no re-encode) + the mix
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -t $DUR -movflags +faststart out/${N}_MASTER.mp4
# share + no-song: one high-quality encode from the master picture
for q in "share mix_master" "share_SFX-only-no-song sfx_master"; do set -- $q
  ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/$2.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 14 -tune film -pix_fmt yuv420p -profile:v high \
    -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -t $DUR -movflags +faststart out/${N}_$1.mp4
done
rm -f out/_pre.wav
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
