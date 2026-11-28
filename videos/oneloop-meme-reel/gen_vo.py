"""Generate the pitch lines in Naga Datta's cloned voice (approved), panicked delivery. Loads the model once.
usage: ../../tools/voice-clone/.venv/bin/python gen_vo.py [ids...]"""
import sys, json, os, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
V = '../../tools/voice-clone/voices/naga-datta'; cfg = json.load(open(V + '/voice.json'))
lines = json.load(open('script.json')); want = set(sys.argv[1:])
m = ChatterboxTTS.from_pretrained(device='cpu')
for i, (k, text) in enumerate(lines):
    if want and k not in want: continue
    for take, (ex, cw) in enumerate([(.7, .3), (.55, .35)]):         # two takes: panicked, and a steadier one
        torch.manual_seed(10 + i * 7 + take)
        wav = m.generate(text, audio_prompt_path=V + '/ref.wav', exaggeration=ex, cfg_weight=cw)
        torchaudio.save(f'vo/{k}_t{take}.wav', wav, m.sr); print(k, take, round(wav.shape[-1] / m.sr, 2), flush=True)
