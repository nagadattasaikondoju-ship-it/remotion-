# Crop each shot's frames + masks to the strip that holds the text (full width, full resolution) for inpainting.
import os, sys, glob, cv2
W = sys.argv[1]
BANDS = {"01": (600, 1304)}            # title shot; all timestamp captions sit in y 296–800
for d in sorted(glob.glob(os.path.join(W, "*/"))):
    name = os.path.basename(d.rstrip("/"))
    if name.startswith(("02", "03")): continue
    y0, y1 = BANDS.get(name[:2], (296, 800))
    for sub in ("frames", "masks"):
        od = os.path.join(d, "band_" + sub); os.makedirs(od, exist_ok=True)
        for f in sorted(glob.glob(os.path.join(d, sub, "*.png"))):
            im = cv2.imread(f, cv2.IMREAD_UNCHANGED); cv2.imwrite(os.path.join(od, os.path.basename(f)), im[y0:y1])
    print(name, y0, y1)
