import os
import time
from selenium import webdriver
import cv2
import numpy as np
import pytesseract
from scipy import stats

def get_imgs(save_dir): 
    url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?response_type=code&client_id=eeclass&redirect_uri=https%3A%2F%2Feeclass.nthu.edu.tw%2Fservice%2Foauth%2F&scope=lmsid+userid&state='
    driver = webdriver.Safari()
    driver.get(url)
    time.sleep(2)
    img_node = driver.find_element_by_id('captcha_image')
    img_src = img_node.get_attribute('src')
    for index in range(0, 10):
        driver.get(img_src)
        with open(f'{save_dir}{index:03}.png', 'wb') as f:
            f.write(driver.find_element_by_tag_name('img').screenshot_as_png)
    driver.close()
    return

# All params are decided by... nothing
def denoise(read_dir, save_dir):
    for filename in sorted(os.listdir(read_dir)):
        img = cv2.cvtColor(cv2.imread(read_dir + filename), cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img,3)
        (thresh, img) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        kernel = np.ones((4,1), np.uint8)
        virtical_only = cv2.dilate(img, kernel, iterations= 2)

        kernel = np.ones((1,3), np.uint8)
        final = cv2.dilate(virtical_only, kernel, iterations= 2)

        cv2.imwrite(save_dir + filename, final)
    return 

def ocr(read_dir):
    results = np.empty((0, 4), int)
    my_config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    for filename in sorted(os.listdir(read_dir)):
        img = cv2.imread(read_dir + filename)
        result = pytesseract.image_to_string(img, lang='digits', config=my_config).strip()
        print(filename, result)
        if len(result) == 4:
            results = np.append(results,
                np.array([ list(result) ]),
                axis=0)
    return stats.mode(results)[0]


if __name__ == '__main__':
    get_imgs('raw/')
    denoise('raw/', 'denoised/')
    print(ocr('denoised/'))


