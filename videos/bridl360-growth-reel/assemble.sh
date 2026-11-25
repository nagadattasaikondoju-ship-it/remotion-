#!/usr/bin/env bash
# BRIDL360 version of a land-investment reel the user supplied (25 Nov 2026): the reference's picture and motion graphics are kept
# as they are; only the brand moments are replaced by brand.html (Hyderabad, the BRIDL360 tag on the arrows, the map pin with a
# BRIDL360 project, the places + "5 projects", the end card). New male VO (Kokoro hm_omega, vo/), the reference's music stem
# (Demucs no_vocals) as the bed. 49.77 s, 1080x1920, 30 fps.
#   REF_UP=<reference cropped to 420x746 and ESRGAN-upscaled to 1080x1920> BED=<no_vocals.wav> bash assemble.sh
#   (first: python3 build_vo.py; node render.cjs overlay)
# Framing fix: the screen recording has an 11 px black strip at its right edge and the player's timestamp in its bottom rows, so the
# base is cropped to 1050x1867 and scaled back to 1080x1920 (brand.html applies the same scale to the segments that sit on it).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
REF_UP=${REF_UP:?upscaled reference}; BED=${BED:?music stem}
N=BRIDL360_LandAroundGrowth; DUR=49.7667
FIXV="crop=1050:1867:0:0,scale=1080:1920:flags=lanczos,setsar=1"
ffmpeg -nostdin -v error -y -i "$REF_UP" -i out/overlay.mov -filter_complex "[0:v]$FIXV,trim=0:$DUR,setpts=PTS-STARTPTS[b];[b][1:v]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -preset slow -crf 10 -tune film -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 out/picture.mp4
# voice: raised to the reference VO's loudness (-13.8 LUFS; the bed sits ~6 LU under it as in the reference), rumble cut, a little presence
ffmpeg -nostdin -v error -y -i vo/voice.wav -af "aresample=48000,highpass=f=70,equalizer=f=3000:t=q:w=1.2:g=1.5,volume=3.5dB,apad,atrim=0:$DUR" -ac 2 -c:a pcm_f32le out/voice.wav
# bed: the reference's own hits for its logo pops (28.6-29.6 s) land off our place-name pops, so it dips 7 dB under them
ffmpeg -nostdin -v error -y -i "$BED" -af "aresample=48000,volume='if(between(t,28.15,29.95),0.45,1)':eval=frame,afade=t=out:st=49.3:d=0.45,apad,atrim=0:$DUR" -ac 2 -c:a pcm_f32le out/bed.wav
python3 - <<'EOF'
import json
T = json.load(open("vo/times.json"))
C = [(14.14, "pop", .4, "Hyderabad pops in"), (22.88, "pop", .45, "BRIDL360 tag lands on the arrows"), (26.88, "pop", .35, "BRIDL360 project in the map pin"),
     (T["tKom"] - .04, "pop", .45, "Kompally"), (T["tGac"] - .04, "pop", .45, "Gachibowli"), (T["tSad"] - .04, "pop", .45, "Sadashivpet"),
     (30.44, "swipe", .4, "places slide out, projects slide in"), (T["tFive"] + .04, "pop", .5, "5 projects"),
     (45.42, "softwhoosh", .35, "end card rises"), (46.78, "chime", .45, "DM US OR CALL NOW lands")]
json.dump([{"t": round(t, 3), "type": k, "g": g, "note": n} for t, k, g, n in C], open("sfx_cues.json", "w"), indent=1)
json.dump({"pop": {"ids": [65], "role": "ui"}, "swipe": {"ids": [53], "role": "whoosh"}, "softwhoosh": {"ids": [57], "role": "whoosh"}, "chime": {"ids": [61], "role": "ui"}},
          open("sfx_map.json", "w"), indent=1)
EOF
ffmpeg -nostdin -v error -y -i out/voice.wav -i out/bed.wav -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0:duration=first" -c:a pcm_f32le out/base.wav
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/base.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/base.wav" --sfx-trim-db ${SFX_TRIM:-3}) 2>&1 \
 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|Traceback|File \"<|ModuleNotFound|^\s*$" | tail -3
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness)" "$W/result/critique.txt" || true
rm -f out/_a.mov "$W/result/mix.mp4"
ffmpeg -nostdin -v error -y -i out/base.wav -i "$W/result/mix_sfx_track.wav" -filter_complex "[1:a]apad=whole_dur=$DUR[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad,atrim=0:$DUR" -c:a pcm_s24le out/mix.wav
rm -f out/_pre.wav out/base.wav
O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -movflags +faststart -t $DUR"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix.wav $O -crf 10 -tune film -c:a aac -b:a 320k out/${N}_1080x1920_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix.wav $O -crf 17 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_1080x1920_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_1080x1920_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
