"""Privacy-safe stills for the reel.

- payment-1500: the real PhonePe receipt with every personal/client field pixelated + blurred
  (payee name, account numbers, banking name, transaction ID, payer bank logo, UTR).
- not-published: the supplied "Webpage not available" illustration, cropped to the icon + message.
- logo: the One Loop logo lockup cropped from the supplied square.
Run: python3 scripts/prep_stills.py
"""
import os
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "sources")
OUT = os.path.join(HERE, "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)


def redact(im, box, cell=30, radius=14):
    r = im.crop(box)
    w, h = r.size
    r = r.resize((max(1, w // cell), max(1, h // cell)), Image.BILINEAR).resize((w, h), Image.NEAREST)
    im.paste(r.filter(ImageFilter.GaussianBlur(radius)), box)


pay = Image.open(os.path.join(SRC, "payment-1500.png")).convert("RGB")
for box in [
    (215, 305, 845, 372),   # payee name
    (215, 375, 560, 430),   # payee account
    (395, 505, 840, 565),   # banking name
    (60, 805, 620, 875),    # transaction ID
    (60, 960, 165, 1060),   # payer bank logo
    (215, 975, 600, 1050),  # payer account
    (215, 1075, 660, 1135), # UTR
]:
    redact(pay, box)
pay.save(os.path.join(OUT, "payment-1500.png"))

err = Image.open(os.path.join(SRC, "not-published.png")).convert("RGB")
err.crop((292, 118, 732, 394)).save(os.path.join(OUT, "not-published.png"))

logo = Image.open(os.path.join(SRC, "oneloop-logo.png")).convert("RGB")
logo.crop((110, 270, 1144, 980)).save(os.path.join(OUT, "logo.png"))
print("ok")
