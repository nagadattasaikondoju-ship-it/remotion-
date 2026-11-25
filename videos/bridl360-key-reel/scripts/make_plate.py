"""Build clean plates from the BRIDL360 carousel photo: remove burned-in text, extend the sky, export a 1080x1920 plate."""
import cv2, numpy as np, os
D = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
src = cv2.imread(os.path.join(D, "carousel-src.png"))  # 1122x1402 BGR
H, W = src.shape[:2]
# 1) text mask: bright, low-saturation pixels in the sky band (y<620)
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
mask = np.zeros((H, W), np.uint8)
sky = (hsv[..., 2] > 175) & (hsv[..., 1] < 70)
mask[:625][sky[:625]] = 255
mask = cv2.dilate(mask, np.ones((9, 9), np.uint8), iterations=2)
clean = cv2.inpaint(src, mask, 12, cv2.INPAINT_TELEA)
# smooth the sky band where the text was so no ghosting remains
blur = cv2.GaussianBlur(clean, (0, 0), 14)
soft = cv2.GaussianBlur(mask, (0, 0), 10).astype(np.float32)[..., None] / 255.0
clean = (clean * (1 - soft) + blur * soft).astype(np.uint8)
# keep only the photo above the logo/URL band
photo = clean[:1150]
cv2.imwrite(os.path.join(D, "_clean_debug.jpg"), photo, [cv2.IMWRITE_JPEG_QUALITY, 92])
# 2) vertical plate 1080x1920: scale 1.36, bottom-aligned, sky extended upward
s = 1.36
ph = cv2.resize(photo, (int(W * s), int(1150 * s)), interpolation=cv2.INTER_LANCZOS4)
# unsharp to counter upscale softness
g = cv2.GaussianBlur(ph, (0, 0), 1.2)
ph = cv2.addWeighted(ph, 1.35, g, -0.35, 0)
x0 = int((ph.shape[1] - 1080) * 0.42)
ph = ph[:, x0:x0 + 1080]
plate = np.zeros((1920, 1080, 3), np.float32)
top = 1920 - ph.shape[0]
plate[top:] = ph
row = ph[:24].astype(np.float32).mean(axis=0)  # per-column colour at the top of the photo
row = cv2.GaussianBlur(row[None], (0, 0), 30)[0]
darker = row * np.array([0.72, 0.66, 0.62])  # BGR: sky deepens toward the zenith
for y in range(top):
    k = (top - y) / top
    plate[y] = row * (1 - k) + darker * k
# feather the seam
seam = 60
for i in range(seam):
    a = i / seam
    y = top + i
    plate[y] = plate[y] * a + (row * 1.0) * (1 - a)
plate = np.clip(plate, 0, 255).astype(np.uint8)
cv2.imwrite(os.path.join(D, "hyd-plate.jpg"), plate, [cv2.IMWRITE_JPEG_QUALITY, 93])
# 3) skyline strip for the key teeth (buildings band), 2x
strip = clean[760:1080, 0:1122]
strip = cv2.resize(strip, (1122 * 2, 320 * 2), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite(os.path.join(D, "hyd-strip.jpg"), strip, [cv2.IMWRITE_JPEG_QUALITY, 92])
print("plate top", top, "x0", x0)
