from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import pandas as pd
import random
import requests
import os
import time

driver = webdriver.Chrome()

# 스타일
style = '에스닉'
style_code = '19'

url = f'https://www.musinsa.com/snap/main/recommend?brands=&category=&genders=&height-range=&seasons=&styles={style_code}&tpos=&weight-range=&sort=NEWEST'
driver.get(url)
time.sleep(20)

# 변수 설정
img_urls = []
img_alts = []

# 스크롤 중간에 정지할 시간 설정
scroll_pause_time = 0.5



while True:
    # 현재 페이지의 HTML 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    snap_grid_list = soup.select_one('#__next > div.sc-7d5e0ea7-0.csTHEA.container > main > div.sc-f98f05ee-0.ipBIJV > div.sc-aaa4dfc3-0.gIYmjL > div:nth-child(2) > div > div.snap-grid-list')
    
    # 현재 로드된 모든 이미지 태그 수집
    img_tags = snap_grid_list.find_all('img', alt=True)
    new_images_count = 0
    
    for img_tag in img_tags:
        img_url = img_tag['src']
        img_alt = img_tag['alt']
        
        # 이미지 URL 중복 확인
        if img_url not in img_urls:
            img_urls.append(img_url)
            img_alts.append(img_alt)
            new_images_count += 1
    
    print(f'{len(img_urls)}만큼의 이미지를 수집했습니다..')
    
    # 스크롤
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(scroll_pause_time) 
    
    # 새로운 이미지가 더 이상 로드되지 않으면 루프 종료
    if new_images_count == 0:
        print("새로운 이미지가 없습니다.")
        break

print(f'##########{len(img_urls)}장의 이미지 수집 완료##########')
    
driver.quit()

# 이미지 저장 폴더 설정
if not os.path.exists(style):
    os.makedirs(style)

# 중복 방지를 위해 이미 다운로드한 이미지 URL 저장
downloaded_urls = set()

# 이미지 다운로드 
for idx, img_url in enumerate(img_urls):
    if img_url.startswith('http') and img_url not in downloaded_urls:
        img_response = requests.get(img_url)
        img_name = f'{img_alts[idx]}.jpg'  # 고유한 이름 설정
        with open(f'{style}/{img_name}', 'wb') as f:
            f.write(img_response.content)
        downloaded_urls.add(img_url)
        print(f'{idx}번째 이미지 다운 완료: {img_name}')
    else:
        print(f'중복 스킵: {img_url}')

print('모든 이미지들이 다운로드되었습니다.')
