import json
import pandas as pd

# JSON 파일 불러오기
with open('/content/drive/MyDrive/cafe_combined_similarity_side_by_side.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# DataFrame으로 변환
dfs = []
for cafe, comparisons in data.items():
    df = pd.DataFrame(comparisons)
    df['Cafe'] = cafe  # 카페 이름을 컬럼으로 추가
    dfs.append(df)

# 모든 DataFrame을 하나로 합치기
final_df = pd.concat(dfs, ignore_index=True)

# 열 순서 재정렬 (카페 이름을 가장 왼쪽으로 이동)
final_df = final_df[['Cafe', 'Summary Style', 'Summary Similarity', 'Keyword Style', 'Keyword Similarity']]

# CSV 파일로 저장
output_csv = '/content/drive/MyDrive/cafe_combined_similarity_sorted_with_cafe_first.csv'
final_df.to_csv(output_csv, index=False, encoding='utf-8-sig')

print(f"결과가 {output_csv} 파일로 저장되었습니다.")