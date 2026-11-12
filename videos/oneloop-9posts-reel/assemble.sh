#!/bin/bash
# "how I'd turn 1 photo into 9 posts": MVI_0680 (floral shirt sketching in a notebook) under a sticker of one photo (the One Loop
# site on a laptop, MVI_0727) and a 3x3 grid of nine One Loop posts made from it, timed to the reference (8.0 s loop).
# Sound: the reference's own song (one loop) + one real paper drop as the grid lands (Real SFX, CC0).
# usage: SRC=<MVI_0680.mp4> bash assemble.sh
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
SRC=${SRC:-/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/r2/MVI_0680.mp4}; SONG=${SONG:-assets/song_ref.wav}
END=8.0; NF=480; N=OneLoop_1Photo9Posts_1080x1920_60fps
mkdir -p out; node render_overlay.mjs
# overlay frames (60 fps), cut points measured from the reference: hook 0, grid 184, end 480
rm -rf out/seq; mkdir -p out/seq
cuts="0:hook 184:grid"
for f in $(seq 0 $((NF-1))); do sc=hook; for c in $cuts; do [ $f -ge ${c%%:*} ] && sc=${c#*:}; done; ln -s ../ov/$sc.png out/seq/$(printf %04d $f).png; done
# picture: the first 7.4 s of sketching, stretched to 8.2 s (492 frames); output = frames 12..479, then frames 480..491
# cross-fade into frames 0..11, so the last frame flows into the first and the reel loops without a jump
ffmpeg -nostdin -v error -y -i "$SRC" -framerate 60 -i out/seq/%04d.png -filter_complex \
 "[0:v]trim=0:7.4,setpts=PTS-STARTPTS,transpose=2,eq=contrast=1.03:saturation=1.02,setpts=PTS*8.2/7.4,fps=60,trim=end_frame=492,setpts=PTS-STARTPTS,split=3[s1][s2][s3];\
  [s1]trim=start_frame=12:end_frame=480,setpts=PTS-STARTPTS[a];[s2]trim=start_frame=480:end_frame=492,setpts=PTS-STARTPTS[b];[s3]trim=end_frame=12,setpts=PTS-STARTPTS[c];\
  [b][c]xfade=transition=fade:duration=0.2:offset=0[x];[a][x]concat=n=2:v=1:a=0,fps=60[bg];\
  [1:v]format=rgba[ov];[bg][ov]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]" \
 -map "[v]" -frames:v $NF -c:v libx264 -preset slow -crf 8 -r 60 -an out/video.mp4
ffmpeg -nostdin -v error -y -i "$SONG" -af "aresample=48000,apad=whole_dur=$END,atrim=0:$END" -ac 2 -c:a pcm_s24le out/bed.wav
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/bed.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le out/video_v.mov
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_v.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/mix.mp4" --base-audio "$HERE/out/bed.wav" --sfx-trim-db ${SFX_TRIM:-12}) 2>/dev/null
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/mix_resolved_cues.json" "$W/result/mix_sfx_track.wav" > "$W/result/critique.txt") 2>/dev/null || true
grep -E "^\| (sync|balance|headroom|loudness)" "$W/result/critique.txt" || true
cp "$W/result/mix_sfx_track.wav" out/stems/sfx.wav; cp out/bed.wav out/stems/song.wav
ffmpeg -nostdin -v error -y -i out/bed.wav -i out/stems/sfx.wav -filter_complex "[1:a]apad=whole_dur=$END[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$END" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,atrim=0:$END" -c:a pcm_s24le out/mix_master.wav
for q in "MASTER 10 320k" "share 15 256k"; do set -- $q
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf $2 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -profile:v high -c:a aac -b:a $3 -af apad -t $END -movflags +faststart out/${N}_$1.mp4
done
rm -rf out/video_v.mov out/_pre.wav out/seq out/sfxwork/result/mix.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size:stream=nb_frames -of csv=p=0 "$f" | tr '\n' ' ')"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
