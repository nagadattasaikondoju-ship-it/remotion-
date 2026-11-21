#!/usr/bin/env bash
# Veridale ep. 03 — hook (MVI_0425: typing, then hand to chin, thinking; 143 frames = 2.383 s, ends on the beat drop) + profile build (462 frames)
# → 10.08 s, 1080×1920, 60 fps. Audio: "DANCE…" (Slayyyter), lifted from the user's reference recording, + real SFX
# (Openverse → Real SFX → Earshot), two-pass loudnorm −14 LUFS.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
U=/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e
SRC="${SRC:-/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/ol/drive/MVI_0425.mp4}"  # camera original from Drive (file 10vEEGDig17NjeoMI25B7heo1jv6foN4R), landscape → rotated
REF="${REF:-$U/e7d3e28e-WhatsApp_Video_2026-10-26_at_2.40.15_PM_1.mp4}"   # reference reel screen recording (the song)
HOOK_IN=2.95      # last keystrokes → hand to chin → thinking on the cut (ep. 01 used this clip's opening typing)
SONG_IN=3.73      # the reference reel's hook in its screen recording (+30 ms so the kicks sit on the steps)
N=Veridale_IfIHandledYourRealEstateBrand_ep03_1080x1920_60fps
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
[ -f out/caption.png ] && [ -f out/ui/f_00461.png ] || { node render.mjs caption; node render.mjs ui; }

ffmpeg -nostdin -v error -y -ss $HOOK_IN -i "$SRC" -i out/caption.png -framerate 60 -i out/ui/f_%05d.png -filter_complex "
  [0:v]transpose=2,eq=contrast=1.06:saturation=1.08:gamma=0.97,fps=60,trim=end_frame=143,setpts=PTS-STARTPTS,format=rgba[h];
  [h][1:v]overlay=format=auto[hc];
  [2:v]fps=60,setpts=PTS-STARTPTS,format=rgba[u];
  [hc][u]concat=n=2:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 8 -tune film -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 60 -movflags +faststart out/video.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/video.mp4)
ffmpeg -nostdin -v error -y -ss $SONG_IN -t "$D" -i "$REF" -vn -ac 2 -ar 48000 -af "afade=t=out:st=$(python3 -c "print(round($D-0.12,3))"):d=0.12" out/song.wav
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/song.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/video_song.mov

# Real SFX: the film's own cue list → Earshot-picked real recordings, placed on the frame
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_song.mov" --out "$W/work/cues.json" \
   --ui library --map "$HERE/sfx_map.json" --kind pop=slices:10 --one-source pop \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/veridale_sfx.mp4" --base-audio "$HERE/out/song.wav" --sfx-trim-db 0)
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/veridale_sfx_resolved_cues.json" "$W/result/veridale_sfx_sfx_track.wav" > "$W/result/critique.txt") || true; head -16 "$W/result/critique.txt"
cp "$W/result/veridale_sfx_sfx_track.wav" out/stems/sfx.wav; cp "$W/result/veridale_sfx_base.wav" out/stems/song.wav
cp "$W/result/veridale_sfx_resolved_cues.json" "$W/result/veridale_sfx_cue_report.md" out/stems/ 2>/dev/null || true
ffmpeg -nostdin -v error -y -i out/stems/song.wav -i out/stems/sfx.wav -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0:duration=first" -c:a pcm_f32le out/mix.wav

norm() {  # two-pass loudnorm −14 LUFS / TP −1.2 (ffmpeg 6.1)
  local J; J=$(ffmpeg -nostdin -hide_banner -i "$1" -af loudnorm=I=-14:TP=-1.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
  ffmpeg -nostdin -v error -y -i "$1" -af "loudnorm=I=-14:TP=-1.2:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad=whole_dur=$D,atrim=0:$D" -c:a pcm_s24le "$2"
}
norm out/mix.wav out/mix_master.wav
V="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 60 -movflags +faststart -shortest"
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav $V -crf 8 -tune film -c:a aac -b:a 320k out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav $V -crf 17 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_share.mp4
# for posting with Instagram's own audio ("Use audio" on the reference reel): picture + SFX only, no song
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/stems/sfx.wav -af apad $V -crf 17 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_share_SFX-only-no-song.mp4
for f in out/${N}_*.mp4; do echo "$f"; ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,r_frame_rate,width,height:format=duration,bit_rate,size -of csv=p=0 "$f"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
