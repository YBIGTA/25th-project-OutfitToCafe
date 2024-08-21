import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

# JSON 파일 경로
json_file_path = '/Users/macbook/Desktop/numbered_cafes.json'

# JSON 파일에서 카페 목록 로드
with open(json_file_path, 'r', encoding='utf-8') as f:
    cafes = json.load(f)

# 네이버 모바일 검색 URL 패턴
search_url = "https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query={}"

def crawl_images(cafe_name):
    # 카페명을 URL에 맞게 인코딩
    encoded_cafe_name = urllib.parse.quote(cafe_name)
    url = search_url.format(encoded_cafe_name)

    # 네이버 검색 결과 페이지 요청
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve search results for {cafe_name}")
        return []

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser')

    # 첫 번째 selector로 이미지 태그를 선택하여 src 속성 추출
    image_tags_1 = soup.select('img.K0PDV._div')
    image_urls_1 = [img['src'] for img in image_tags_1 if 'src' in img.attrs]

    # 첫 번째 리스트의 마지막 이미지를 제외
    if image_urls_1:
        image_urls_1 = image_urls_1[:-1]

    # 두 번째 selector로 음식 사진 이미지 태그를 선택하여 src 속성 추출
    ul_element = soup.select_one('#place-main-section-root > div > div:nth-child(4) > div.place_section_content > ul')
    if ul_element:
        image_tags_2 = ul_element.select('div.lazyload-wrapper img')
        image_urls_2 = [img['src'] for img in image_tags_2 if 'src' in img.attrs]
    else:
        image_urls_2 = []

    # 두 리스트를 합쳐서 반환
    all_image_urls = image_urls_1 + image_urls_2
    return all_image_urls

# 각 카페별로 이미지 크롤링 수행
for cafe in cafes:
    cafe_name = cafe["카페명"]
    print(f"Crawling images for: {cafe_name}")
    image_urls = crawl_images(cafe_name)
    for idx, url in enumerate(image_urls):
        print(f"Image {idx + 1}: {url}")
