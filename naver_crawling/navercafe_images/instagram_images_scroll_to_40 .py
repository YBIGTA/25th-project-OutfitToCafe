import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import base64

# 크롤링할 인스타그램 URL 설정
url = "https://www.instagram.com/camelcoffee_kor/"

# JSON 파일 이름 예시
json_file_name = "naver_review_60_카멜커피 성수점_55585656.json"

# JSON 파일 이름에서 num과 cafe_name 추출
file_parts = json_file_name.split('_')
num = file_parts[2]
cafe_name = file_parts[3]

# 이미지 저장 폴더 설정 (cafeinsta_images 폴더 내에 저장)
base_folder = "cafeinsta_images"
folder_name = os.path.join(base_folder, f"{num}_{cafe_name}_instagram_images")

# 폴더가 존재하지 않을 경우 생성
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# 크롬 웹드라이버 구동 및 기본설정
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get(url)

# 이미지 수집 수와 스크롤 횟수 설정
target_image_count = 40
scroll_pause_time = 2  # 스크롤 후 대기 시간 (초)
collected_images = set()

while len(collected_images) < target_image_count:
    # 현재 로드된 모든 이미지 요소 찾기
    images = driver.find_elements(By.CLASS_NAME, "x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3")
    
    # 새롭게 발견된 이미지 주소 저장
    for image in images:
        image_src = image.get_attribute('src')
        if image_src and image_src not in collected_images:  # 이미지 소스가 None이 아닌지 확인
            collected_images.add(image_src)
            if len(collected_images) >= target_image_count:
                break
    
    # 페이지 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

# 이미지 다운로드
for idx, image_src in enumerate(collected_images):
    try:
        if image_src.startswith('data:image'):  # Base64 인코딩된 이미지 처리
            header, encoded = image_src.split(',', 1)
            data = base64.b64decode(encoded)
            file_extension = header.split('/')[1].split(';')[0]  # 파일 확장자 추출 (png, jpeg 등)
            filename = os.path.join(folder_name, f'{cafe_name}_image_{idx + 1}.{file_extension}')
            with open(filename, 'wb') as f:
                f.write(data)
        else:  # 일반 URL 이미지 다운로드
            response = requests.get(image_src)
            response.raise_for_status()  # 요청에 실패한 경우 예외 발생
            filename = os.path.join(folder_name, f'{cafe_name}_image_{idx + 1}.jpg')
            with open(filename, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print(f"이미지 다운로드 중 오류 발생: {e}")

print(f"사진 수집이 완료되었습니다. 총 {len(collected_images)}장의 사진이 '{folder_name}' 폴더에 저장되었습니다.")

# 브라우저 종료
driver.quit()