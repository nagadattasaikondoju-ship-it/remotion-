#!/usr/bin/env bash
# Rebuild the narration: Kokoro hf_alpha (local, explainroo's cached model) reads each line of lines.json with American
# English phonemes at 1.12×; silences are trimmed; lines are placed with fixed gaps into one continuous 42.5 s master.
set -euo pipefail; cd "$(dirname "$0")"; mkdir -p raw trim
node tts.mjs raw hf_alpha a 1.12 @lines.json
for f in raw/*.wav; do ffmpeg -v error -y -i "$f" -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse" "trim/$(basename "$f")"; done
python3 -I - <<'PY'
import json, subprocess
lead, gaps, END = 0.40, [0.30, 0.35, 0.30, 0.25, 0.25, 0.35, 0.30, 0.35, 0.35], 42.5
dur = lambda f: float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
t, starts = lead, {}
for i in range(1, 11): starts[i] = round(t, 3); t += dur(f"trim/L{i:02d}.wav") + (gaps[i-1] if i < 10 else 0)
ins = sum([["-i", f"trim/L{i:02d}.wav"] for i in range(1, 11)], [])
fc = ";".join(f"[{i-1}]aresample=48000,adelay={int(starts[i]*1000)}|{int(starts[i]*1000)}[a{i}]" for i in range(1, 11)) + ";" + "".join(f"[a{i}]" for i in range(1, 11)) + f"amix=inputs=10:normalize=0,apad=whole_dur={END},atrim=0:{END}[o]"
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",fc,"-map","[o]","-ac","1","-ar","48000","voice_master.wav"],check=True)
json.dump({"lead": lead, "gaps": gaps, "END": END, "starts": starts}, open("lines_timing.json","w"), indent=1); print(starts)
PY
