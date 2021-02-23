import os
import sys
import requests
from bs4 import BeautifulSoup


def get_index():
    filelist = sorted(os.listdir('./raw'))
    if len(filelist) < 1:
        return 0
    last_filename = filelist[-1].split('.')[0]
    return int(last_filename) + 1

def download_img(index): 
    root_url = 'https://oauth.ccxp.nthu.edu.tw/v1.1/'
    url = root_url + 'authorize.php?response_type=code&client_id=eeclass&redirect_uri=https%3A%2F%2Feeclass.nthu.edu.tw%2Fservice%2Foauth%2F&scope=lmsid+userid&state='
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')
    imgsrc = root_url + soup.find(id='captcha_image').get('src')
    with open(f'./raw/{index:06}.png', 'wb') as f:
        f.write(requests.get(imgsrc).content)
    return

if __name__ == '__main__':
    i = get_index()
    for j in range(int(sys.argv[1])):
        download_img(i+j)

