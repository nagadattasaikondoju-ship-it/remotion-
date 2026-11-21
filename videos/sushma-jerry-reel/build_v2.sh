#!/bin/bash
# v2 (16 Nov): the same Jerry loop, AI-upscaled, and a full-details end card instead of the logo-only one.
# The clinic's card (logo, name pill, "Act Early... Choose Wisely!", BOOK AN APPOINTMENT, Dr. Sri Sushma, MDS, phone,
# website, address, socials) pops up over the last cartoon frame and holds for 5 s so the number and address can be read.
#   REF  = the user's screen recording (460x774, 30 fps; one loop = frames 12..236). LOGO = out/logo.png (blue 3D logo).
#   REF=<recording.mp4> bash build_v2.sh          full build (the AI upscale takes ~4 min on CPU; reused if out/cartoon_up.mp4 exists)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
REF=${REF:?path to the reference screen recording}
N=DrSriSushma_JerryReel_v2_1080x1920_30fps
CART=181; CARD=150; FPS=30; DUR=$(python3 -I -c "print(round(($CART+$CARD)/$FPS, 4))" 2>/dev/null)
mkdir -p out
# 1) cartoon: crop the recording's side bars, undo the player's bottom darkening (1.0 -> 0.733 over rows 669..773), remove the
#    timer, losslessly at the native 436x774; then Real-ESRGAN x4 (tools/upscale_realesr.py) straight to 1080x1920.
if [ ! -f out/cartoon_up.mp4 ]; then
  G="if(gt(Y\,669)\,1-0.267*(Y-669)/104\,1)"
  ffmpeg -v error -y -i "$REF" -filter_complex "[0:v]trim=start_frame=12:end_frame=193,setpts=PTS-STARTPTS,crop=436:774:12:0,format=gbrp,
    geq=r='min(255\,r(X\,Y)/$G)':g='min(255\,g(X\,Y)/$G)':b='min(255\,b(X\,Y)/$G)',format=yuv444p,delogo=x=3:y=733:w=118:h=34,setsar=1[v]" \
    -map "[v]" -c:v libx264 -preset slow -qp 0 -pix_fmt yuv444p out/cartoon_clean.mp4
  /usr/bin/python3 -P "$REPO/tools/upscale_realesr.py" out/cartoon_clean.mp4 out/cartoon_up.mp4 --scale 4 --size 1080x1920 --crf 8
  rm -f out/cartoon_clean.mp4
fi
# 2) end card: card.html rendered frame by frame at 2x (render.cjs), over the last cartoon frame (SKIP_PICTURE=1: sound + deliverables only)
if [ -z "${SKIP_PICTURE:-}" ]; then
ffmpeg -v error -y -i out/cartoon_up.mp4 -vf "select=eq(n\,$((CART-1)))" -vsync 0 -frames:v 1 out/last_frame.png
NODE_PATH=$(npm root -g) node render.cjs | tail -1
# 3) picture: one encode of cartoon + card
ffmpeg -nostdin -v error -y -i out/cartoon_up.mp4 -i out/card.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 10 -tune animation -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture.mp4
fi
# 4) sound: the cartoon's own audio for the same loop (0.4 s + 6.03 s, a 60 ms fade at the cut), then the card's three cues
ffmpeg -nostdin -v error -y -ss 0.4 -t $(python3 -I -c "print($CART/$FPS)" 2>/dev/null) -i "$REF" -vn \
  -af "aresample=48000,afade=t=out:st=5.973:d=0.06,apad,atrim=0:$DUR" -ac 2 -c:a pcm_f32le out/base.wav
python3 -I sfx_cues.py
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/base.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/base.wav" --sfx-trim-db ${SFX_TRIM:-10}) 2>&1 \
 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|Traceback|File \"<|ModuleNotFound|^\s*$" | tail -2
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness)" "$W/result/critique.txt" || true
rm -f out/_a.mov "$W/result/mix.mp4"
ffmpeg -nostdin -v error -y -i out/base.wav -i "$W/result/mix_sfx_track.wav" -filter_complex "[1:a]apad=whole_dur=$DUR[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad,atrim=0:$DUR" -c:a pcm_s24le out/mix_master.wav
rm -f out/_pre.wav
# 5) MASTER = the picture untouched + the mix; share = one more high-quality encode
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -t $DUR -movflags +faststart out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 16 -tune animation -pix_fmt yuv420p \
  -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -t $DUR -movflags +faststart out/${N}_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size,bit_rate -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
