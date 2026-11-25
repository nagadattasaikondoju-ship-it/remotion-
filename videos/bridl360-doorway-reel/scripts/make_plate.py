"""Full-frame 1080x1920 plate from the BRIDL360 'Sri Hemadurga Siva Hills' carousel image, with its burned-in
title, details, logo, URL and page number removed. The towers fill the middle of the frame, where the key's
building slices line up."""
import cv2, numpy as np, os
D = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
src = cv2.cvtColor(np.array(__import__("PIL.Image", fromlist=["Image"]).open(os.path.join(D, "siva-hills-src.webp")).convert("RGB")), cv2.COLOR_RGB2BGR)
H, W = src.shape[:2]
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
bright = (hsv[..., 2] > 165) & (hsv[..., 1] < 70)
mask = np.zeros((H, W), np.uint8)
top = np.zeros_like(bright); top[40:515, 140:885] = True          # title, pin, details, rule, tagline
bot = np.zeros_like(bright); bot[1235:1375, 380:1075] = True       # logo, wordmark, URL, "| 06"
mask[(top | bot) & bright] = 255
mask = cv2.dilate(mask, np.ones((7, 7), np.uint8), iterations=2)
clean = cv2.inpaint(src, mask, 12, cv2.INPAINT_TELEA)
soft = cv2.GaussianBlur(mask, (0, 0), 9).astype(np.float32)[..., None] / 255.0
clean = (clean * (1 - soft) + cv2.GaussianBlur(clean, (0, 0), 12) * soft).astype(np.uint8)
cv2.imwrite(os.path.join(D, "_siva_clean.jpg"), clean, [cv2.IMWRITE_JPEG_QUALITY, 92])
S = 1920 / H
big = cv2.resize(clean, (round(W * S), 1920), interpolation=cv2.INTER_LANCZOS4)
big = cv2.addWeighted(big, 1.3, cv2.GaussianBlur(big, (0, 0), 1.1), -0.3, 0)
x0 = (big.shape[1] - 1080) // 2
cv2.imwrite(os.path.join(D, "plate.jpg"), big[:, x0:x0 + 1080], [cv2.IMWRITE_JPEG_QUALITY, 93])
print("scale", S, "x0", x0)
