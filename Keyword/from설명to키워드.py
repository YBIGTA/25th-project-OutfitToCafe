import os
import json
from functions import *
import ast

# 설명 데이터가 담긴 디렉토리
directory = './cafe_summary'
# 파일명 리스트 생성
file_lists = get_all_file_lists(directory)

# 키워드 파일 저장 디렉토리
output_dir = './cafe_keyword'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 데이터 저장할 딕셔너리
data_dict = {}

# 프롬프트
system_message = '''
내가 입력한 데이터의 "summary"부분에서 키워드를 20~30개 추출해줘.
빈도수에 따른 가중치도 0.1~1 사이로 함께 출력해줘.
반환은 {'키워드1':가중치, '키워드2':가중치, ... }로, 줄바꿈 없이 부탁해. 
'''

for file in file_lists:

    # 숨김파일 무시
    if file.startswith('.'):
        continue
    # 확인
    print(file)
    # 디렉토리 생성
    file_path = f'{directory}/{file}'

    # gpt 사용
    keywords = ask_to_gpt(file_path, system_message)

    if len(keywords) == 0:
        print('gpt가 동작하지 않음!!!')

    # 딕셔너리 형태로 변환
    keywords_dict = ast.literal_eval(keywords)
    # 카페 이름, 아이디 추출
    cafe_name, cafe_id = extract_filename(file)
    # 카페 이름, 아이디와 함께 키워드 저장 
    data_dict[cafe_name] = {'cafe_id' : cafe_id, 'keywords': keywords_dict}

    print(f'{cafe_name} 성공!')

# 하나의 파일로 저장
output_filename = f'{output_dir}/cafe_keywords.json'
with open(output_filename, 'w', encoding='utf-8') as file:
    json.dump(data_dict, file, ensure_ascii=False, indent=4)