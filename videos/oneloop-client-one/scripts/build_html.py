"""Generate index.html from scripts/template.html + the overlay timings in edl.py.

Run: python3 scripts/build_html.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import CAPS, OVER, TOTAL  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
D = {
    "total": TOTAL,
    "paper": [round(x, 4) for x in OVER["paper"]],
    "pay": [round(x, 4) for x in OVER["pay"]],
    "notpub": [round(x, 4) for x in OVER["notpub"]],
    "flash": [round(x, 4) for x in OVER["flash"]],
    "caps": [{"sm": s, "kw": k, "t0": round(a, 4), "t1": round(b, 4), "pos": p} for s, k, a, b, p in CAPS],
}
tpl = open(os.path.join(HERE, "template.html")).read()
html = tpl.replace("%%DATA%%", json.dumps(D, ensure_ascii=False)).replace("%%TOTAL%%", f"{TOTAL:.4f}")
open(os.path.join(HERE, "..", "index.html"), "w").write(html)
print(json.dumps(D, ensure_ascii=False, indent=1))
