import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import time
import datetime
from bs4 import BeautifulSoup

# JSON 파일 열기
with open('/Users/macbook/Desktop/numbered_cafes.json', 'r', encoding='utf-8') as json_file:
    cafe_list = json.load(json_file)

# 크롤링할 카페 n개 선택
cafe_list_to_crawl = cafe_list[:]

# 웹 드라이버 옵션 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

# 웹 드라이버 초기화
driver = webdriver.Chrome(options=options)

# 리뷰 데이터를 저장할 리스트
reviews_data = []

# 크롤링 시작
try:
    for cafe in cafe_list_to_crawl:
        cafe_name = cafe['카페명']
        cafe_id = cafe['id값']
        cafe_number = cafe['번호']  # 카페 번호 가져오기
        print(f"크롤링 중: {cafe_name}")

        try:
            # URL 구성
            url = f'https://m.place.naver.com/restaurant/{cafe_id}/review/visitor?entry=ple&review'
            driver.get(url)
            driver.implicitly_wait(30)

            # 식당 이름 추출
            try:
                restaurant_name_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#_header'))
                )
                restaurant_name = restaurant_name_element.text
                print(f"추출된 식당 이름: {restaurant_name}")
            except Exception as e:
                restaurant_name = 'N/A'
                print(f"식당 이름 추출 실패: {e}")

            # Pagedown
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

            try:
                for i in range(30):  # 최대 30번 반복
                    driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/div[2]/div/a').click()
                    time.sleep(0.4)
            except Exception as e:
                print('More reviews button not found or finished loading reviews')

            time.sleep(5)  # 페이지 로드 대기
            html = driver.page_source
            bs = BeautifulSoup(html, 'html.parser')
            reviews = bs.select('li.pui__X35jYm.EjjAW')

            for r in reviews:
                # nickname
                nickname = r.select_one('div.pui__JiVbY3 > span.pui__uslU0d').text if r.select_one('div.pui__JiVbY3 > span.pui__uslU0d') else ''

                # content
                content = r.select_one('div.pui__vn15t2 > a.pui__xtsQN-').text if r.select_one('div.pui__vn15t2 > a.pui__xtsQN-') else ''

                # date
                date_elements = r.select('div.pui__QKE5Pr > span.pui__gfuUIT > time')
                date = date_elements[0].text if date_elements else 'N/A'

                # revisit
                revisit_span = r.select('div.pui__QKE5Pr > span.pui__gfuUIT')
                revisit = revisit_span[1].text if len(revisit_span) > 1 else 'N/A'

                # 리뷰 데이터 저장
                reviews_data.append({
                    'restaurant_name': restaurant_name,  # 식당 이름 추가
                    'url': url,  # URL 추가
                    'nickname': nickname,
                    'content': content,
                    'date': date,
                    'revisit': revisit,
                    'cafe_id': cafe_id  # 카페 ID 추가
                })

                time.sleep(0.06)

            # 파일 저장 (식당 이름을 파일명에 포함)
            sanitized_name = re.sub(r'[\\/*?:"<>|]', "", restaurant_name)  # 파일명에 사용할 수 없는 문자를 제거
            file_name = f'/Users/macbook/Desktop/naver_review_{cafe_number}_{sanitized_name}_{cafe_id}.json'
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(reviews_data, f, ensure_ascii=False, indent=4)
            
            # 리뷰 데이터를 초기화 (다음 카페의 리뷰 데이터 저장을 위해)
            reviews_data = []

        except Exception as e:
            print(f"Error processing cafe: {cafe_name} (ID: {cafe_id}), Error: {e}")

finally:
    # 브라우저 종료
    driver.quit()

print("크롤링이 완료되었습니다.")
