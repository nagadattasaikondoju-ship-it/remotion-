"""Derived plates: a soft 'vision' plot for the build scene and a clean landscape Hyderabad skyline for the end card."""
import cv2, numpy as np, os
D = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
b = cv2.imread(os.path.join(D, "build.jpg"))
soft = cv2.GaussianBlur(b, (0, 0), 22)
gray = cv2.cvtColor(soft, cv2.COLOR_BGR2GRAY)[..., None].repeat(3, 2)
soft = cv2.addWeighted(soft, 0.55, gray, 0.45, 12)
cv2.imwrite(os.path.join(D, "build-plot.jpg"), soft, [cv2.IMWRITE_JPEG_QUALITY, 90])
# Hyderabad skyline, burned-in text removed (same recipe as the doorway reel), landscape 16:9 crop
src = cv2.imread(os.path.join(D, "carousel-src.png")); H, W = src.shape[:2]
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
bright = (hsv[..., 2] > 170) & (hsv[..., 1] < 80)
mask = np.zeros((H, W), np.uint8); mask[:625][bright[:625]] = 255
band = np.zeros_like(bright); band[1150:1335, 360:1100] = True; mask[band & bright] = 255
mask = cv2.dilate(mask, np.ones((9, 9), np.uint8), iterations=2)
clean = cv2.inpaint(src, mask, 14, cv2.INPAINT_TELEA)
crop = clean[520:520 + 631, 0:1122]
big = cv2.resize(crop, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite(os.path.join(D, "hyd-wide.jpg"), big, [cv2.IMWRITE_JPEG_QUALITY, 92])
cv2.imwrite(os.path.join(D, "hyd-wide-soft.jpg"), cv2.GaussianBlur(big, (0, 0), 10), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("ok")
