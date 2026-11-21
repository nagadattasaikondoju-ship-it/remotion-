#!/usr/bin/env bash
# tools_sheet.sh out.jpg img1 img2 … → contact sheet, 4 per row at 360×640 with time labels
set -e; OUT=$1; shift; n=$#; cols=4; [ $n -lt 4 ] && cols=$n
args=(); f=""; i=0; lay=""
for im in "$@"; do args+=(-i "$im"); lab=$(basename "$im" .png)
  f+="[$i]scale=480:270,drawtext=text='$lab':x=8:y=8:fontsize=26:fontcolor=yellow:box=1:boxcolor=black@0.6[v$i];"
  lay+="$(( (i%cols)*480 ))_$(( (i/cols)*270 ))|"; i=$((i+1)); done
ins=""; for ((k=0;k<n;k++)); do ins+="[v$k]"; done
ffmpeg -v error -y "${args[@]}" -filter_complex "${f}${ins}xstack=inputs=$n:layout=${lay%|}:fill=gray" "$OUT"
