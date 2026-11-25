"""Full-frame 1080x1920 plate from the BRIDL360 carousel photo, every burned-in word removed,
framed so the dense buildings sit where the key's building piece lines up (frame y ~830-1122)."""
import cv2, numpy as np, os
D = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
src = cv2.imread(os.path.join(D, "carousel-src.png"))
H, W = src.shape[:2]
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
bright = (hsv[..., 2] > 170) & (hsv[..., 1] < 80)
mask = np.zeros((H, W), np.uint8)
mask[:625][bright[:625]] = 255
band = np.zeros_like(bright); band[1150:1335, 360:1100] = True
mask[band & bright] = 255
mask = cv2.dilate(mask, np.ones((9, 9), np.uint8), iterations=2)
clean = cv2.inpaint(src, mask, 14, cv2.INPAINT_TELEA)
soft = cv2.GaussianBlur(mask, (0, 0), 10).astype(np.float32)[..., None] / 255.0
clean = (clean * (1 - soft) + cv2.GaussianBlur(clean, (0, 0), 14) * soft).astype(np.uint8)
S = 1.37
big = cv2.resize(clean, (round(W * S), round(H * S)), interpolation=cv2.INTER_LANCZOS4)
big = cv2.addWeighted(big, 1.3, cv2.GaussianBlur(big, (0, 0), 1.1), -0.3, 0)
TY = round(1080 * S - 1122)          # source row 1080 (base of the white blocks) lands on frame y 1122
X0 = 150
plate = np.zeros((1920, 1080, 3), np.float32)
part = big[TY:TY + 1920, X0:X0 + 1080].astype(np.float32)
plate[:part.shape[0]] = part
gap = 1920 - part.shape[0]
if gap > 0:  # extend the foliage downward: mirrored, softened, darkened
    refl = part[-gap:][::-1]
    refl = cv2.GaussianBlur(refl, (0, 0), 10)
    k = (np.linspace(0.55, 0.06, gap) ** 1.2)[:, None, None]
    plate[part.shape[0]:] = refl * k
    seam = 40
    for i in range(seam):
        y = part.shape[0] - seam // 2 + i
        a = i / seam
        plate[y] = plate[y] * (1 - abs(a - 0.5)) + cv2.GaussianBlur(plate[y - 3:y + 4], (0, 0), 2)[3] * abs(a - 0.5)
cv2.imwrite(os.path.join(D, "plate.jpg"), np.clip(plate, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])
print("TY", TY, "gap", gap)
