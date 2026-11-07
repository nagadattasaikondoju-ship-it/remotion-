# Cue sheet for the sound pass, derived from the same word times the graphics use (timeline.json).
# Few sounds, real recordings, only on moments that matter: moves get whooshes, UI events get clicks/pops,
# the two "frame becomes a card" moments get a riser ending on the transition, the payoffs get one hit/chime each.
import json
TL = json.load(open("timeline.json")); WS = [w for w in TL["words"] if w["who"] == "host" and w["t0"] >= TL["T_MAIN"]]
norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
def W(ph, after=0):
    toks = [norm(x) for x in ph.split()]
    for i in range(len(WS)):
        if WS[i]["t0"] < after: continue
        if all(i + j < len(WS) and norm(WS[i + j]["w"]) == tk for j, tk in enumerate(toks)): return WS[i]["t0"], WS[i + len(toks) - 1]["t1"]
    raise SystemExit("missing " + ph)
TS, TM = TL["T_SPLIT"], TL["T_MAIN"]
pa, pg, dec, rd = W("pick the age"), W("pick the gender"), W("decides"), W("it reads")
sh, m, one = W("so here's"), W("we call it"), W("one a problem")
three, angle, method = W("three angle"), W("angle method"), W("method")
two, thr, pain, test, deal = W("two a proof"), W("three an offer"), W("pain"), W("testimonial"), W("deal")
same, tc, mf, aud = W("same product"), W("three completely"), W("meta finds"), W("different audience")
run, cut, win, we = W("run all three"), W("cut the weakest"), W("winner"), W("we tested")
meta, google, leads = W("meta and google"), W("google"), W("leads and sales")
want, dm, dmm = W("want us"), W("dm us"), W("dm us meta")
C = []
def c(t, typ, g, note, **k): C.append(dict(t=round(t, 3), type=typ, g=g, note=note, **k))
c(TS + 0.02, "whoosh", 0.5, "split opens: her clip slides down, he slides into the lower half")
c(TS + 0.30, "click", 0.45, "'paused' tag on the host's half")
c(TM + 0.12, "whoosh", 0.45, "split closes: back to him full screen")
c(pa[0] + 0.02, "pop", 0.55, "audience panel grows in")
c(pa[0] + 0.20, "click", 0.45, "cursor grabs the age slider")
c(pg[0] + 0.42, "click", 0.5, "cursor clicks 'Women'")
c(dec[0] + 0.05, "strike", 0.5, "red strike through 'your targeting' on 'decides'")
c(rd[0] + 0.10, "scan", 0.45, "the scan line reads the ad creative")
c(sh[0] + 0.02, "whoosh", 0.4, "ad card leaves: 'so here's what we do'")
c(m[0] - 1.6, "riser", 0.55, "build into the frame-becomes-card move", len=1.6)
c(m[0] + 0.12, "whoosh", 0.55, "his frame shrinks into a tilted card")
for t_, n in [(three, "01 problem"), (angle, "02 proof"), (method, "03 offer")]: c(t_[0] + 0.06, "pop", 0.55, f"fan card {n}")
c(one[0] - 0.02, "whoosh", 0.5, "frame flies back full, card 01 becomes the lower card")
c(one[0] + 0.02, "hit", 0.4, "low impact under the return (loudest stack of the first half)")
c(pain[0] - 0.08, "type", 0.4, "the pain types itself out", len=0.8)
c(two[0] - 0.02, "pop", 0.45, "card swaps to 02 PROOF")
c(test[0] + 0.05, "pop", 0.45, "testimonial slides up")
c(thr[0] - 0.02, "pop", 0.45, "card swaps to 03 OFFER")
c(deal[0] + 0.02, "stamp", 0.6, "'deal' stamp lands")
c(same[0] - 1.4, "riser", 0.5, "build into the second frame-becomes-card move", len=1.4)
c(same[0] + 0.12, "whoosh", 0.55, "his frame shrinks again; the product box appears")
for i in range(3): c(tc[0] + 0.12 + 0.1 * i, "pop", 0.5, f"one product → ad {i + 1} shoots out")
c(mf[0] - 0.28, "whoosh", 0.5, "frame flies back full")
c(aud[0] + 0.02, "pop", 0.45, "each ad finds its own audience (dots)")
c(run[0] + 0.0, "pop", 0.5, "budget chart in, bars grow")
c(cut[0] + 0.04, "cut", 0.65, "click: the weakest bar is cut (red)")
c(win[0] - 0.18, "win", 0.55, "money moves to the winner (mint bar grows)")
c(we[0] - 0.02, "whoosh", 0.4, "chart leaves: 'we tested this'")
c(meta[0] - 0.02, "pop", 0.5, "Meta chip")
c(google[0] - 0.02, "pop", 0.5, "Google chip")
c(want[0] + 0.22, "pop", 0.45, "DM composer grows in")
c(dm[0] - 0.06, "click", 0.45, "cursor clicks the message field")
c(dm[0] + 0.05, "type", 0.4, "types META", len=max(0.3, dmm[1] - 0.2 - dm[0]))
c(dmm[1] - 0.05, "send", 0.55, "send: META bubble pops")
json.dump(C, open("sfx_cues.json", "w"), indent=1); print(len(C), "cues")
