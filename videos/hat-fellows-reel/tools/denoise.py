# Voice clean-up: DeepFilterNet3 (deep-learning speech enhancement, MIT/Apache) on the WHOLE source take before cutting,
# so the noise reduction has continuous context. Model weights: ~/.cache/DeepFilterNet/DeepFilterNet3.
#   PYTHONPATH=<dfnlib> python3 tools/denoise.py in.wav out.wav [atten_lim_db]
import sys, os, torch
from df.enhance import init_df, enhance, load_audio, save_audio
model, st, _ = init_df(model_base_dir=os.path.expanduser("~/.cache/DeepFilterNet/DeepFilterNet3"))
audio, _ = load_audio(sys.argv[1], sr=st.sr())
lim = float(sys.argv[3]) if len(sys.argv) > 3 else None
out = enhance(model, st, audio, atten_lim_db=lim)
save_audio(sys.argv[2], out, st.sr())
print("denoised", audio.shape, "lim", lim)
