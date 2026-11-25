"""Key geometry (viewBox 0 0 1000 520): bow = BRIDL360 logo, blade with a skyline-shaped underside, photo bit = Hyderabad skyline."""
import json
S, OX, OY = 0.78, 600, 40          # logo 806-space -> key space
def L(x, y): return (round(OX + (x - 190) * S, 1), round(OY + (y - 142) * S, 1))
def pts(seq): return " ".join(f"{x},{y}" for x, y in seq)
logo_lines = [
  [(190,570),(190,142),(326,212),(194,292),(412,407),(630,294)],
  [(326,212),(410,179),(630,294),(630,568)],
  [(326,212),(326,636)],
  [(511,230),(511,500)],
  [(190,570),(284,620),(511,500),(630,568),(416,684),(326,636)],
]
outline = [(190,142),(326,212),(410,179),(630,294),(630,568),(416,684),(326,636),(326,598),(284,620),(190,570)]
win = [(395,268),(417,268),(395,288),(417,288)]
# skyline profile: (width, height above the base) left->right, Hyderabad-ish mix of towers + a Charminar-like pair of minarets
BASE, X0 = 300, 70
blocks = [(26,10),(34,28),(20,46),(40,18),(14,40),(14,40),(30,24),(44,52),(22,30),(36,14),(18,58),(30,36),(42,22),(24,48),(34,12),(28,34),(40,26),(20,44)]
prof, x = [(X0, BASE)], X0
for w, h in blocks:
    prof += [(x, BASE - h), (x + w, BASE - h)]
    x += w
X1 = x
prof.append((X1, BASE))
# key bitting along the bottom of the photo bit
cuts = [(60,372),(46,398),(58,356),(52,392),(64,366),(48,404),(60,350),(X1 - X0 - 388, 384)]
bottom, cx = [], X0
for w, y in cuts:
    bottom += [(cx + 6, y), (cx + w - 6, y)]
    cx += w
bit = prof + [(X1, bottom[-1][1])] + list(reversed(bottom)) + [(X0, bottom[0][1])]
# blade: tip bevel on the left, underside follows the skyline so the bit interlocks
blade = [(30, 248), (52, 212), (640, 212), (640, 300)] + [(X1 + 4, 300)] + [(px, py) for px, py in reversed(prof[1:-1])] + [(X0 - 4, 300), (52, 300)]
out = {
  "bow": pts([L(*p) for p in outline]),
  "logo": [pts([L(*p) for p in seg]) for seg in logo_lines],
  "win": [[*L(x, y)] for x, y in win], "win_size": round(14 * S, 1),
  "stroke": round(14 * S, 1),
  "blade": pts(blade), "bit": pts(bit), "bit_box": [X0, min(p[1] for p in prof), X1, max(p[1] for p in bottom)],
  "bow_center": [*L(410, 413)],
}
print(json.dumps(out, indent=1))
