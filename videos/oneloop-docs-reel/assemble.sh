#!/bin/bash
# "What we send a client the day they sign": MVI_0425 (green polo typing, then thinking) under five hard-cut One Loop documents,
# timed frame for frame to the reference reel (8.4 s loop), with the reference's own song plus a real paper drop on each document.
# usage: SRC=<MVI_0425.mp4> SONG=<song_ref.wav, one 8.4 s loop> bash assemble.sh
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
SC=/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/docreel
SRC=${SRC:-$SC/MVI_0425.mp4}; SONG=${SONG:-$SC/song_ref.wav}
END=8.4; N=OneLoop_DayTheySign_1080x1920_60fps
mkdir -p out
node render_overlay.mjs
# ---- overlay track: one symlinked PNG per output frame, hard cuts on the reference's frames (60 fps) ----
rm -rf out/seq; mkdir -p out/seq
cuts="0:hook 116:contract 172:invoice 234:welcome 298:questionnaire 362:strategy 434:hook"
for f in $(seq 0 503); do sc=hook; for c in $cuts; do [ $f -ge ${c%%:*} ] && sc=${c#*:}; done; ln -s ../ov/$sc.png out/seq/$(printf %04d $f).png; done
# ---- picture: upright, 15 % punch-in framed high (face clear of the documents, blown ceiling cropped).
# 8.308 s of footage is stretched to 8.6 s (516 frames, 3.5 % slower). Output = frames 12..503, then the last 12 frames
# cross-fade into frames 0..11, so frame 503 flows into frame 0 and the reel loops without a jump.
G="transpose=2,scale=1242:2208:flags=lanczos,crop=1080:1920:81:288,eq=contrast=1.04:saturation=1.03,unsharp=5:5:0.4"
ffmpeg -nostdin -v error -y -i "$SRC" -framerate 60 -i out/seq/%04d.png -filter_complex \
 "[0:v]$G,setpts=PTS*8.6/8.3083,fps=60,trim=end_frame=516,setpts=PTS-STARTPTS,split=3[s1][s2][s3];\
  [s1]trim=start_frame=12:end_frame=504,setpts=PTS-STARTPTS[a];\
  [s2]trim=start_frame=504:end_frame=516,setpts=PTS-STARTPTS[b];[s3]trim=end_frame=12,setpts=PTS-STARTPTS[c];\
  [b][c]xfade=transition=fade:duration=0.2:offset=0[x];[a][x]concat=n=2:v=1:a=0,fps=60[bg];\
  [1:v]format=rgba[ov];[bg][ov]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]" \
 -map "[v]" -frames:v 504 -c:v libx264 -preset slow -crf 8 -r 60 -an out/video.mp4
# ---- sound: the song (one loop) + real CC0 paper drops placed by Real SFX ----
ffmpeg -nostdin -v error -y -i "$SONG" -af "aresample=48000,apad=whole_dur=$END,atrim=0:$END" -ac 2 -c:a pcm_s24le out/bed.wav
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/bed.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le out/video_v.mov
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_v.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/doc_sfx.mp4" --base-audio "$HERE/out/bed.wav" --sfx-trim-db ${SFX_TRIM:-20})
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/doc_sfx_resolved_cues.json" "$W/result/doc_sfx_sfx_track.wav" > "$W/result/critique.txt") || true; sed -n 1,14p "$W/result/critique.txt"
cp "$W/result/doc_sfx_sfx_track.wav" out/stems/sfx.wav; cp out/bed.wav out/stems/song.wav
ffmpeg -nostdin -v error -y -i out/bed.wav -i out/stems/sfx.wav -filter_complex "[1:a]apad=whole_dur=$END[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$END" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,atrim=0:$END" -c:a pcm_s24le out/mix_master.wav
# ---- deliverables ----
for q in "MASTER 10 320k" "share 15 256k"; do set -- $q
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf $2 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -profile:v high -c:a aac -b:a $3 -af apad -t $END -movflags +faststart out/${N}_$1.mp4
done
rm -f out/video_v.mov out/_pre.wav
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size:stream=nb_frames -of csv=p=0 "$f" | tr '\n' ' ')"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
