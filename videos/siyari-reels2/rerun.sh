#!/usr/bin/env bash
# Re-run the parts that crashed (too many Chromium instances at once), at most 5 workers, then assemble + encode each reel.
cd "$(dirname "$0")"; R2=$(pwd); R1=$(cd ../siyari-reel && pwd); NP=$(npm root -g)
job() { case $1 in
  v3_*) f0=${1#v3_}; f0=${f0%_*}; f1=${1##*_}; (cd $R1 && F0=$f0 F1=$f1 OUT=out/v3/p$f0.mp4 NODE_PATH=$NP node render.cjs > out/v3/p$f0.log 2>&1);;
  ring2_3) F0=282 F1=375 PAGE=ring2.html OUT=out/parts/ring2_3.mp4 NODE_PATH=$NP node render.cjs > out/parts/ring2_3.log 2>&1;;
  ear_*) i=${1#ear_}; f0=$((i*217)); f1=$(( (i+1)*217 < 865 ? (i+1)*217 : 865 )); F0=$f0 F1=$f1 PAGE=earrings.html OUT=out/parts/earrings_$i.mp4 NODE_PATH=$NP node render.cjs > out/parts/earrings_$i.log 2>&1;;
esac; }
export -f job; export R1 R2 NP
# wait until the still-running parts are done, so at most 5 Chromium instances ever run
while [ "$(pgrep -fc 'node render.cjs')" -gt 1 ]; do sleep 10; done
printf "%s\n" v3_0_89 v3_89_178 ring2_3 ear_0 ear_1 ear_2 ear_3 | xargs -P 5 -I{} bash -c 'job {}'
# reel 1 v3 assembly (same steps as render_v3.sh after its renders)
(cd $R1 && N=Siyari_YourDesignMadeReal_RingChain_v3 && FPS=60 && DUR=8.933 && \
 ffmpeg -nostdin -v error -y -i out/v3/p0.mp4 -i out/v3/p89.mp4 -i out/v3/p178.mp4 -i out/v3/p266.mp4 -i out/v2/p354.mp4 -i out/v2/p445.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v]concat=n=6:v=1:a=0,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 10 -tune animation -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS out/picture_v3.mp4 && \
 O="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r $FPS -movflags +faststart -t $DUR" && \
 ffmpeg -nostdin -v error -y -i out/picture_v3.mp4 -i out/music_v2.wav $O -crf 12 -tune animation -c:a aac -b:a 320k out/${N}_1080x1920_60fps_MASTER.mp4 && \
 ffmpeg -nostdin -v error -y -i out/picture_v3.mp4 -i out/music_v2.wav $O -crf 18 -maxrate 14M -bufsize 28M -c:a aac -b:a 256k out/${N}_1080x1920_60fps_share.mp4 && \
 for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames:format=duration,size -of csv=p=0 "$f" | tr '\n' ' ')"; done > out/v3/all.log 2>&1)
for n in earrings ring2; do for i in 0 1 2 3; do echo "file '${n}_$i.mp4'"; done > out/parts/${n}_list.txt
  ffmpeg -nostdin -v error -y -f concat -safe 0 -i out/parts/${n}_list.txt -c copy out/$n.mp4 && echo "out/$n.mp4: $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 out/$n.mp4) frames" > out/${n}_render.log; done
bash build.sh earrings > out/build_earrings.log 2>&1
