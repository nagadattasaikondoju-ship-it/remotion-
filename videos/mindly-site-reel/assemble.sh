#!/usr/bin/env bash
# One Loop ep. 04: "if i rebuilt your brand's website..." AI-slop site vs the rebuilt site (same brand, Mindly).
# hook (MVI_0706 from the One Loop B-roll Drive: typing, then hand to chin on the beat drop; 143 frames = 2.383 s)
# + screen (index.html, 60 fps, from the drop) -> 13.27 s, 1080x1920, 60 fps.
# Song: "DANCE..." as heard in ep. 03 (only copy on hand: the ep. 03 reel, whose pops sit on every 2-beat step). Extended to
# 13.27 s by repeating 6 beats [5.538, 8.724) cut just before the kicks; every pop then lands on a build/end-card event.
# Sound pipeline (Openverse library -> real-sfx from_cues + mix -> critique), two-pass loudnorm -14 LUFS / TP -1.2.
#   B=<MVI_0706.MP4> U=<ep03 reel.mp4> bash assemble.sh      (node render.cjs caption / ui first)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
B=${B:?B-roll MVI_0706}; U=${U:?ep. 03 reel with the song}
N=OneLoop_IfIRebuiltYourBrandsWebsite_ep04_1080x1920_60fps
[ -f out/caption.png ] || NODE_PATH=$(npm root -g) node render.cjs caption
[ -f out/ui.mp4 ] || NODE_PATH=$(npm root -g) node render.cjs ui
ffmpeg -nostdin -v error -y -ss 0.35 -i "$B" -i out/caption.png -filter_complex "[0:v]transpose=2,eq=contrast=1.06:saturation=1.08:gamma=0.97,fps=60,trim=end_frame=143,setpts=PTS-STARTPTS,format=rgba[h];[h][1:v]overlay=format=auto,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -preset slow -crf 8 -tune film -r 60 out/hook.mp4
ffmpeg -nostdin -v error -y -i out/hook.mp4 -i out/ui.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 8 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 60 out/video.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/video.mp4)
ffmpeg -nostdin -v error -y -i "$U" -filter_complex "[0:a]aresample=48000,atrim=0:8.724,asetpts=PTS-STARTPTS[a];[0:a]aresample=48000,atrim=5.538:8.724,asetpts=PTS-STARTPTS[b];[0:a]aresample=48000,atrim=8.724,asetpts=PTS-STARTPTS[c];[a][b]acrossfade=d=0.006:c1=tri:c2=tri[ab];[ab][c]acrossfade=d=0.006:c1=tri:c2=tri,afade=t=out:st=13.12:d=0.15,apad,atrim=0:$D[o]" \
  -map "[o]" -ac 2 -c:a pcm_s16le out/song.wav
python3 - <<'EOF'
import json
B = 60 / 113; P = lambda k: 3.442 + (k - 1) * 2 * B
json.dump([{"t": 4.0, "type": "swipe", "g": .45, "note": "the agent cursors swarm in from the edges"},
           {"t": round(P(2) + .01, 3), "type": "glitch", "g": .35, "note": "the slop is deleted (with the song's own pop)"},
           {"t": round(P(8) - .05, 3), "type": "softwhoosh", "g": .35, "note": "the browser shrinks up for the end card"}], open("sfx_cues.json", "w"), indent=1)
json.dump({"swipe": {"ids": [53], "role": "whoosh"}, "glitch": {"ids": [62], "role": "glitch"}, "softwhoosh": {"ids": [57], "role": "whoosh"}}, open("sfx_map.json", "w"), indent=1)
EOF
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/song.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/_a.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/song.wav" --sfx-trim-db ${SFX_TRIM:-8}) 2>&1 \
 | grep -v -E "distutils|_distutils_hack|frozen site|addpackage|Remainder|Traceback|File \"<|ModuleNotFound|^\s*$" | tail -3
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness)" "$W/result/critique.txt" || true
rm -f out/_a.mov "$W/result/mix.mp4"
ffmpeg -nostdin -v error -y -i out/song.wav -i "$W/result/mix_sfx_track.wav" -filter_complex "[1:a]apad=whole_dur=$D[s];[0:a][s]amix=inputs=2:normalize=0:duration=first" -c:a pcm_f32le out/mix.wav
J=$(ffmpeg -nostdin -hide_banner -i out/mix.wav -af loudnorm=I=-14:TP=-1.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/mix.wav -af "loudnorm=I=-14:TP=-1.2:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad=whole_dur=$D,atrim=0:$D" -c:a pcm_s24le out/mix_master.wav
V="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 60 -movflags +faststart -shortest"
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav $V -crf 8 -tune film -c:a aac -b:a 320k out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav $V -crf 17 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
