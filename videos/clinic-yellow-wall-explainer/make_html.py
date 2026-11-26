"""explainer.html = the shared flat-2D engine (helpers, palette, Riya/kulfi/doctor, the tooth cross-section, brushes) from
../sushma-sensitivity-explainer/explainer.html + this film's characters and scenes (scenes.js). Gum colours are made settable
(st.gumA / st.gumB) for inflamed gums. Re-run after editing scenes.js."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
src = open("../sushma-sensitivity-explainer/explainer.html").read()
head = src[:src.index("// ---------- scenes ----------")]
head = re.sub(r"<!-- \"The Ice Cream Betrayal\".*?-->", """<!-- "Chai, Gutkha and the Yellow Wall": a flat 2D explainer on tobacco, stains and gum disease for the dental clinic
     (non-judgemental; no doctor's name is spoken). Pure function of time: seek(t). Beats follow the narration's word times (timeline.js).
     Built by make_html.py from the shared engine of ../sushma-sensitivity-explainer + scenes.js. -->""", head, flags=re.S)
head = head.replace("const TEND = 36.5;", "const TEND = 33.7;")
k0, k1 = head.index("const K = {"), head.index("window.KEYS = K;")
head = head[:k0] + """const K = {
  smile: WT(1, 'smile'), year: WT(1, 'year'), gums: WT(2, 'gums'),
  chai: WT(3, 'chai'), cig: WT(3, 'cigarette'), gutka: WT(3, 'gutka'),
  drew0: LS(4), drew: WT(4, 'drew'), brown: WT(4, 'brown'),
  but: LS(5), worse: WT(5, 'worse'),
  tartar: LS(6), germs: WT(6, 'germs'), tobacco: WT(6, 'tobacco'),
  attack: WT(7, 'attack'), pull: WT(7, 'pull'),
  bone: WT(8, 'bone'), away: WT(8, 'away'),
  clinic0: LS(9), deep: WT(9, 'deep'), stains: WT(9, 'stains'),
  gumcare: LS(10), heal: WT(10, 'heal'), team: WT(10, 'team'), quit: WT(10, 'quit'), step: WT(10, 'step'),
  again0: LS(11), cta: LS(12)
};
""" + head[k1:]
head = head.replace("X.fillStyle = grad(gy - 30, gy + 260, [[0, P.gum], [1, P.gumD]]); X.fill();", "X.fillStyle = grad(gy - 30, gy + 260, [[0, st.gumA || P.gum], [1, st.gumB || P.gumD]]); X.fill();")
open("explainer.html", "w").write(head + open("scenes.js").read())
print("explainer.html written")
