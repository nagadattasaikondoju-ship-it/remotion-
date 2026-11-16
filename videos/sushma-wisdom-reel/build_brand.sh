#!/bin/bash
# v2 (16 Nov, user's call): the reference reel EXACTLY as it is (picture, voice, music), only the other clinic's brand removed:
#  - picture: the AI-upscaled reference (out/base_up.mp4) frames 0-1030, then Dr. Sri Sushma's full card popping up out of the
#    white flash (endcard/: the Jerry reel's card, backdrop = frame 1030), held 5 s;
#  - sound: the original soundtrack up to 35.25 s; from there the music/SFX bed alone (Demucs stem), so the line
#    "Call Next Care Dental today" is gone; the bed is extended under the longer card; card SFX through the sound pipeline.
#   REF=<reference.mp4> STEMS=<dir with music_sfx.wav> bash build_brand.sh
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
REF=${REF:?reference video}; STEMS=${STEMS:?folder with music_sfx.wav}
N=DrSriSushma_WisdomTeeth_v2_1080x1920_30fps; KEEP=1031; FPS=30
DUR=$(python3 -c "print(round(($KEEP+150)/$FPS,4))" 2>/dev/null); CUT=34.80
ffmpeg -nostdin -v error -y -i out/base_up.mp4 -i endcard/out/card.mp4 -filter_complex \
  "[0:v]trim=end_frame=$KEEP,setpts=PTS-STARTPTS[a];[a][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 12 -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture_v2.mp4
# soundtrack: original until CUT, then the music bed; the bed's last 2 s looped once (0.5 s crossfade) and faded out under the card
ffmpeg -nostdin -v error -y -i "$REF" -i "$STEMS/music_sfx.wav" -filter_complex "
  [0:a]aresample=48000,atrim=0:$CUT,asetpts=PTS-STARTPTS[o];
  [1:a]aresample=48000,atrim=$CUT:37.9,asetpts=PTS-STARTPTS[m1];
  [1:a]aresample=48000,atrim=35.9:37.9,asetpts=PTS-STARTPTS[m2];
  [m1][m2]acrossfade=d=0.5[m];[o][m]acrossfade=d=0.04,afade=t=out:st=$(python3 -c "print($DUR-1.3)" 2>/dev/null):d=1.3,apad,atrim=0:$DUR" \
  -ac 2 -c:a pcm_f32le out/base_v2.wav
python3 - <<'EOF'
import json
C = 1031 / 30
json.dump([{"t": round(C + 0.06, 3), "type": "whoosh", "g": 0.45, "note": "the card pops up out of the white flash"},
           {"t": round(C + 0.36, 3), "type": "pop", "g": 0.5, "note": "the logo lands"},
           {"t": round(C + 1.17, 3), "type": "chime", "g": 0.45, "note": "the BOOK AN APPOINTMENT button lands"}], open("sfx_cues_v2.json", "w"), indent=1)
json.dump({"whoosh": {"ids": [56], "role": "whoosh"}, "pop": {"ids": [65], "role": "ui"}, "chime": {"ids": [61], "role": "ui"}}, open("sfx_map_v2.json", "w"), indent=1)
EOF
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/picture_v2.mp4 -i out/base_v2.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues_v2.json" --video "$HERE/out/_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map_v2.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/base_v2.wav" --sfx-trim-db ${SFX_TRIM:-2}) 2>&1 \
 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|Traceback|File \"<|ModuleNotFound|^\s*$" | tail -2
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness)" "$W/result/critique.txt" || true
rm -f out/_a.mov "$W/result/mix.mp4"
ffmpeg -nostdin -v error -y -i out/base_v2.wav -i "$W/result/mix_sfx_track.wav" -filter_complex "[1:a]apad=whole_dur=$DUR[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad,atrim=0:$DUR" -c:a pcm_s24le out/mix_v2.wav
rm -f out/_pre.wav
ffmpeg -nostdin -v error -y -i out/picture_v2.mp4 -i out/mix_v2.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -t $DUR -movflags +faststart out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture_v2.mp4 -i out/mix_v2.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -profile:v high \
  -c:a aac -b:a 256k -t $DUR -movflags +faststart out/${N}_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
