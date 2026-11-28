#!/usr/bin/env bash
# v2 (user's note): one pass, no repeat, and the reference ad's own music instead of designed SFX.
# Picture: frames 0-275 (0-4.6 s) are the v1 render (identical code path); 276-535 re-rendered into out/v2/ (rings to 5.9 s, logo sting to 8.933 s).
# Music: the reference's loop unit, 6.667-15.600 s of ref/reference.mp4 (its own cut lands on the beat at 5.9 s), loudness -14 LUFS / -1 dBTP.
set -euo pipefail; cd "$(dirname "$0")"
N=Siyari_YourDesignMadeReal_RingChain_v2; FPS=60; DUR=8.933
ffmpeg -nostdin -v error -y -i out/reel.mp4 -i out/v2/p276.mp4 -i out/v2/p316.mp4 -i out/v2/p354.mp4 -i out/v2/p445.mp4 \
  -filter_complex "[0:v]trim=end_frame=276,setpts=PTS-STARTPTS[a];[a][1:v][2:v][3:v][4:v]concat=n=5:v=1:a=0,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 10 -tune animation -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture_v2.mp4
ffmpeg -nostdin -v error -y -ss 6.667 -t $DUR -i ref/reference.mp4 -vn -af "aresample=48000,afade=t=in:d=0.01,afade=t=out:st=$(echo "$DUR-0.12" | bc):d=0.12" -c:a pcm_f32le out/_m.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_m.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_m.wav -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000" -c:a pcm_s24le out/music_v2.wav; rm -f out/_m.wav
O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS -movflags +faststart -t $DUR"
ffmpeg -nostdin -v error -y -i out/picture_v2.mp4 -i out/music_v2.wav $O -crf 12 -tune animation -c:a aac -b:a 320k out/${N}_1080x1920_60fps_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/picture_v2.mp4 -i out/music_v2.wav $O -crf 18 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_1080x1920_60fps_share.mp4
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames:format=duration,size -of csv=p=0 "$f" | tr '\n' ' ')"; done
ffmpeg -nostdin -hide_banner -i out/${N}_1080x1920_60fps_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
