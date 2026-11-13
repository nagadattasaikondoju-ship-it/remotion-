# The cut: one table drives picture (base_render.py), dialogue (audio.sh) and captions/motion graphics (overlay.html).
#   python3 timeline.py  ->  out/timeline.json
# Times: `in`/`out` are SOURCE seconds; everything in the json is OUTPUT seconds (30 fps).
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("SRC_DIR", "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/build")
FILES = {"skit": f"{SRC}/skit.mp4", "broll": f"{SRC}/broll_0640.mp4", **{f"t{i}": f"{SRC}/clips/t{i}.mp4" for i in range(1, 10)}}
WORDS = {"skit": f"{SRC}/tr/turbo/skit_np.json", **{f"t{i}": f"{SRC}/tr/med/t{i}.json" for i in range(1, 10)}}
# Two short sketch lines are unintelligible (Whisper medium + turbo, raw and cleaned audio, with and without context, all disagree):
# the developer's second line (raw 3.1-4.4 s) and the client's complaint (raw 9.0-10.9 s). They are cut, not guessed.
A1_DUR = 1.70          # 1.15 -> 2.85: "That's about the entire software."
A1_EXTRA, B1_EXTRA = [], []

# face anchors in ORIGINAL source pixels (skit 478x850, Tarun 480x854; base_render scales them for the upscaled files)
DEV_A, CLI_A, PAIR_A = (318, 335), (120, 330), (215, 330)   # shot A: the demo (developer = yellow check, client = blue check)
DEV_B, PAIR_B = (338, 250), (232, 268)                      # shot B: three weeks later, the crash
CLI_C = (132, 152)                                          # shot C: the client calls the manager
TARUN = (187, 228)

