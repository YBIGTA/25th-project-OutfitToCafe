import os
import json

# 디렉토리 경로를 설정합니다.
input_directory = '/Users/macbook/Desktop/navercafe_review'
output_directory = '/Users/macbook/Desktop/navercafe_review_content'

# 출력 디렉토리가 없으면 생성합니다.
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 디렉토리 내의 모든 파일을 읽습니다.
for filename in os.listdir(input_directory):

    # .DS_Store (숨김파일) 의 경우 무시
    if filename == ".DS_Store":
        continue

    print(f"Processing {filename}")

    # 파일 경로를 생성합니다.
    input_file_path = os.path.join(input_directory, filename)
    
    # JSON 파일 읽기
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 리뷰 목록이 리스트 형태로 되어 있으므로, 각 리뷰의 'content' 키를 추출합니다.
    extracted_contents = [review['content'] for review in data if 'content' in review and review['content'].strip()]

    if not extracted_contents:
        print(f"No valid 'content' found in {filename}")
        continue

    # 출력 파일 경로를 생성합니다.
    output_file_path = os.path.join(output_directory, filename)

    # 추출된 'content' 부분을 새로운 JSON 파일로 저장합니다.
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(extracted_contents, output_file, ensure_ascii=False, indent=4)

    print(f"Saved extracted content to {output_file_path}")

print("All files processed successfully.")
