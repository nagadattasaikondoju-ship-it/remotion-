# Auto-edit pipeline

Pre-processing for the talking-head → vertical-short composition. Runs once per
source video; Remotion only reads the JSON it produces.

```bash
pipeline/setup.sh                        # once: python deps + models (~480 MB)
pipeline/run.sh ~/Downloads/clip.mp4     # stages 1-2 -> public/media/source.*
```

| Output | What |
| --- | --- |
| `public/media/source.mp4` | copy of the input |
| `source.words.json` | transcript with word-level `{text,start,end}` (seconds) |
| `source.edl.json` | **edit-decision list** — contiguous `{start,end,keep,reason,text}` segments; the cut list |
| `source.faces.json` | per-frame face box `{f,x,y,w,h}` normalised 0-1, gaps interpolated |

## Stage 1 — transcription + silence/filler detection

- `transcribe.py` — speech-to-text with word timestamps via
  [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) running NVIDIA
  Parakeet-TDT 0.6B. (Whisper was the plan, but its model hosts are blocked in
  the build environment and sherpa's Whisper export has no timestamps; Parakeet
  is as accurate on English and gives per-token timings.)
- `build_edl.py` — combines:
  - `ffmpeg silencedetect` (default `-30 dB`, `> 0.3 s`), keeping 80 ms after
    and 100 ms before speech so cuts don't clip breaths;
  - a 30 ms guard around every transcribed word, so quiet words that dip
    under the threshold are never cut;
  - filler words: `um/uh/erm/…` always, `like` only when isolated by pauses or
    followed by a comma, `you know`;
  - **retake candidates**: any 3-word phrase repeated within 10 s is attached to
    the segment as `review` — never cut automatically.

### Reviewing cuts

Add `pipeline/overrides/source.json` (see `overrides/example.json`) with
`{start, end, keep, note}` ranges and re-run `run.sh` — overrides win over
everything else. You can also hand-edit `source.edl.json` directly, and fix
mis-heard words in `source.words.json` (captions read from it).

Tuning flags: `python3 pipeline/build_edl.py --help`.

## Stage 2 — face tracking

`detect_faces.py` runs MediaPipe's BlazeFace (short range) over every frame.
With several faces it follows the one nearest the previous frame's box.
Smoothing is left to Remotion so the raw data stays inspectable.

`public/media/` and `pipeline/models/` are git-ignored — regenerate them with
the two commands above.
