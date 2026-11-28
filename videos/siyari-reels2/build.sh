#!/usr/bin/env bash
# Music + final encodes for the three Siyari reels. Each uses its reference video's own music (user's instruction), cut as the edit was timed:
#   earrings: ref/r1.mp4 0-30.0 s (100 bpm; products change every 8 beats)      shapes: ref/r2.mp4 1.0-10.3 s (stone swaps on its hits)
#   ring:     ref/r3.mp4 rebuilt to the full 15.06 s track: the recording muted its first 2.26 s, so 0-2.56 s comes from the recording's
#             second loop (14.87-17.43) and the rest from 2.26-14.76 (track time = recording time + 0.30), joined with a 30 ms crossfade.
# Loudness -14 LUFS / -1 dBTP (Instagram). MASTER crf 12 + share crf 18, 1080x1920 30 fps.   bash build.sh [earrings|shapes|ring]
set -euo pipefail; cd "$(dirname "$0")"; mkdir -p out/audio
music() { local n=$1
  case $n in
    earrings) ffmpeg -nostdin -v error -y -ss 0 -t 30.0 -i ref/r1.mp4 -vn -af aresample=48000 -c:a pcm_f32le out/audio/_$n.wav; D=30.0;;
    shapes)   ffmpeg -nostdin -v error -y -ss 1.0 -t 9.3 -i ref/r2.mp4 -vn -af aresample=48000 -c:a pcm_f32le out/audio/_$n.wav; D=9.3;;
    ring)     ffmpeg -nostdin -v error -y -i ref/r3.mp4 -filter_complex "[0:a]atrim=14.87:17.46,asetpts=PTS-STARTPTS,aresample=48000[a];[0:a]atrim=2.23:14.76,asetpts=PTS-STARTPTS,aresample=48000[b];[a][b]acrossfade=d=0.03:c1=tri:c2=tri" -c:a pcm_f32le out/audio/_$n.wav; D=15.06;;
  esac
  ffmpeg -nostdin -v error -y -i out/audio/_$n.wav -af "apad,atrim=0:$D,afade=t=out:st=$(echo "$D-0.15" | bc):d=0.15" -c:a pcm_f32le out/audio/__$n.wav
  J=$(ffmpeg -nostdin -hide_banner -i out/audio/__$n.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
  ffmpeg -nostdin -v error -y -i out/audio/__$n.wav -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000" -c:a pcm_s24le out/audio/$n.wav
  rm -f out/audio/_$n.wav out/audio/__$n.wav; }
enc() { local n=$1 title=$2; music $n
  O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -movflags +faststart -t $D"
  ffmpeg -nostdin -v error -y -i out/$n.mp4 -i out/audio/$n.wav $O -crf 12 -tune animation -c:a aac -b:a 320k out/${title}_1080x1920_30fps_MASTER.mp4
  ffmpeg -nostdin -v error -y -i out/$n.mp4 -i out/audio/$n.wav $O -crf 18 -maxrate 12M -bufsize 24M -c:a aac -b:a 256k out/${title}_1080x1920_30fps_share.mp4
  for f in out/${title}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$f")"; done
  ffmpeg -nostdin -hide_banner -i out/${title}_1080x1920_30fps_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"; }
for n in ${@:-earrings shapes ring}; do
  case $n in earrings) enc earrings Siyari_TheEarringEdit;; shapes) enc shapes Siyari_WhatIsYourNextShape;; ring) enc ring Siyari_ImagineItDesignItWearIt;; esac
done