# ---- picture: (id, kind, src, in, dur, layout, anchor, zoom keys [(t_local, z)], grade, note) ----
# Part 1 is the sketch IN STORY ORDER, as Tarun asked ("keep it natural, no heavy cuts"): the demo -> 3 weeks later the
# crash -> the client calls the manager. Only dead air is removed; every line is kept in its place.
V = [
 ("co1",  "clip",   "skit", 11.05, 1.20, "full",  DEV_B,  [(0, 1.30), (0.12, 1.30), (0.30, 1.75), (1.2, 1.82)], "warm", "cold open: flash-forward to the crash, punch in on the developer"),
 ("co2",  "black",  None,   0,     1.30, None,    None,   None, None, "black: He had no idea what was coming."),
 ("a1",   "clip",   "skit", 1.15,  A1_DUR, "full", PAIR_A, [(0, 1.00), (A1_DUR, 1.04)], "warm", "THE DEMO: the developer shows the software (wide two-shot, roles labelled)"),
 ("a3",   "clip",   "skit", 5.20,  2.85, "full",  CLI_A,  [(0, 1.30), (2.85, 1.36)], "warm", "cut to the client: The demo looks fine. So you can deploy it. (APPROVED)"),
 ("lat",  "black",  None,   0,     1.15, None,    None,   None, None, "card: 3 weeks later… (Tarun's script: the client said go ahead, three weeks later... this)"),
 ("b",    "clip",   "skit", 10.95, 3.35, "full",  DEV_B,  [(0, 1.05), (0.20, 1.05), (0.42, 1.65), (3.35, 1.72)], "warm", "Deployment failed. Please do something! (quick zoom on the developer) / I'll do something."),
 ("c1",   "clip",   "skit", 15.40, 10.55, "full", CLI_C,  [(0, 1.00), (1.3, 1.00), (3.2, 1.10), (9.45, 1.15), (9.62, 1.32), (10.55, 1.36)], "warm", "the client walks off and calls the manager; punch-in on the punchline"),
 ("frz",  "freeze", "skit", 25.90, 1.37, "full",  CLI_C,  [(0, 1.36), (1.37, 1.40)], "freeze", "freeze + record scratch; Tarun's VO starts over it"),
 ("t1b",  "clip",   "t1",   2.62,  2.83, "full",  TARUN,  [(0, 1.00), (2.83, 1.07)], "cool", "nobody plans to build a software that dies. It happens quietly."),
 ("t1c",  "clip",   "t1",   5.45,  3.65, "split", TARUN,  [(0, 1.00), (3.65, 1.05)], "cool", "split: DEMO panel on top"),
 ("t2a",  "clip",   "broll", 1.50, 1.80, "cover", None,   [(0, 1.00), (1.8, 1.08)], "cool", "b-roll MVI_0640 night traffic: the real world walks in"),
 ("t2b",  "black",  None,   0,     1.05, None,    None,   None, None, "MG: hundreds of people"),
 ("t2c",  "black",  None,   0,     1.20, None,    None,   None, None, "MG: messy data"),
 ("t2d",  "clip",   "t2",   4.65,  2.50, "pip",   TARUN,  None, "cool", "MG: phones on bad networks; Tarun in a circle"),
 ("t3",   "clip",   "t3",   0.55,  4.70, "full",  TARUN,  [(0, 1.00), (4.7, 1.10)], "cool", "one steady shot: build for the wild"),
 ("t4a",  "clip",   "t4",   0.70,  1.60, "full",  TARUN,  [(0, 1.14), (1.6, 1.16)], "cool", "It's not just a talk."),
 ("t4b",  "clip",   "t4",   2.30,  1.80, "pip",   TARUN,  None, "cool", "PROOF 1 Nirvaha, live on Google Play"),
 ("t5",   "clip",   "t5",   0.65,  2.30, "pip",   TARUN,  None, "cool", "PROOF 2 logistics: real vehicles"),
 ("t6",   "clip",   "t6",   0.80,  2.70, "pip",   TARUN,  None, "cool", "PROOF 3 LN Sports Arena: real players"),
 ("t7a",  "clip",   "t7",   0.45,  1.10, "full",  TARUN,  [(0, 1.00), (1.1, 1.03)], "cool", "So, yes,"),
 ("t7b",  "black",  None,   0,     2.70, None,    None,   None, None, "copper slam: we don't build demos / we build software that actually works"),
 ("t9",   "clip",   "t9",   0.70,  3.30, "full",  TARUN,  [(0, 1.04), (3.3, 1.09)], "cool", "Follow OneLoop: the logo lands"),
 ("t8",   "clip",   "t8",   0.75,  2.25, "full",  TARUN,  [(0, 1.10), (2.25, 1.14)], "cool", "Comment BUILD"),
 ("hold", "freeze", "t8",   2.99,  2.00, "full",  TARUN,  [(0, 1.14), (2.0, 1.16)], "hold", "CTA hold 2 s"),
]
CENTRE = {"co1": 1.0, "b": 1.0, "a3": 0.7, "c1": 0.5}  # punch-ins that pull the speaker's face toward the middle of the frame
# ---- dialogue: (src, in, out, at = id of the picture segment it starts in, offset into that segment) ----
A = [
 ("skit", 11.05, 12.25, "co1", 0), ("skit", 1.15, 1.15 + A1_DUR, "a1", 0), ("skit", 5.20, 8.05, "a3", 0),
 ("skit", 10.95, 14.30, "b", 0),                 # one continuous take: "Please do something!", the quick zoom, "I'll do something."
 ("skit", 15.40, 25.95, "c1", 0),                # the whole phone call, pauses and all (the look back at the developer is the joke)
 ("t1", 1.85, 9.10, "frz", 0.60),               # J-cut: "You see," over the freeze, picture cuts to Tarun on "nobody"
 ("t2", 0.60, 7.15, "t2a", 0), ("t3", 0.55, 5.25, "t3", 0), ("t4", 0.70, 4.10, "t4a", 0),
 ("t5", 0.65, 2.95, "t5", 0), ("t6", 0.80, 3.50, "t6", 0), ("t7", 0.45, 4.25, "t7a", 0),
 ("t9", 0.70, 4.00, "t9", 0), ("t8", 0.75, 3.00, "t8", 0),
]
# ---- captions: (src, from, to, text, emphasised words, hint); word times come from Whisper inside [from, to] ----
# The sketch is transcribed with Whisper turbo (tr/turbo/skit_np.json); lines checked against medium and a clean-audio pass.
C = [
 ("skit", 11.08, 12.10, "Please do something!", ["something!"], "co1"),
 ("skit", 1.26, 2.80, "That's about the entire software.", ["software."], None),
 *A1_EXTRA,
 ("skit", 5.30, 6.70, "The demo looks fine.", ["fine."], None), ("skit", 6.76, 8.00, "So you can deploy it.", ["deploy"], None),
 *B1_EXTRA,
 ("skit", 11.08, 12.10, "Please do something!", ["something!"], "b"),
 ("skit", 13.12, 14.10, "I'll do something.", [], "b"),
 ("skit", 16.50, 17.60, "Hey, hi. Listen,", [], None), ("skit", 18.02, 19.66, "the demo is actually good.", ["good."], None),
 ("skit", 19.98, 21.20, "But you know what's the problem?", ["problem?"], None),
 ("skit", 21.28, 22.45, "But it failed in deployment.", ["failed"], None),
 ("skit", 22.80, 23.60, "Can you…", [], None, [23.08, 23.24]),   # word onsets read off the speech envelope (Whisper drifts here)
 ("skit", 24.80, 25.95, "just change the developer, please?", ["developer,"], None, [24.90, 25.04, 25.20, 25.30, 25.72]),
 ("t1", 1.85, 2.55, "You see,", [], None), ("t1", 2.65, 3.56, "nobody plans to build", ["nobody"], None),
 ("t1", 3.56, 4.66, "a software that dies.", ["dies."], None), ("t1", 4.66, 5.45, "It happens quietly.", ["quietly."], None),
 ("t1", 5.55, 6.20, "In the demo,", ["demo,"], None), ("t1", 6.30, 7.20, "the data is clean.", ["clean."], None),
 ("t1", 7.40, 8.02, "there is one user", ["one", "user"], None), ("t1", 8.02, 9.08, "and the Wi-Fi is perfect.", ["perfect."], None),
 ("t2", 0.65, 1.76, "Then the real world", ["real", "world"], None), ("t2", 1.76, 2.40, "walks in.", [], None),
 ("t2", 2.55, 3.45, "Hundreds of people,", ["Hundreds"], None), ("t2", 3.48, 4.60, "lots of messy data,", ["messy"], None),
 ("t2", 4.70, 5.86, "phones on bad networks", ["bad", "networks"], None), ("t2", 5.86, 7.10, "in the middle of nowhere.", ["nowhere."], None),
 ("t3", 0.62, 1.84, "We've watched this story", [], None), ("t3", 1.84, 2.80, "too many times.", ["too", "many"], None),
 ("t3", 2.88, 3.58, "So at OneLoop,", ["OneLoop,"], None), ("t3", 3.58, 4.44, "we build for the wild", ["wild"], None),
 ("t3", 4.44, 5.25, "from day one.", ["day", "one."], None),
 ("t4", 0.74, 2.30, "It's not just a talk.", ["talk."], None), ("t4", 2.40, 3.08, "A wellness app,", ["wellness"], None),
 ("t4", 3.08, 4.08, "live on Play Store.", ["Play", "Store."], None),
 ("t5", 0.70, 1.72, "A logistics system", ["logistics"], None), ("t5", 1.72, 2.92, "tracking real vehicles.", ["real", "vehicles."], None),
 ("t6", 0.82, 1.46, "A booking app", ["booking"], None), ("t6", 1.46, 2.52, "handling real players", ["real", "players"], None),
 ("t6", 2.52, 3.48, "every single day.", ["every", "single", "day."], None),
 ("t7", 0.46, 1.58, "So, yes,", [], None),
 ("t9", 0.76, 1.70, "Follow OneLoop", ["OneLoop"], None), ("t9", 1.70, 2.80, "for more such content", [], None),
 ("t9", 2.80, 3.95, "on tech and business.", ["tech", "business."], None),
]

