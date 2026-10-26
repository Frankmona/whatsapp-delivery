import qrcode
from PIL import Image
import cv2
import numpy as np

url = "https://wa.me/2347037858093?text=Hi%20FM%20XPRESS%2C%20I%20am%20applying%20for%20the%20Dispatch%20Rider%20job%20in%20Kubwa."

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=12,
    border=4
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="#020617", back_color="#ffffff").convert("RGBA")
img.save("public/images/fmxpress_hiring_qr.png")

# Verify decoding using OpenCV
cv_img = cv2.imread("public/images/fmxpress_hiring_qr.png")
detector = cv2.QRCodeDetector()
data, bbox, straight_qrcode = detector.detectAndDecode(cv_img)
if data:
    print("SUCCESS: Decoded QR correctly ->", data)
else:
    print("FAILED to decode QR")
