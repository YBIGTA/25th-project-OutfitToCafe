import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

# 크롤링할 인스타그램 url 설정
url = "https://www.instagram.com/oafuoafu"

# 이미지를 저장할 폴더 이름 설정
folder_name = "오푸_instagram_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# 크롬 웹드라이버 구동 및 기본설정
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get(url)

# 이미지 클래스명으로 모든 이미지 요소 찾기
images = driver.find_elements(By.CLASS_NAME, "x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3")

# 이미지 주소 저장 및 다운로드
for idx, image in enumerate(images):
    image_src = image.get_attribute('src')
    response = requests.get(image_src)
    filename = os.path.join(folder_name, f'오푸_image_{idx}.jpg')
    with open(filename, 'wb') as f:
        f.write(response.content)

print(f"사진 수집이 완료되었습니다. 모든 사진이 '{folder_name}' 폴더에 저장되었습니다.")

# 브라우저 종료
driver.quit()