#!/usr/bin/env bash
# The reel's base picture, from the reference (25 Nov, second pass: "clarity, realism, smoothness"):
#   1. detail: the Real-ESRGAN upscale (REF_UP) blended 55/45 with a sharpened lanczos upscale of the same crop (REF_CROP), so edges and
#      text stay crisp but real texture (sand, grass, aerials) comes back instead of ESRGAN's painted look; a gentle clarity grade
#   2. smoothness: the screen recording repeats ~20% of its frames (1186 unique of 1494), so motion stutters. Repeats are dropped
#      (mpdecimate) and refilled with motion-compensated frames (minterpolate mci), in 4 chunks in parallel
#   REF_UP=<ref_up.mp4> REF_CROP=<ref_crop.mp4> bash smooth_base.sh   -> out/base_smooth.mp4 (1080x1920, 30 fps, reference framing)
set -euo pipefail; HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"; mkdir -p out/chunks
REF_UP=${REF_UP:?}; REF_CROP=${REF_CROP:?}; N=1493; K=4; L=$(( (N + K - 1) / K ))
ffmpeg -nostdin -v error -y -i "$REF_UP" -i "$REF_CROP" -filter_complex "[1:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.8:5:5:0[l];[0:v][l]blend=all_expr='A*0.55+B*0.45',unsharp=3:3:0.35:3:3:0,eq=contrast=1.04:saturation=1.06,trim=end_frame=$N,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -preset fast -crf 9 -r 30 out/chunks/detail.mp4
for k in $(seq 0 $((K - 1))); do a=$((k * L)); b=$(( (k + 1) * L < N ? (k + 1) * L : N ))
  ffmpeg -nostdin -v error -y -i out/chunks/detail.mp4 -vf "trim=start_frame=$a:end_frame=$((b + 12)),setpts=PTS-STARTPTS,mpdecimate=hi=200:lo=100:frac=0.1,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:scd=fdiff,tpad=stop=30:stop_mode=clone,trim=end_frame=$((b - a)),setpts=PTS-STARTPTS" \
    -c:v libx264 -preset fast -crf 9 -r 30 out/chunks/c$k.mp4 &
done; wait
for k in $(seq 0 $((K - 1))); do echo "file 'c$k.mp4'"; done > out/chunks/list.txt
ffmpeg -nostdin -v error -y -f concat -safe 0 -i out/chunks/list.txt -c copy out/base_smooth.mp4
echo "out/base_smooth.mp4: $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 out/base_smooth.mp4) frames"
for k in $(seq 0 $((K - 1))); do echo "chunk $k: $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 out/chunks/c$k.mp4) frames"; done
rm -rf out/chunks
