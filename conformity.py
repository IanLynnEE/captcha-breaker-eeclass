import os
import requests
from bs4 import BeautifulSoup

import cv2
import numpy as np
import pytesseract

# TODO
# Need cookie
def get_imgs(): 
    root_url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/'
    url = root_url + 'authorize.php?response_type=code&client_id=eeclass&redirect_uri=https%3A%2F%2Feeclass.nthu.edu.tw%2Fservice%2Foauth%2F&scope=lmsid+userid&state='
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')
    imgsrc = root_url + soup.find(id='captcha_image').get('src')
    for index in range(0, 10):
        with open(f'temp/{index:06}.png', 'wb') as f:
            f.write(requests.get(imgsrc).content)
    return

def denoise():
    for filename in sorted(os.listdir('temp')):
        img = cv2.cvtColor(cv2.imread('temp/'+ filename), cv2.COLOR_BGR2GRAY)
        (thresh, img) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        kernel = np.ones((3,1), np.uint8)
        noisy = cv2.dilate(img, kernel, iterations= 1)

        kernel = np.ones((1,3), np.uint8)
        final = cv2.dilate(noisy, kernel, iterations= 1)

        cv2.imwrite('temp/' + filename, final)
    return 

def ocr():
    my_config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    valid_results = []
    for filename in sorted(os.listdir('temp')):
        img = cv2.imread('temp/'+ filename)
        result = pytesseract.image_to_string(img, lang='digits', config=my_config).strip()
        if len(result) == 4:
            valid_results.append(result)
    counts = np.bincount(valid_results)
    return np.argmax(counts)




get_imgs()
denoise()
print(ocr())


