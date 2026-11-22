#!/usr/bin/env bash
# One Loop website series ep. 01: "if i rebuilt your brand's website..." AI-slop site vs the rebuilt site (same brand, Mindly).
# hook (MVI_0706 from the One Loop B-roll Drive: typing, then hand to chin; 143 frames = 2.383 s). Its last 0.22 s push in
# toward his laptop while the caption fades; the screen part (index.html, 60 fps) starts on that same frame and the site
# grows out of the laptop (no dark gap). 13.27 s, 1080x1920, 60 fps. Two versions of the screen part:
#   TEXT  = every overlay (AI slop. / now watch it get rebuilt... / your brand deserves the second one. / comment "SITE")
#   CLEAN = no text while the site changes; the full site holds, then the comment "SITE" CTA + logo
# Song: "DANCE..." as heard in ep. 03 of the Instagram series (only copy on hand: that reel, whose pops sit on every 2-beat
# step). Extended to 13.27 s by repeating 6 beats [5.538, 8.724) cut just before the kicks. Clarity EQ (sub-rumble cut, a
# little less 300 Hz mud, a touch of air), then the sound pipeline (real-sfx from_cues + mix -> critique), loudnorm -14 / -1.2.
#   B=<MVI_0706.MP4> U=<ep03 reel.mp4> bash assemble.sh      (render first: node render.cjs caption; VARIANT=text|clean node render.cjs ui)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
B=${B:?B-roll MVI_0706}; U=${U:?ep. 03 reel with the song}
N=OneLoop_IfIRebuiltYourBrandsWebsite_ep01
Z="(1+0.5*pow(max(0\,(t-2.163)/0.22)\,2))"
ffmpeg -nostdin -v error -y -ss 0.35 -i "$B" -loop 1 -framerate 60 -t 2.3834 -i out/caption.png -filter_complex "
 [1:v]format=rgba,fade=t=out:st=2.19:d=0.16:alpha=1[c];
 [0:v]transpose=2,eq=contrast=1.06:saturation=1.08:gamma=0.97,fps=60,trim=end_frame=143,setpts=PTS-STARTPTS,format=rgba[h];
 [h][c]overlay=format=auto:shortest=1,scale=w='2*trunc(540*$Z)':h='2*trunc(960*$Z)':eval=frame:flags=bicubic,crop=1080:1920:x='180*(iw/1080)-180':y='1380*(ih/1920)-1380',format=yuv420p[v]" \
 -map "[v]" -c:v libx264 -preset slow -crf 8 -tune film -r 60 out/hook.mp4
for V in text clean; do
  ffmpeg -nostdin -v error -y -i out/hook.mp4 -i out/ui_$V.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
    -c:v libx264 -preset slow -crf 8 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 60 out/video_$V.mp4
done
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/video_text.mp4)
ffmpeg -nostdin -v error -y -i "$U" -filter_complex "[0:a]aresample=48000,atrim=0:8.724,asetpts=PTS-STARTPTS[a];[0:a]aresample=48000,atrim=5.538:8.724,asetpts=PTS-STARTPTS[b];[0:a]aresample=48000,atrim=8.724,asetpts=PTS-STARTPTS[c];[a][b]acrossfade=d=0.006:c1=tri:c2=tri[ab];[ab][c]acrossfade=d=0.006:c1=tri:c2=tri,highpass=f=28:poles=2,equalizer=f=300:t=q:w=1.0:g=-1.5,highshelf=f=9000:g=1.5,afade=t=out:st=13.12:d=0.15,apad,atrim=0:$D[o]" \
  -map "[o]" -ac 2 -c:a pcm_f32le out/song.wav
python3 - <<'EOF'
import json
B = 60 / 113; P = lambda k: 3.442 + (k - 1) * 2 * B
json.dump([{"t": 4.0, "type": "swipe", "g": .45, "note": "the agent cursors swarm in from the edges"},
           {"t": round(P(2) + .01, 3), "type": "glitch", "g": .35, "note": "the slop is deleted (with the song's own pop)"},
           {"t": round(P(8) - .05, 3), "type": "softwhoosh", "g": .35, "note": "the browser shrinks up for the CTA"}], open("sfx_cues.json", "w"), indent=1)
json.dump({"swipe": {"ids": [53], "role": "whoosh"}, "glitch": {"ids": [62], "role": "glitch"}, "softwhoosh": {"ids": [57], "role": "whoosh"}}, open("sfx_map.json", "w"), indent=1)
EOF
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result"
ffmpeg -nostdin -v error -y -i out/video_text.mp4 -i out/song.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/_a.mov
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
O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 60 -movflags +faststart -shortest"
for V in text clean; do T=$(echo $V | tr a-z A-Z)
  ffmpeg -nostdin -v error -y -i out/video_$V.mp4 -i out/mix_master.wav $O -crf 8 -tune film -c:a aac -b:a 320k out/${N}_${T}_1080x1920_60fps_MASTER.mp4
  ffmpeg -nostdin -v error -y -i out/video_$V.mp4 -i out/mix_master.wav $O -crf 17 -maxrate 14M -bufsize 28M -c:a aac -b:a 320k out/${N}_${T}_1080x1920_60fps_share.mp4
done
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
ffmpeg -nostdin -hide_banner -i out/${N}_TEXT_1080x1920_60fps_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
