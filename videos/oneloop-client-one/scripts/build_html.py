"""Generate index.html (+ assets/cut/ranges.json for the speaker cut-outs) from template.html,
the caption map (captions.py), the EDL and the measured faces / surface tracks (assets/track.json).

Run: python3 scripts/build_html.py
Writes CAPTION_MAP.md: every card with its exact text, timing, mode and tracking.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from captions import CARDS, END_CARD  # noqa: E402
from edl import FLASHCUTS, FPS, MATCH_PAGES, OVER, TOTAL, TOTAL_F, T  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
W, H = 1080, 1920
SAFE_TOP, SAFE_L, SAFE_R = 250, 50, 1030
TR = json.load(open(os.path.join(ROOT, "assets", "track.json")))
FACES = {int(k): v for k, v in TR["faces"].items()}
PIECES = TR["pieces"]  # [f0, f1, src, src_in]
PLANES = {int(k): v for k, v in TR["planes"].items()}
AROLL = {"0647", "0658", "0662", "VID"}

# ---------- exact text widths from the font files ----------
FONTS = {}
for key, fn in {"main": "Montserrat-normal-900.ttf", "sm": "Montserrat-normal-800.ttf",
                "kw": "PlayfairDisplay-italic-600.ttf"}.items():
    f = TTFont(os.path.join(ROOT, "assets", "fonts", fn))
    FONTS[key] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
SPACING = {"main": -0.012, "sm": 0.02, "kw": -0.01}
LH = {"main": 0.98, "sm": 0.98, "kw": 1.04}


def width(text, cls, size):
    cmap, hmtx, upm = FONTS[cls]
    t = text if cls == "kw" else text.upper()
    adv = sum(hmtx[cmap.get(ord(ch), cmap.get(32))][0] for ch in t)
    return adv / upm * size + SPACING[cls] * size * len(t)


def piece_at(f):
    for k, p in enumerate(PIECES):
        if p[0] <= f < p[1]:
            return k
    return len(PIECES) - 1


def shot_span(f):
    """[start, end) of the run of pieces from the same camera source around frame f (A-roll merges J/whip)"""
    k = piece_at(f)
    src = PIECES[k][2]
    a, b = k, k
    while a > 0 and PIECES[a - 1][2] == src and PIECES[a - 1][1] == PIECES[a][0]:
        a -= 1
    while b + 1 < len(PIECES) and PIECES[b + 1][2] == src and PIECES[b + 1][0] == PIECES[b][1]:
        b += 1
    return PIECES[a][0], PIECES[b][1], src


# picture changes = where the camera source changes (J-cut carry-overs and whip frames are not cuts)
cuts = sorted(PIECES[k][0] for k in range(1, len(PIECES)) if PIECES[k][2] != PIECES[k - 1][2])

# ---------- timing ----------
cards = []
for i, (seg, a, b, lines, mode, o) in enumerate(CARDS):
    t0 = T(seg, a) - 0.04
    if o.get("start_at_picture"):
        near = [c / FPS for c in cuts if T(seg, a) - 0.05 <= c / FPS <= T(seg, a) + 0.35]
        t0 = max(t0, near[0]) if near else t0
    if o.get("start_at"):
        t0 = max(t0, OVER[o["start_at"]][0])
    if mode == "env":  # an environment caption belongs to its shot: snap onto a picture cut just after the word
        near = [c / FPS for c in cuts if t0 < c / FPS <= t0 + 0.15]
        t0 = near[0] if near else t0
    cards.append({"i": i, "seg": seg, "a": a, "b": b, "lines": lines, "mode": mode, "o": o,
                  "t0": round(t0, 4), "speech": (T(seg, a), T(seg, b))})
for k, c in enumerate(cards):
    end_speech = c["speech"][1]
    nxt = cards[k + 1]["t0"] if k + 1 < len(cards) else OVER["end"][0]
    t1 = nxt if nxt - end_speech <= 0.6 else end_speech + 0.30
    if c["o"].get("hold_to"):
        t1 = OVER[c["o"]["hold_to"]][0]
    f0 = round(c["t0"] * FPS)
    if c["mode"] in ("behind", "env"):  # never carry a placed caption into a different shot
        s0, s1, src = shot_span(f0)
        if c["mode"] == "env" and k + 1 < len(cards) and cards[k + 1]["mode"] == "env":
            s1 = max(s1, round(nxt * FPS))
        t1 = min(t1, s1 / FPS)
    c["t1"] = round(min(t1, TOTAL), 4)
end_t0 = round(cards[-1]["t1"], 4)

# ---------- layout ----------
def fit(lines, maxw, cap):
    """font sizes per line: main lines fill maxw up to cap; support lines ~45 %, keyword lines ~115 %"""
    main = [t for t, c in lines if c == ""] or [t for t, c in lines]
    s_main = min(cap, min(maxw / max(1, width(re.sub(r"[\[\]]", "", t), "main", 1)) for t in main))
    out = []
    for t, c in lines:
        cls = c or "main"
        plain = re.sub(r"[\[\]]", "", t)
        want = {"main": s_main, "sm": max(44, 0.46 * s_main), "kw": 1.18 * s_main}[cls]
        size = min(want, maxw / max(1, width(plain, cls, 1)))
        out.append((t, cls, round(size, 1)))
    return out


def block_h(sized):
    return sum(s * LH[c] for _, c, s in sized)


def face_stats(f0, f1):
    pts = [FACES[f] for f in range(f0, f1) if f in FACES]
    return np.median(np.array(pts), 0) if pts else None


def cut_for(f0, f1):
    for fn in os.listdir(os.path.join(ROOT, "assets", "cut")):
        m = re.match(r"cut_(\d+)_(\d+)\.webm$", fn)
        if m and int(m.group(1)) <= f0 and f1 <= int(m.group(2)):
            return os.path.join(ROOT, "assets", "cut", fn), int(m.group(1))
    return None, None


def person_top(f0, f1, cx, fw, cy=None):
    """top of the speaker's head (hair included), traced upward from the face through the connected
    silhouette in the cut-out alpha (ignores trees / walls the segmenter may catch); None if not cut yet"""
    path, a = cut_for(f0, f1)
    if not path:
        return None
    tops = []
    for f in sorted({f0, (f0 + f1) // 2, f1 - 1}):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", path, "-vf",
                              f"select=eq(n\\,{f - a}),alphaextract,scale=540:960", "-frames:v", "1", "-f", "rawvideo",
                              "-pix_fmt", "gray", "-"], capture_output=True).stdout
        if len(raw) < 540 * 960:
            continue
        al = np.frombuffer(raw[:540 * 960], np.uint8).reshape(960, 540)
        x0, x1 = int(max(0, (cx - 0.5 * fw) / 2)), int(min(540, (cx + 0.5 * fw) / 2))
        cov = (al[:, x0:x1] > 128).mean(1)
        r = int((cy if cy is not None else 0) / 2)
        miss = 0
        while r > 0 and miss < 3:
            r -= 1
            miss = miss + 1 if cov[r] < 0.12 else 0
        t = (r + 3) * 2
        if cy is not None and not (cy - 1.25 * fw <= t <= cy - 0.7 * fw):
            t = int(cy - 1.0 * fw)  # silhouette merged with a tree / wall behind the head: use the face geometry
        tops.append(t)
    return min(tops) if tops else None


def html_line(t, cls):
    return re.sub(r"\[(.+?)\]", r'<span class="k">\1</span>', t)


out_caps, cmap_rows, behind_ranges = [], [], []
for c in cards:
    o = c["o"]
    f0, f1 = round(c["t0"] * FPS), round(c["t1"] * FPS)
    mode = c["mode"]
    layer = {"behind": "behind", "upper": "front", "env": "front", "lower": "front", "top": "top"}[mode]
    scheme = o.get("scheme", "light")
    track, t3d, note = None, o.get("t3d"), ""
    if mode == "behind":
        behind_ranges.append((f0, f1))  # authored behind-cards always get a speaker cut-out
        fs = face_stats(f0, f1)
        sized = fit(c["lines"], SAFE_R - SAFE_L - 40, o.get("size", 150))
        hb = block_h(sized)
        cx, cy, fw = fs
        top = person_top(f0, f1, cx, fw, cy)
        # only the foot of the last line tucks behind the hair; the words stay readable
        # the main line tucks a quarter of its height behind the top of the head; every word stays readable
        bottom = (top + 0.25 * sized[-1][2]) if top is not None else cy - 1.0 * fw
        dbg = f"top={top} bottom={bottom:.0f} hb={hb:.0f}"
        if bottom - hb < SAFE_TOP:  # shrink to fit the space above the head
            k = (bottom - SAFE_TOP) / hb
            if k < 0.55:
                mode, layer = "lower", "front"
                note = f"behind did not fit ({dbg}) → "
            else:
                sized = [(t, cl, round(s * k, 1)) for t, cl, s in sized]
                hb = block_h(sized)
        if mode == "behind":
            bw = max(width(re.sub(r"[\[\]]", "", t), cl, s) for t, cl, s in sized)
            x = float(np.clip(cx, SAFE_L + bw / 2, SAFE_R - bw / 2))
            y = bottom - hb / 2
            note = f"behind head (face {cx:.0f},{cy:.0f}); person roto-masked in front"
            # moving speaker (selfie): damped follow of the head, 55 % of its motion, critically smoothed
            src = PIECES[piece_at(f0)][2]
            if src == "VID" and PIECES[piece_at(f0)][3] >= 9.9:
                track, sx, sy = [], 0.0, 0.0
                base = FACES.get(f0) or [cx, cy, fw]
                for f in range(f0, f1):
                    fc = FACES.get(f, base)
                    sx += 0.18 * (0.55 * (fc[0] - base[0]) - sx)
                    sy += 0.18 * (0.55 * (fc[1] - base[1]) - sy)
                    track.append([f, round(sx, 1), round(sy, 1), 1, 0])
                note += "; damped head-follow (55 %, smoothed)"
            else:
                note += "; locked (tripod shot)"
    if mode == "upper":
        # the regular phrase: clean, in the open space above the speaker's head, in front of the background
        fs = face_stats(f0, f1)
        cx, cy, fw = fs
        sized = fit(c["lines"], o.get("maxw", 900), o.get("size", 104))
        hb = block_h(sized)
        top = person_top(f0, f1, cx, fw, cy)
        bottom = (top if top is not None else cy - 1.0 * fw) - 30
        if bottom - hb < SAFE_TOP:
            k = (bottom - SAFE_TOP) / hb
            if k < 0.6:
                mode, layer = "lower", "front"
                note = f"upper did not fit (top={top} bottom={bottom:.0f} hb={hb:.0f}) → "
            else:
                sized = [(t, cl, round(s * k, 1)) for t, cl, s in sized]
                hb = block_h(sized)
        if mode == "upper":
            bw = max(width(re.sub(r"[\[\]]", "", t), cl, s) for t, cl, s in sized)
            x = float(np.clip(540 + 0.35 * (cx - 540), SAFE_L + bw / 2, SAFE_R - bw / 2))
            y = bottom - hb / 2
            note = "clean phrase in the open space above the head (front, never touches face/hands)"
    if mode == "lower":
        sized = fit(c["lines"], o.get("maxw", 860), o.get("size", 96))
        x, y = o.get("x", 540), o.get("y", 1440)
        note = note + "clean lower phrase"
    if mode == "top":
        sized = fit(c["lines"], o.get("maxw", 900), o.get("size", 110))
        x, y = 540, o.get("y", 330) + block_h(sized) / 2
        note = "above the proof screen, never on it"
    if mode == "env":
        sized = fit(c["lines"], o.get("maxw", 880), o.get("size", 124))
        x, y = o["x"], o["y"]
        k = piece_at(f0)
        couple = o.get("couple", 1.0)
        if k in PLANES:
            pl = PLANES[k]
            M = [np.vstack([np.array(m).reshape(2, 3), [0, 0, 1]]) for m in pl["m"]]
            Ms_inv = np.linalg.inv(M[f0 - pl["f0"]])
            track = []
            for f in range(f0, min(f1, pl["f1"])):
                R = M[f - pl["f0"]] @ Ms_inv
                px, py = (R @ [x, y, 1])[:2]
                s = float(np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2))
                rot = float(np.degrees(np.arctan2(R[1, 0], R[0, 0])))
                track.append([f, round((px - x) * couple, 1), round((py - y) * couple, 1),
                              round(1 + (s - 1) * couple, 4), round(rot * couple, 2)])
            note = (f"pinned to {PIECES[k][2]} surface, planar track"
                    + (f" damped to {int(couple * 100)} % (fast camera move)" if couple < 1 else ""))
        if t3d:
            note += f"; surface angle {t3d.split(') ')[-1]}"
    out_caps.append({
        "layer": layer, "mode": mode, "scheme": scheme, "x": round(x, 1), "y": round(y, 1), "t3d": t3d,
        "t0": c["t0"], "t1": c["t1"], "emph": bool(o.get("emph")), "track": track,
        "lines": [{"html": html_line(t, cl), "cls": "" if cl == "main" else cl, "size": s} for t, cl, s in sized],
    })
    text = " / ".join(re.sub(r"[\[\]]", "", t) for t, _ in c["lines"])
    cmap_rows.append((c["t0"], c["t1"], c["speech"], text, mode, note))

# end card: "Next in Part 2" — the call to action stays fully readable: in front, above the held face, gentle rise
fs = face_stats(round(OVER["end"][0] * FPS), TOTAL_F)
sized = fit(END_CARD, 820, 120)
# the held selfie fills the top of the frame, so the lockup sits low on the shirt, clear of the face
y_end = 1560
out_caps.append({"layer": "front", "mode": "end", "scheme": "light", "x": 540,
                 "y": y_end, "t3d": None, "t0": end_t0, "t1": TOTAL, "emph": False,
                 "gentle": True, "track": None,
                 "lines": [{"html": html_line(t, cl), "cls": "" if cl == "main" else cl, "size": s} for t, cl, s in sized]})
cmap_rows.append((end_t0, TOTAL, None, "Next in / Part 2", "end card (front)",
                  "low on the held frame (the face fills the top), gentle opacity rise — the CTA is never hidden"))

# ---------- speaker cut-out ranges (merged, padded) ----------
rs = sorted((max(0, a - 3), min(TOTAL_F, b + 3)) for a, b in behind_ranges)
merged = []
for a, b in rs:
    if merged and a <= merged[-1][1] + 6:
        merged[-1][1] = max(merged[-1][1], b)
    else:
        merged.append([a, b])
os.makedirs(os.path.join(ROOT, "assets", "cut"), exist_ok=True)
tags, missing, used = [], [], set()
for a, b in merged:  # reuse any existing cut-out that covers the range; list the rest for make_cutouts.py
    path, start = cut_for(a, b)
    if path is None:
        missing.append([a, b])
        continue
    if path in used:
        continue
    used.add(path)
    m = re.match(r"cut_(\d+)_(\d+)\.webm$", os.path.basename(path))
    a0, b0 = int(m.group(1)), int(m.group(2))
    tags.append(f'      <video id="cut{a0}" class="full" src="assets/cut/{os.path.basename(path)}" data-start="{a0 / FPS:.4f}" '
                f'data-duration="{(b0 - a0) / FPS:.4f}" data-media-start="0" data-track-index="{2 + len(tags) % 2}" '
                f'muted playsinline></video>')
json.dump(missing, open(os.path.join(ROOT, "assets", "cut", "ranges.json"), "w"))

# ---------- newspaper page 2 columns (abstract text bars, no invented copy) ----------
def cols(n_rows, seed):
    r = np.random.default_rng(seed)
    return "".join("<div>" + "".join(f'<div class="bar" style="width:{int(r.uniform(62, 100))}%"></div>'
                                     for _ in range(n_rows)) + "</div>" for _ in range(3))


logo_w = 900
D = {
    "total": TOTAL, "caps": out_caps, "paper": list(OVER["paper"]), "pages": MATCH_PAGES,
    "pay": list(OVER["pay"]), "notpub": list(OVER["notpub"]),
    "flashcuts": [[round(t, 4), k, lvl] for t, k, lvl, _ in FLASHCUTS],
    # logo wordmark centre lands on the same screen point as every page's "OneLoop" (y 820)
    "logo": {"x": 70 + (W - logo_w) / 2, "y": 30 + 820 - 532 * logo_w / 1034},
}
tpl = open(os.path.join(HERE, "template.html")).read()
html = (tpl.replace("%%DATA%%", json.dumps(D, ensure_ascii=False)).replace("%%TOTAL%%", f"{TOTAL:.4f}")
        .replace("%%CUTOUTS%%", "\n".join(tags)).replace("%%COLS1%%", cols(16, 3)).replace("%%COLS2%%", cols(30, 5)))
open(os.path.join(ROOT, "index.html"), "w").write(html)

# ---------- caption map + coverage ----------
md = ["# Caption map — One Loop \"Client #1\"", "",
      "Timeline seconds. Every spoken phrase has a card; gaps are measured against the speech.", "",
      "| # | on screen | speech | caption text | mode | placement / tracking |", "|---|---|---|---|---|---|"]
for k, (t0, t1, sp, text, mode, note) in enumerate(cmap_rows):
    sps = f"{sp[0]:.2f}–{sp[1]:.2f}" if sp else "—"
    md.append(f"| {k + 1} | {t0:.2f}–{t1:.2f} | {sps} | {text} | {mode} | {note} |")
md.append("")
md.append("**Match cut (3.20–4.30):** \"…we had just started One Loop…\" is carried by the newspaper pages — every page's "
          "highlighted line reads \"…just started **OneLoop**…\", ending on the One Loop logo card.")
open(os.path.join(ROOT, "CAPTION_MAP.md"), "w").write("\n".join(md) + "\n")

# uncovered speech check: any spoken instant with no caption (and not the match cut) for > 0.35 s
cover = np.zeros(TOTAL_F, bool)
for c in out_caps:
    cover[round(c["t0"] * FPS):round(c["t1"] * FPS)] = True
cover[round(OVER["paper"][0] * FPS):round(OVER["paper"][1] * FPS)] = True
words = json.load(open(os.path.join(HERE, "..", "assets", "words_timeline.json")))
gaps = []
for w, a, b in words:
    fa, fb = round(a * FPS), round(b * FPS)
    miss = (~cover[fa:fb]).sum()
    if miss > 0.35 * FPS:
        gaps.append((w, a, b, miss))
modes = {}
for c in out_caps:
    modes[c["mode"]] = modes.get(c["mode"], 0) + 1
print(f"{len(out_caps)} cards {modes}; cut-outs used {len(tags)}, still to cut {missing}; "
      f"uncovered words > 0.35 s: {gaps}")

