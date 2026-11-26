#!/usr/bin/env bash
# "Chai, Gutkha and the Yellow Wall": flat 2D explainer (tobacco, stains, gum disease) for the dental clinic. 37.4 s, 1080x1920, 60 fps.
# Run after:  node tts.mjs vo/lines.tsv vo hf_beta (SPEED=1.08) + trim (README) ; python3 build_vo.py ; echo "window.TL = $(cat timeline.json);" > timeline.js
#             node render.cjs  -> out/explainer.mp4 (0 .. 33.7 s)
# This script: end card on the last frame (33.7-37.4 s) -> picture -> voice polish -> SFX through the house pipeline (real-sfx from_cues + mix
# + critique; no music under animation, per the sound playbook) -> two-pass loudnorm -14 LUFS / -1.5 dBTP -> MASTER + share.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=DentalClinic_ChaiGutkaYellowWall_GumHealth_Explainer; FPS=60; TEND=33.7; CARD=3.7; DUR=37.4
ffmpeg -nostdin -v error -y -sseof -0.03 -i out/explainer.mp4 -frames:v 1 -update 1 endcard/out/last_frame.png
(cd endcard && FPS=$FPS CARD_DUR=$CARD NODE_PATH=$(npm root -g) node render.cjs | tail -1)
ffmpeg -nostdin -v error -y -i out/explainer.mp4 -i endcard/out/card.mp4 -filter_complex "[0:v]trim=0:$TEND,setpts=PTS-STARTPTS[a];[a][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 10 -tune animation -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture.mp4
# voice: rumble cut, a little presence, gentle compression so it sits on top of every sound
ffmpeg -nostdin -v error -y -i vo/voice.wav -af "aresample=48000,highpass=f=80,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,apad,atrim=0:$DUR" \
  -ac 2 -c:a pcm_f32le out/voice_v.wav
python3 - <<'EOF'
import json, re
L = json.load(open("timeline.json"))["lines"]
def wt(li, w, nth=0):
    n = 0
    for x in L[li - 1]["words"]:
        if re.sub(r"[^a-z']", "", x["w"].lower()).startswith(w):
            if n == nth: return x["s"]
            n += 1
    return L[li - 1]["start"]
ls = lambda li: L[li - 1]["start"]
TE = 33.7
C = [(wt(1, "year") + .1, "tick", .35, "the year counter lands on 2025"),
     (wt(2, "gums") + .05, "pop", .3, "gums pulling back"),
     (wt(3, "chai") - .05, "pop", .35, "chai icon"), (wt(3, "cigarette") - .05, "pop", .35, "cigarette icon"), (wt(3, "gutka") - .05, "pop", .35, "gutka icon"),
     (ls(4) - .15, "swipe", .35, "the daughter's drawing"),
     (wt(5, "worse") + .4, "whoosh", .45, "dive into the gums (iris)"),
     (ls(6) + .05, "pop", .35, "TARTAR label"), (wt(6, "germs") + .05, "squish", .4, "germs appear"),
     (wt(7, "attack") + .05, "softwhoosh", .3, "gums inflame"),
     (wt(8, "bone") + .1, "crumble", .4, "bone wears away"),
     (ls(9) - .15, "swipe", .35, "cut to the clinic"),
     (wt(9, "deep") + .05, "scaler", .35, "the scaler cleans the tartar"),
     (wt(9, "stains") + .1, "sparkle", .45, "polish: the tooth shines"),
     (wt(10, "heal") + .05, "chime", .35, "gums heal"),
     (wt(10, "team") - .25, "swipe", .32, "the quit plan"),
     (wt(10, "step") + .2, "tick", .3, "streak fills"),
     (ls(11) - .15, "swipe", .35, "the new drawing"), (ls(11) + 1.0, "sparkle", .45, "white smile, hearts"),
     (TE + .02, "whoosh", .45, "clinic card pops up"), (TE + .32, "pop", .5, "the logo lands"), (TE + 1.12, "chime", .45, "BOOK AN APPOINTMENT lands")]
json.dump([{"t": round(t, 3), "type": k, "g": g, "note": n} for t, k, g, n in C], open("sfx_cues.json", "w"), indent=1)
json.dump({"pop": {"ids": [65], "role": "ui"}, "boing": {"ids": [70], "role": "misc"}, "crunch": {"ids": [67], "role": "hit"}, "zap": {"ids": [62], "role": "glitch"},
           "swipe": {"ids": [53], "role": "whoosh"}, "whoosh": {"ids": [56], "role": "whoosh"}, "softwhoosh": {"ids": [57], "role": "whoosh"},
           "tick": {"ids": [58], "role": "ui"}, "squish": {"ids": [10], "role": "misc"}, "crumble": {"ids": [67], "role": "hit"}, "scaler": {"ids": [69], "role": "misc"}, "chime": {"ids": [61], "role": "ui"}, "sparkle": {"ids": [68], "role": "chime"}}, open("sfx_map.json", "w"), indent=1)
EOF
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/voice_v.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/voice_v.wav" --sfx-trim-db ${SFX_TRIM:-0}) 2>&1 \
 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|Traceback|File \"<|ModuleNotFound|^\s*$" | tail -3
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness|masking)" "$W/result/critique.txt" || true
rm -f out/_a.mov "$W/result/mix.mp4"
ffmpeg -nostdin -v error -y -i out/voice_v.wav -i "$W/result/mix_sfx_track.wav" -filter_complex "[1:a]volume=${SFX_GAIN:-0}dB,apad=whole_dur=$DUR[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$DUR" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad,atrim=0:$DUR" -c:a pcm_s24le out/mix.wav
rm -f out/_pre.wav
O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS -movflags +faststart -t $DUR"
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix.wav $O -crf 12 -tune animation -c:a aac -b:a 320k out/${N}_1080x1920_60fps_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture.mp4 -i out/mix.wav $O -crf 18 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_1080x1920_60fps_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_1080x1920_60fps_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
