import os
import json
from functions import *


# 리뷰 데이터가 담긴 디렉토리 
directory = '../네이버크롤링/navercafe_review_extracted'

# 파일명들을 리스트로 생성 
file_lists = get_all_file_lists(directory)

# 요약 설명 파일을 저장할 디렉토리
output_dir = './cafe_summary'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 프롬프트 설정 
system_message = "내가 올리는 리뷰 데이터를 참고해서, 이 카페의 전반적인 분위기와 특징이 어떤지 설명해줘. 분위기, 제공되는 음료, 맛 등등에 대해 전반적으로 설명해줘. 설명은 약 300~500자정도로."
# 리뷰 데이터 -> 요약설명 

for file in file_lists:

    # 숨김파일 시 무시
    if file.startswith('.'):
     continue
    
    # 확인용
    print(file)

    # 디렉토리 생성
    file_path = f'{directory}/{file}'

    # gpt 통해 설명 추출 
    summary = ask_to_gpt(file_path, system_message)

    # 카페이름, 아이디 추출 (저장파일 생성 위해)
    cafe_name, cafe_id = extract_filename(file)
    
    # 카페 이름, 아이디랑 함께 내용 저장 
    data = {
        'cafe_name' : cafe_name,
        'cafe_id' : cafe_id,
        'summary' : summary
    }

    # 저장 파일명 생성
    output_filename = f'{output_dir}/summary_{cafe_name}_{cafe_id}.json'


    # 최종 데이터를 json으로 저장
    with open(output_filename,'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print(f"{cafe_name} 성공!")