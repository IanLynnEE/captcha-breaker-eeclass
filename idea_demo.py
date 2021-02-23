import os
import time
from selenium import webdriver
import cv2
import numpy as np
import pytesseract
from scipy import stats

def touch_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)   
    return

def get_imgs(): 
    url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?response_type=code&client_id=eeclass&redirect_uri=https%3A%2F%2Feeclass.nthu.edu.tw%2Fservice%2Foauth%2F&scope=lmsid+userid&state='
    driver = webdriver.Safari()
    driver.get(url)
    time.sleep(1)
    img_node = driver.find_element_by_id('captcha_image')
    img_src = img_node.get_attribute('src')
    for index in range(0, 10):
        driver.get(img_src)
        with open(f'test/{index:03}.png', 'wb') as f:
            f.write(driver.find_element_by_tag_name('img').screenshot_as_png)
    driver.close()
    return


def binarize(img_list):
    out = []
    for img in img_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (th, img) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        out.append(img)
    return out


def dilate(img_list, kernel):
    out = []
    for img in img_list:
        out.append(cv2.dilate(img, kernel, iterations= 1))
    return out


def ocr_by_mode(img_list):
    results = np.empty((0, 4), int)
    my_config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    for img in img_list:
        result = pytesseract.image_to_string(img, lang='digits', config=my_config).strip()
        print(result)
        if len(result) == 4:
            results = np.append(results,
                np.array([ list(result) ]),
                axis=0)
    return stats.mode(results)[0]


def save_imgs_in_temp(img_list):
    for i, img in enumerate(img_list):
        cv2.imwrite(f'temp/{i:03}.png', img)
    return


if __name__ == '__main__':
    touch_dir('test')
    get_imgs()
    raw_imgs = [ cv2.imread(f'test/{filename}') for filename in sorted(os.listdir('test')) ]
    bw_imgs = binarize(raw_imgs)
    imgs_1 = dilate(bw_imgs, np.ones((4,1), np.uint8))
    imgs_2 = dilate(imgs_1, np.ones((1,3), np.uint8))
    touch_dir('temp')
    save_imgs_in_temp(imgs_2)
    print('----------')
    print(ocr_by_mode(imgs_2))


