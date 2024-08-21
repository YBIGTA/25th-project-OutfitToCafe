# KoBERT_combine_keyword.py - cosine, jaccard 유사도를 합친 결과 

import json
from functions import *

def get_style_keyword(user_style):
    with open('../../style_keyword_gpt.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_style_keywords = ' '.join(data[user_style])
    user_style_keywords_jaccard = set(data[user_style])

    return user_style_keywords, user_style_keywords_jaccard      

# 카페 키워드 데이터 가져오기
keyword_path = '../../카페키워드추출/cafe_keyword/split_cafe_keywords.json'

# 유저 스타일 반환값 (CNN모델 들어갈 곳) + 해당 키워드 임베딩
user_styles =['레트로', '스포티', '로맨틱', '캐주얼', '미니멀', '걸리시', '클래식', '시크', '고프코어', '스트릿', '워크웨어', '시티보이']
for user_style in user_styles:    
    user_style_keywords = get_style_keyword(user_style)[0]
    user_style_keywords_jaccard =  get_style_keyword(user_style)[1]

    keyword_embeddings = get_bert_embedding(user_style_keywords)


    ###############유사도 계산##################
    with open(keyword_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 반환 딕셔너리
    similarity_df = {}

    # 모든 카페 키워드에 대해.. 
    for cafe, keyword in data.items():

        # 카페키워드 변환
        cafe_keywords = set(keyword) # 자카드유사도
        text = ' '.join(keyword) # 코사인유사도

        # 카페 키워드에 대해 BERT 임베딩 생성 후 코사인 유사도 계산
        text_embedding = get_bert_embedding(text)
        cosine_similarities = cosine_similarity(text_embedding, keyword_embeddings)[0][0]

        # 자카드 유사도 계산 
        jaccard_similarities = jaccard_similarity(user_style_keywords_jaccard, cafe_keywords)
        
        # 자카드 유사도와 코사인 유사도 합치기 (2:8)\
        combined_similarity = (0.3 * jaccard_similarities) + (0.7 * cosine_similarities)
        # 유사도 결과를 저장
        similarity_df[cafe] = f'{combined_similarity:.5f}'

    # 유사도 결과 출력 (소수점 5자리 포맷팅 적용)
    print(similarity_df)

    # 유사도 높은 순으로 정렬
    sorted_cafe_similarities = sorted(similarity_df.items(), key=lambda item: item[1], reverse=True)

    # 결과를 JSON 파일로 저장
    output_file = f'/Users/minseo/YBIGTA_Proj/similarity/combine유사도/{user_style}_스타일_추천카페_KoBert.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_cafe_similarities, f, ensure_ascii=False, indent=4)

    # 전체 카페 갯수 출력
    total_cafes = len(sorted_cafe_similarities)
    print(f"{user_style}에 대해 총 {total_cafes}개의 카페가 분석되었습니다.")
    print(f"결과가 {output_file} 파일로 저장되었습니다.")