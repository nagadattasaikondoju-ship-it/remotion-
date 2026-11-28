"""Speak text in a saved voice.  usage: .venv/bin/python say.py naga-datta OUT.wav "text" [seed]
Long scripts: one sentence per call works best; join the WAVs afterwards."""
import sys, json, os, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
name, out, text = sys.argv[1:4]
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voices', name); cfg = json.load(open(os.path.join(d, 'voice.json')))
ref = os.path.join(d, 'ref.wav')
if not os.path.exists(ref): sys.exit(f'{ref} missing: download ref.wav from the Drive backup named in {d}/voice.json')
s = cfg['settings']; torch.manual_seed(int(sys.argv[4]) if len(sys.argv) > 4 else s['seed'])
m = ChatterboxTTS.from_pretrained(device='cpu')
wav = m.generate(text, audio_prompt_path=ref, exaggeration=s['exaggeration'], cfg_weight=s['cfg_weight'])
torchaudio.save(out, wav, m.sr); print(out, round(wav.shape[-1] / m.sr, 2), 's')
