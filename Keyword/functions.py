import os
import json
from dotenv import load_dotenv
from openai import OpenAI


# api key 가져오기
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# gpt에게 물어보기 
def ask_to_gpt(file_path, system_message):
    # JSON 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as f:
        data = str(json.load(f))

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": data }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 사용할 모델을 선택하세요.
        messages=messages,
        max_tokens=3000,  # 요약의 길이를 설정합니다.
        temperature=0.7  # 텍스트 생성의 창의성을 조정합니다.
    )
    
    # 내용 반환
    return response.choices[0].message.content

# 모든 파일 가져오기 
def get_all_file_lists(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# 파일 이름에서 카페명, 카페id 추출하기 
def extract_filename(filename):
    filename = filename.replace('.json', '').replace('naver_review_', '').replace('summary_', '')
    cafe_name = filename.split('_')[0]
    cafe_id = filename.split('_')[1]
    return cafe_name, cafe_id
