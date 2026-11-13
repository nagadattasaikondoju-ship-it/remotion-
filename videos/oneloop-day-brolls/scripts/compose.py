# Paste the cleaned text strip back into each full frame and write the clip's frames to <shot>/final
import os, sys, glob, cv2
D = sys.argv[1]; y0, y1 = int(sys.argv[2]), int(sys.argv[3])
od = os.path.join(D, "final"); os.makedirs(od, exist_ok=True)
for f in sorted(glob.glob(os.path.join(D, "frames", "*.png"))):
    im = cv2.imread(f); c = os.path.join(D, "band_clean", os.path.basename(f))
    if os.path.exists(c): im[y0:y1] = cv2.imread(c)
    cv2.imwrite(os.path.join(od, os.path.basename(f)), im)
