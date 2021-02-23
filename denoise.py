import os
import cv2
import numpy as np

import pytesseract

for filename in sorted(os.listdir('raw')):
    if not 'png' in filename:
        continue
    img = cv2.cvtColor(cv2.imread('raw/'+ filename), cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    (thresh, img) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    kernel = np.ones((3,1), np.uint8)
    noisy = cv2.erode(img, kernel, iterations= 1)

    kernel = np.ones((2,2), np.uint8)
    final = cv2.erode(noisy, kernel, iterations= 1)

    inv = cv2.bitwise_not(final)

    my_config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    result = pytesseract.image_to_string(inv, lang='digits', config=my_config)
    print(filename, result)
    cv2.imwrite('test/' + filename, inv)
