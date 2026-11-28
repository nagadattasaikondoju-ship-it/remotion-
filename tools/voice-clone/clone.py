"""Clone a voice with Chatterbox (MIT, local CPU). Only with the speaker's consent.
usage: .venv/bin/python clone.py REF.wav OUT.wav "text" [exaggeration] [cfg_weight] [seed]"""
import sys, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
ref, out, text = sys.argv[1:4]
ex = float(sys.argv[4]) if len(sys.argv) > 4 else .5
cfg = float(sys.argv[5]) if len(sys.argv) > 5 else .5
torch.manual_seed(int(sys.argv[6]) if len(sys.argv) > 6 else 1)
m = ChatterboxTTS.from_pretrained(device="cpu")
wav = m.generate(text, audio_prompt_path=ref, exaggeration=ex, cfg_weight=cfg)
torchaudio.save(out, wav, m.sr); print(out, round(wav.shape[-1] / m.sr, 2), "s")
