"""Stage 1b: silence + filler detection -> edit-decision list (EDL).

The EDL is a contiguous, non-overlapping cover of the source timeline:
  {"segments": [{"id", "start", "end", "keep", "reason", "text", "review"?}]}
keep:false segments are removed in Remotion. `review` marks things a human
should check (possible retakes, ambiguous "like"); they stay keep:true until
you flip them - either edit the EDL directly, or add entries to an overrides
file ({"cuts": [{"start", "end", "keep", "note"}]}) and re-run this script.
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

HARD_FILLERS = {"um", "uh", "erm", "er", "uhm", "umm", "hmm", "mm", "ah"}
SOFT_FILLERS = {"like"}          # only a filler when isolated by pauses
PHRASE_FILLERS = [("you", "know")]


def norm(w):
    return re.sub(r"[^a-z']", "", w.lower())


def detect_silences(video, noise_db, min_dur):
    p = subprocess.run(
        ["npx", "remotion", "ffmpeg", "-hide_banner", "-i", video, "-vn",
         "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}", "-f", "null", "-"],
        cwd=ROOT, capture_output=True, text=True, check=True)
    out, start = [], None
    for line in p.stderr.splitlines():
        if m := re.search(r"silence_start: ([\d.]+)", line):
            start = float(m.group(1))
        elif (m := re.search(r"silence_end: ([\d.]+)", line)) and start is not None:
            out.append((start, float(m.group(1))))
            start = None
    return out, start  # trailing silence may have no end


def find_fillers(words, gap=0.15):
    cuts = []
    for i, w in enumerate(words):
        t = norm(w["text"])
        prev_gap = w["start"] - words[i - 1]["end"] if i else 1
        next_gap = words[i + 1]["start"] - w["end"] if i + 1 < len(words) else 1
        if t in HARD_FILLERS:
            cuts.append((w["start"], w["end"], "filler", w["text"], None))
        elif t in SOFT_FILLERS:
            isolated = prev_gap >= gap and next_gap >= gap
            if isolated or w["text"].endswith(","):
                cuts.append((w["start"], w["end"], "filler", w["text"], None))
        for a, b in PHRASE_FILLERS:
            if i + 1 < len(words) and t == a and norm(words[i + 1]["text"]) == b:
                cuts.append((w["start"], words[i + 1]["end"], "filler", f"{w['text']} {words[i+1]['text']}", None))
    return cuts


def find_retakes(words, n=3, window=10.0):
    """An n-gram said twice within `window` seconds -> earlier take is a likely false start."""
    flags, toks = [], [norm(w["text"]) for w in words]
    for i in range(len(words) - n + 1):
        gram = toks[i:i + n]
        if not all(gram):
            continue
        for j in range(i + n, len(words) - n + 1):
            if words[j]["start"] - words[i]["start"] > window:
                break
            if toks[j:j + n] == gram:
                flags.append((words[i]["start"], words[j]["start"], "possible retake",
                              " ".join(w["text"] for w in words[i:j]), f"repeats '{' '.join(gram)}'"))
                break
    return flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("words")
    ap.add_argument("out")
    ap.add_argument("--noise-db", type=float, default=-30)
    ap.add_argument("--min-silence", type=float, default=0.3)
    ap.add_argument("--pad-after", type=float, default=0.08, help="keep this much after speech ends")
    ap.add_argument("--pad-before", type=float, default=0.10, help="keep this much before speech starts")
    ap.add_argument("--word-guard", type=float, default=0.03, help="never cut within this margin of a transcribed word")
    ap.add_argument("--min-cut", type=float, default=0.08, help="ignore silence cuts shorter than this")
    ap.add_argument("--overrides", help="JSON {cuts:[{start,end,keep,note}]} applied last")
    a = ap.parse_args()

    tr = json.load(open(a.words))
    words, duration = tr["words"], tr["duration"]

    silences, open_start = detect_silences(a.video, a.noise_db, a.min_silence)
    if open_start is not None:
        silences.append((open_start, duration))

    # (start, end, reason, text, note)
    removals = []
    for s, e in silences:
        s2 = s + (a.pad_after if s > 0.01 else 0)
        e2 = e - (a.pad_before if e < duration - 0.01 else 0)
        if e2 - s2 > 0.05:
            removals.append((s2, e2, "silence", "", f"{e - s:.2f}s silence"))
    fillers = find_fillers(words)

    # Paint the timeline at 1ms resolution: 1 = keep, 0 = cut.
    ms = int(round(duration * 1000))
    keep = bytearray([1]) * ms
    reason = [None] * ms

    def paint(s, e, value, why):
        for t in range(max(0, int(s * 1000)), min(ms, int(e * 1000))):
            keep[t], reason[t] = value, why

    for s, e, why, _, note in removals:
        paint(s, e, 0, (why, note))
    # Quiet words can fall under the silence threshold - never let a silence cut clip a word.
    for w in words:
        paint(w["start"] - a.word_guard, w["end"] + a.word_guard, 1, None)
    for s, e, why, _, note in fillers:
        paint(s, e, 0, (why, note))

    overrides = json.load(open(a.overrides))["cuts"] if a.overrides and os.path.exists(a.overrides) else []
    for o in overrides:
        paint(o["start"], o["end"], 1 if o["keep"] else 0, None if o["keep"] else ("manual", o.get("note")))

    # Drop cuts too short to matter (they'd just add a jump cut).
    t = 0
    while t < ms:
        u = t
        while u < ms and keep[u] == keep[t]:
            u += 1
        if not keep[t] and (u - t) < a.min_cut * 1000 and (reason[t] or ("",))[0] == "silence":
            paint(t / 1000, u / 1000, 1, None)
        t = u

    segs, t = [], 0
    while t < ms:
        u = t
        while u < ms and keep[u] == keep[t] and reason[u] == reason[t]:
            u += 1
        s, e = t / 1000, u / 1000
        seg = {"id": len(segs), "start": s, "end": e, "keep": bool(keep[t]),
               "reason": "speech" if keep[t] else reason[t][0]}
        if not keep[t] and reason[t][1]:
            seg["note"] = reason[t][1]
        seg["text"] = " ".join(w["text"] for w in words
                               if (w["start"] + w["end"]) / 2 >= s and (w["start"] + w["end"]) / 2 < e)
        segs.append(seg)
        t = u

    # Attach retake flags to the kept segments they overlap (never auto-cut).
    retakes = find_retakes(words)
    for s, e, why, text, note in retakes:
        for seg in segs:
            if seg["keep"] and seg["start"] < e and seg["end"] > s:
                seg.setdefault("review", []).append({"type": why, "start": s, "end": e, "text": text, "note": note})

    kept = sum(x["end"] - x["start"] for x in segs if x["keep"])
    out = {
        "source": tr["source"],
        "sourceDuration": duration,
        "keptDuration": round(kept, 3),
        "params": {k: getattr(a, k) for k in ("noise_db", "min_silence", "pad_after", "pad_before", "word_guard", "min_cut")},
        "segments": segs,
    }
    json.dump(out, open(a.out, "w"), indent=1)
    cut = [x for x in segs if not x["keep"]]
    flagged = sum(len(x.get("review", [])) for x in segs)
    print(f"{len(segs)} segments, {len(cut)} cuts, {duration:.2f}s -> {kept:.2f}s, "
          f"{flagged} flagged for review -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