def load_words(k):
    d = json.load(open(WORDS[k]))
    return [(w["start"], w["end"], w["word"].strip()) for s in d["segments"] for w in s.get("words", [])]

def main():
    seg, t = {}, 0.0
    out = {"fps": 30, "segments": [], "audio": [], "captions": [], "files": FILES}
    for sid, kind, src, i, dur, layout, anchor, zk, grade, note in V:
        seg[sid] = t
        out["segments"].append({"id": sid, "kind": kind, "src": src, "in": i, "dur": dur, "start": round(t, 4), "layout": layout,
                                "anchor": anchor, "zoom": zk, "grade": grade, "note": note, "centre": CENTRE.get(sid, 0.0)})
        t += dur
    out["duration"] = round(t, 4)
    amap = []  # (src, in, out, out_start)
    for src, i, o, at, off in A:
        s = seg[at] + off; amap.append((src, i, o, s)); out["audio"].append({"src": src, "in": i, "out": o, "start": round(s, 4)})
    def to_out(src, x, hint):
        for s, i, o, st in amap:
            if s == src and i - 0.02 <= x <= o + 0.02 and (hint is None or abs(st - seg[hint]) < 1e-6): return st + (x - i)
        return None
    words = {k: load_words(k) for k in WORDS}
    for src, a, b, text, emph, hint, *fixed in C:
        toks = text.split(); ws = [w for w in words[src] if a - 0.05 <= w[0] < b]
        if fixed: ws = [(x, x, tk) for x, tk in zip(fixed[0], toks)]
        if src in ("t5", "t6"): ws = [w for w in ws if w[0] > 0.3]  # Whisper pins the first word at 0.00; the onset is later
        if len(ws) == len(toks): times = [max(a, w[0]) for w in ws]
        else:  # Whisper split/merged words differently: spread the corrected words over the spoken span
            s0 = ws[0][0] if ws else a; s1 = ws[-1][0] if ws else b - 0.3
            times = [s0 + (s1 - s0) * k / max(1, len(toks) - 1) for k in range(len(toks))]
        o0 = to_out(src, a + 0.03, hint); o1 = to_out(src, min(b, max(times) + 0.6), hint) or to_out(src, b - 0.03, hint)
        ow = [to_out(src, max(x, a + 0.03), hint) for x in times]
        if o0 is None or None in ow: raise SystemExit(f"caption outside the cut: {text}")
        out["captions"].append({"text": text, "words": [{"w": w, "t": round(x, 3), "e": w in emph} for w, x in zip(toks, ow)],
                                "start": round(min(ow) - 0.04, 3), "end": round(o1, 3)})
    caps = out["captions"]  # a caption ends when the next one starts (no overlap), and never lingers > 0.5 s after its last word
    for c, n in zip(caps, caps[1:]): c["end"] = round(min(c["end"], n["start"]), 3)
    out["marks"] = {sid: seg[sid] for sid in seg}
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "out", "timeline.json"), "w"), indent=1)
    print(f"duration {t:.2f}s, {len(V)} shots, {len(A)} dialogue pieces, {len(caps)} captions")
    for s in out["segments"]: print(f"  {s['start']:6.2f}  {s['id']:5s} {s['dur']:5.2f}  {s['note']}")

if __name__ == "__main__": main()
