import json
from experiment import *

# 사용자가 설정한 스타일에 대한 키워드를 가져오는 함수
def get_style_keyword(user_style):
    with open('/Users/macbook/Desktop/YBIGTA_24_SUMMER_PROJECT/cafe_review_summary&keyword_data/style_keyword_gpt.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_style_keyword = ' '.join(data[user_style])
    return user_style_keyword

# 카페 키워드 데이터 파일 경로
keyword_path = '/Users/macbook/Desktop/YBIGTA_24_SUMMER_PROJECT/cafe_review_summary&keyword_data/야매_keyword_without_weight_filtered.json'


# 유저 스타일 설정 (예시: '걸리시')
user_style = '시티보이'
user_style_keyword = get_style_keyword(user_style)
keyword_embeddings = get_bert_embedding(user_style_keyword)

############### 유사도 계산 ##################
with open(keyword_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 유사도 결과를 저장할 딕셔너리
similarity_df = {}

# 모든 카페 키워드에 대해 유사도 계산
for cafe, keyword in data.items():
    text = ' '.join(keyword)
    text_embedding = get_bert_embedding(text)

    # 코사인 유사도 계산
    cosine_similarities = cosine_similarity(text_embedding, keyword_embeddings)[0][0]

    # 유사도 결과를 딕셔너리에 저장
    similarity_df[cafe] = f'{cosine_similarities:.4f}'

# 유사도 결과를 출력
print(similarity_df)

# 유사도 높은 순으로 정렬
sorted_cafe_similarities = sorted(similarity_df.items(), key=lambda item: item[1], reverse=True)

# 결과를 JSON 파일로 저장 (경로 수정 필요)
output_file = f'/Users/macbook/Desktop/YBIGTA_24_SUMMER_PROJECT/KoBERT/야매_gpt_키워드동일_{user_style}_스타일_추천카페_KoBert.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(sorted_cafe_similarities, f, ensure_ascii=False, indent=4)

# 전체 카페 갯수 출력
total_cafes = len(sorted_cafe_similarities)
print(f"총 {total_cafes}개의 카페가 분석되었습니다.")
print(f"결과가 {output_file} 파일로 저장되었습니다.")