#!/usr/bin/env bash
# "We got you." pendulum reel for Dr. Sri Sushma Multispeciality Dental Clinic. 16.6 s, 1080x1920, 60 fps: the pendulum (0-12.6 s), then the
# clinic end card from the earlier reels, unchanged (endcard/, 12.6-16.6 s).
# The reference reel has no audio, so the sound is designed here: real recordings only, placed through the house pipeline
# (real-sfx from_cues + mix -> critique), no music (sound playbook: animation gets SFX only). SFX-only mix mastered to -16 LUFS / -1.5 dBTP.
#   NODE_PATH=$(npm root -g) node render.cjs   -> out/reel.mp4 (the pendulum, 0-12.6 s) ; then: bash build.sh
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=DrSriSushma_WeGotYou_Pendulum; FPS=60; TEND=12.6; CARD=4.0; DUR=16.6
ffmpeg -nostdin -v error -y -sseof -0.03 -i out/reel.mp4 -frames:v 1 -update 1 endcard/out/last_frame.png
(cd endcard && FPS=$FPS CARD_DUR=$CARD NODE_PATH=$(npm root -g) node render.cjs | tail -1)
ffmpeg -nostdin -v error -y -i out/reel.mp4 -i endcard/out/card.mp4 -filter_complex "[0:v]trim=0:$TEND,setpts=PTS-STARTPTS[a];[a][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 10 -tune animation -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture.mp4
ffmpeg -nostdin -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t $DUR -c:a pcm_f32le out/silence.wav
python3 - <<'EOF'
import json
# the swing turns at every 1.2 s (metronome ticks alternate tick / tock); then the drop, the build and the lockup
C = [(round(1.2 * k, 3), "tick" if k % 2 else "tock", .3, f"pendulum turns ({k})") for k in range(1, 10)]
C += [(12.62, "whoosh", .45, "the clinic card pops up"), (12.92, "pop", .5, "the logo lands"), (13.72, "chime", .45, "BOOK AN APPOINTMENT lands")]
json.dump([{"t": t, "type": k, "g": g, "note": n} for t, k, g, n in sorted(C)], open("sfx_cues.json", "w"), indent=1)
json.dump({"tick": {"ids": [24], "role": "click"}, "tock": {"ids": [23], "role": "click"}, "whoosh": {"ids": [56], "role": "whoosh"},
           "pop": {"ids": [65], "role": "ui"}, "chime": {"ids": [61], "role": "ui"}}, open("sfx_map.json", "w"), indent=1)
EOF
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
