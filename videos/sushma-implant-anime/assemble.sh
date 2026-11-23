#!/usr/bin/env bash
# Split-screen awareness reel for Dr. Sri Sushma (missing tooth -> dental implant), 34.5 s, 1080x1920, 30 fps.
# Top: the speaker clip from the user's reference reel (KBC footage, user's call 23 Nov: general awareness), cropped to its top
# panel; from 29.3 s it punches in 1.29x from the top so the original sponsor's banner (another dental chain) is out of frame;
# AI-upscaled with tools/upscale_realesr.py (TOP=1080x596). Bottom: implant.html, an anime story built from scratch and timed
# to his words. 31.5 s -> Dr. Sri Sushma's details card (3 s, endcard/). Sound: his voice (cleaned), plus real recordings
# placed through the house pipeline (real-sfx from_cues + mix -> critique), two-pass loudnorm -14 LUFS / TP -1.5.
#   REF=<reference.mp4> TOP=<top_up.mp4> bash assemble.sh        (node render.cjs first -> out/anime.mp4)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
REF=${REF:?reference reel}; TOP=${TOP:?upscaled top panel}
N=DrSriSushma_MissingToothImplant_SplitAnime; TEND=31.5; CARD=3.0; DUR=$(python3 -c "print($TEND+$CARD)" 2>/dev/null)
ffmpeg -nostdin -v error -y -i out/anime.mp4 -i "$TOP" -filter_complex "[1:v]trim=0:$TEND,setpts=PTS-STARTPTS[t];[0:v][t]overlay=0:0:shortest=1,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset medium -crf 10 -r 30 out/split.mp4
ffmpeg -nostdin -v error -y -sseof -0.04 -i out/split.mp4 -frames:v 1 -update 1 endcard/out/last_frame.png
(cd endcard && CARD_DUR=$CARD NODE_PATH=$(npm root -g) node render.cjs | tail -1)
ffmpeg -nostdin -v error -y -i out/split.mp4 -i endcard/out/card.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 10 -tune film -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 out/picture.mp4
# his voice: rumble cut, a little presence, gentle compression; fades out as the card arrives
ffmpeg -nostdin -v error -y -i "$REF" -af "atrim=0:$TEND,asetpts=PTS-STARTPTS,aresample=48000,highpass=f=75,equalizer=f=250:t=q:w=1:g=-1.5,equalizer=f=3200:t=q:w=1.2:g=2,acompressor=threshold=-22dB:ratio=2.5:attack=10:release=150:makeup=2,afade=t=out:st=$(python3 -c "print($TEND-.15)" 2>/dev/null):d=0.15,apad,atrim=0:$DUR" -ac 2 -c:a pcm_f32le out/voice.wav
python3 - <<'EOF'
import json
C = [(2.28, "crack", .5, "the tooth cracks (impact frames)"), (2.36, "whoosh", .45, "the tooth flies out"), (4.25, "pop", .45, "MISSING TOOTH"),
     (7.53, "swipe", .45, "cut to the face"), (9.72, "tick", .5, "the clock appears"), (11.95, "pop", .45, "FACE SHAPE CHANGES"),
     (13.62, "swipe", .45, "cut to the jawbone"), (14.35, "pop", .45, "BONE LOSS"), (17.45, "whoosh", .4, "a late implant drops in"),
     (19.8, "boing", .5, "it wobbles out: red X, HARDER TO FIX"), (21.68, "rewind", .5, "rewind: do it on time"),
     (22.45, "scaler", .35, "the implant spins into the bone"), (25.4, "click", .5, "the abutment clicks on"), (26.8, "sparkle", .5, "the new tooth lands"),
     (27.25, "pop", .45, "ON TIME!"), (29.28, "swipe", .45, "cut to the calendar"), (29.35, "pop", .45, "DON'T DELAY!"), (30.1, "coin", .55, "coins: delay costs more"),
     (31.56, "whoosh", .5, "Dr. Sri Sushma's card pops up"), (31.86, "pop", .55, "the logo lands"), (32.67, "chime", .5, "BOOK AN APPOINTMENT lands")]
json.dump([{"t": t, "type": k, "g": g, "note": n} for t, k, g, n in C], open("sfx_cues.json", "w"), indent=1)
json.dump({"crack": {"ids": [67], "role": "hit"}, "whoosh": {"ids": [56], "role": "whoosh"}, "pop": {"ids": [65], "role": "ui"}, "swipe": {"ids": [53], "role": "whoosh"},
           "tick": {"ids": [0], "role": "misc"}, "boing": {"ids": [70], "role": "misc"}, "rewind": {"ids": [52], "role": "whoosh"}, "scaler": {"ids": [69], "role": "misc"},
           "click": {"ids": [38], "role": "click"}, "sparkle": {"ids": [68], "role": "chime"}, "coin": {"ids": [71], "role": "misc"}, "chime": {"ids": [61], "role": "ui"}},
          open("sfx_map.json", "w"), indent=1)
EOF
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/voice.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/voice.wav" --sfx-trim-db ${SFX_TRIM:-0}) 2>&1 \
 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|Traceback|File \"<|ModuleNotFound|^\s*$" | tail -3
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness)" "$W/result/critique.txt" || true
rm -f out/_a.mov "$W/result/mix.mp4"
ffmpeg -nostdin -v error -y -i out/voice.wav -i "$W/result/mix_sfx_track.wav" -filter_complex "[1:a]apad=whole_dur=$DUR[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad,atrim=0:$DUR" -c:a pcm_s24le out/mix.wav
rm -f out/_pre.wav
O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -movflags +faststart -t $DUR"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix.wav $O -crf 10 -tune film -c:a aac -b:a 320k out/${N}_1080x1920_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix.wav $O -crf 17 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_1080x1920_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_1080x1920_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
