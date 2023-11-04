import re

import cv2
import numpy as np
import qrcode
from secret import flag

assert re.match(r'^TSGCTF\{[a-zA-Z_]{1468}\}$', flag)

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=2, border=4)
qr.add_data(qrcode.util.QRData(flag * 2))
qr.make(fit=False)
img = np.array(qr.make_image()._img, dtype=np.float64)[1:-1, 1:-1]
sx, sy = img.shape
img = cv2.resize(img, (sx // 4, sy // 4),  interpolation = cv2.INTER_AREA)
cv2.imwrite('flag.png', img * 255)
