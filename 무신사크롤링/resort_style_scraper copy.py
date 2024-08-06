from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

# Chrome 옵션 설정
options = Options()
options.headless = False
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# ChromeDriver 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 스타일별 폴더 생성
style = '리조트' # 이 스크립트의 스타일
base_url = 'https://www.musinsa.com/snap/main/recommend'
save_dir = 'musinsa_style_images'

def save_images(driver, style_dir, images, saved_images):
    for img_element in images:
        try:
            img_url = img_element.get_attribute('src')
            img_alt = img_element.get_attribute('alt')

            # 고유 파일명 생성
            img_name = f"{img_alt}.jpg"
            img_path = os.path.join(style_dir, img_name)

            if not os.path.exists(img_path):
                # 이미지 저장
                img_data = requests.get(img_url).content
                with open(img_path, 'wb') as handler:
                    handler.write(img_data)

                print(f"이미지 저장 완료: {img_name}")
                saved_images += 1

        except Exception as e:
            print(f"이미지 저장 중 오류 발생: {e}")
            continue
    
    return saved_images

try:
    # 스타일별 폴더 생성
    style_dir = os.path.join(save_dir, style)
    os.makedirs(style_dir, exist_ok=True)
    
    # 페이지 로드
    driver.get(base_url)
    
    # 스타일 필터 선택 및 클릭
    style_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @aria-haspopup="dialog" and contains(text(), "스타일")]'))
    )
    style_button.click()

    style_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//span[contains(text(), "{style}")]'))
    )
    style_option.click()

    # "스냅 보기" 버튼 클릭
    snap_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "스냅 보기")]'))
    )
    snap_button.click()
    
    # "인기순" 버튼 클릭
    popular_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "인기순")]'))
    )
    popular_button.click()

    # "최신순" 버튼 클릭
    latest_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "최신순")]'))
    )
    latest_button.click()

    # 페이지 로딩 대기
    time.sleep(3)  # 페이지 로딩을 기다리기 위해 3초 대기 (필요시 시간 조절)
    
    # 이미지 다운로드
    scroll_pause_time = 2  # 스크롤 후 대기 시간
    saved_images = 0

    while True:
        # snap-grid-list 안의 이미지들 가져오기
        images = driver.find_elements(By.XPATH, '//div[@class="snap-grid-list"]//img')
        saved_images = save_images(driver, style_dir, images, saved_images)
        
        # 다음 이미지를 로드하기 위해 스크롤 다운
        driver.execute_script("window.scrollBy(0, window.innerHeight);")  # 전체 화면 크기만큼 스크롤
        time.sleep(scroll_pause_time)  # 스크롤 후 잠시 대기
        
        # 스크롤 후의 새로운 높이를 측정하여, 더 이상 스크롤이 안되면 종료
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == driver.execute_script("return window.pageYOffset + window.innerHeight"):
            break  # 페이지 끝에 도달하면 종료

finally:
    # 브라우저 닫기
    driver.quit()
