import json
import pandas as pd

# 두 개의 JSON 파일 경로 설정
file1_path = '/content/drive/MyDrive/cafe_summary_style_similarities.json'
file2_path = '/content/drive/MyDrive/cafe_keyword_style_similarities.json'

# 파일 불러오기
with open(file1_path, 'r', encoding='utf-8') as f1:
    data1 = json.load(f1)

with open(file2_path, 'r', encoding='utf-8') as f2:
    data2 = json.load(f2)

# 공통 카페의 결과 비교 (DataFrame 형태로 변환)
comparison_results = {}

for cafe in data1:
    if cafe in data2:
        # summary_style_similarities와 keyword_style_similarities를 각각 DataFrame으로 변환
        df_summary = pd.DataFrame(data1[cafe], columns=["Summary Style", "Summary Similarity"])
        df_keyword = pd.DataFrame(data2[cafe], columns=["Keyword Style", "Keyword Similarity"])

        # 두 DataFrame을 나란히 놓기 (index를 기준으로 병합하지 않음)
        df_combined = pd.concat([df_summary, df_keyword], axis=1)

        # DataFrame을 리스트 형식으로 변환하여 저장
        comparison_results[cafe] = df_combined.to_dict(orient="records")

# 비교 결과를 JSON 파일로 저장
output_file = '/content/drive/MyDrive/cafe_combined_similarity_side_by_side.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(comparison_results, f, ensure_ascii=False, indent=4)

# 결과 출력
total_cafes = len(comparison_results)
print(f"총 {total_cafes}개의 카페가 비교되었습니다.")
print(f"결과가 {output_file} 파일로 저장되었습니다.")