# from transformers import BertModel, BertTokenizer
# import torch
# from sklearn.metrics.pairwise import cosine_similarity
# import pandas as pd
import json
from functions import *


def get_style_keyword(user_style):
    with open('/Users/minseo/YBIGTA_Proj/similarity/style_keyword_gpt.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_style_keywords = set(data[user_style])

    return user_style_keywords     


# 카페 키워드 데이터 가져오기 (야매카페키워드)
keyword_path = '/Users/minseo/YBIGTA_Proj/gpt_keyword/cafe_keyword/야매_keyword_without_weight_filtered.json'


# 유저 스타일 반환값 (CNN모델 들어갈 곳) + 해당 키워드 임베딩
# 레트로 스포티 로맨틱 캐주얼 미니멀 걸리시 클래식 시크 고프코어 스트릿 워크웨어 시티보이
user_style = '시티보이' 
user_style_keywords = get_style_keyword(user_style)
# keyword_embeddings = get_bert_embedding(user_style_keyword)


###############유사도 계산##################
with open(keyword_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
# 반환 딕셔너리
similarity_df = {}

# 모든 카페 키워드에 대해.. 
for cafe, keyword in data.items():
 
    cafe_keywords = set(keyword)

    jaccard_similarities = jaccard_similarity(user_style_keywords, cafe_keywords)

    # 유사도 결과를 저장
    similarity_df[cafe] = f'{jaccard_similarities:.4f}'

# 유사도 결과 출력 (소수점 6자리 포맷팅 적용)

print(similarity_df)

# 유사도 높은 순으로 정렬
sorted_cafe_similarities = sorted(similarity_df.items(), key=lambda item: item[1], reverse=True)


# 결과를 JSON 파일로 저장
output_file = f'/Users/minseo/YBIGTA_Proj/similarity/Jaccard/{user_style}_스타일_추천카페_KoBert.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(sorted_cafe_similarities, f, ensure_ascii=False, indent=4)

# 전체 카페 갯수 출력
total_cafes = len(sorted_cafe_similarities)
print(f"총 {total_cafes}개의 카페가 분석되었습니다.")
print(f"결과가 {output_file} 파일로 저장되었습니다.")