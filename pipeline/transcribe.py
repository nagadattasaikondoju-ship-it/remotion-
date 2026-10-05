"""Stage 1a: transcribe a video with word-level timestamps.

Whisper's usual model hosts (Hugging Face / OpenAI CDN) aren't always reachable,
so this uses sherpa-onnx, which runs either:
  - NVIDIA Parakeet-TDT 0.6B (default; per-token timestamps -> word timings), or
  - Whisper via sherpa-onnx (text only; sherpa's Whisper export has no timestamps).

Output: {"duration", "text", "words": [{"text", "start", "end"}]}
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import sherpa_onnx
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_MODEL = os.path.join(HERE, "models", "sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8")


def ffmpeg(*args):
    # Remotion ships ffmpeg; no system install needed.
    subprocess.run(["npx", "remotion", "ffmpeg", "-hide_banner", "-y", "-v", "error", *args], check=True, cwd=ROOT)


def extract_audio(video, wav):
    ffmpeg("-i", video, "-vn", "-ac", "1", "-ar", "16000", wav)


def tokens_to_words(tokens, starts, durations):
    """Parakeet emits sentencepiece tokens; a leading space starts a new word."""
    words = []
    for tok, start, dur in zip(tokens, starts, durations):
        end = start + dur
        is_punct = tok.strip() and all(not c.isalnum() for c in tok.strip())
        if tok.startswith(" ") or not words:
            if is_punct and words:
                words[-1]["text"] += tok.strip()
                continue
            words.append({"text": tok.strip(), "start": start, "end": end})
        else:
            words[-1]["text"] += tok
            if not is_punct:
                words[-1]["end"] = end
    for w in words:
        w["start"] = round(float(w["start"]), 3)
        w["end"] = round(float(max(w["end"], w["start"] + 0.05)), 3)
    return [w for w in words if w["text"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out")
    ap.add_argument("--model-dir", default=DEFAULT_MODEL)
    ap.add_argument("--threads", type=int, default=os.cpu_count() or 4)
    a = ap.parse_args()

    d = a.model_dir
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=os.path.join(d, "encoder.int8.onnx"),
        decoder=os.path.join(d, "decoder.int8.onnx"),
        joiner=os.path.join(d, "joiner.int8.onnx"),
        tokens=os.path.join(d, "tokens.txt"),
        model_type="nemo_transducer",
        num_threads=a.threads,
    )

    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "a.wav")
        extract_audio(a.video, wav)
        audio, sr = sf.read(wav, dtype="float32")

    # Decode in ~60s windows cut at the quietest point so long clips fit in memory.
    words, offset, win = [], 0, 60 * sr
    while offset < len(audio):
        end = min(len(audio), offset + win)
        if end < len(audio):
            search = audio[end - 5 * sr:end]
            frame = int(0.02 * sr)
            energy = np.convolve(search ** 2, np.ones(frame), "valid")
            end = end - 5 * sr + int(np.argmin(energy))
        s = rec.create_stream()
        s.accept_waveform(sr, audio[offset:end])
        rec.decode_stream(s)
        r = s.result
        t0 = offset / sr
        words += tokens_to_words(r.tokens, [t + t0 for t in r.timestamps], r.durations)
        offset = end

    out = {
        "source": os.path.basename(a.video),
        "duration": round(len(audio) / sr, 3),
        "model": os.path.basename(d),
        "text": " ".join(w["text"] for w in words),
        "words": words,
    }
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    print(f"transcribed {len(words)} words -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
