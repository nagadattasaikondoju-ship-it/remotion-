"""Full-frame 1080x1920 plate from the BRIDL360 carousel photo with every burned-in word removed."""
import cv2, numpy as np, os
D = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
src = cv2.imread(os.path.join(D, "carousel-src.png"))
H, W = src.shape[:2]
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
bright = (hsv[..., 2] > 170) & (hsv[..., 1] < 80)
mask = np.zeros((H, W), np.uint8)
mask[:625][bright[:625]] = 255                         # sky: series title, headline, subline
band = np.zeros_like(bright); band[1150:1335, 360:1100] = True   # logo, wordmark, URL, "| 01"
mask[band & bright] = 255
mask = cv2.dilate(mask, np.ones((9, 9), np.uint8), iterations=2)
clean = cv2.inpaint(src, mask, 14, cv2.INPAINT_TELEA)
soft = cv2.GaussianBlur(mask, (0, 0), 10).astype(np.float32)[..., None] / 255.0
sky_blur = cv2.GaussianBlur(clean, (0, 0), 14)
clean = (clean * (1 - soft) + sky_blur * soft).astype(np.uint8)
s = 1920 / H
big = cv2.resize(clean, (round(W * s), 1920), interpolation=cv2.INTER_LANCZOS4)
g = cv2.GaussianBlur(big, (0, 0), 1.1)
big = cv2.addWeighted(big, 1.3, g, -0.3, 0)
x0 = 150
cv2.imwrite(os.path.join(D, "plate.jpg"), big[:, x0:x0 + 1080], [cv2.IMWRITE_JPEG_QUALITY, 93])
print("scale", s, "width", big.shape[1])
