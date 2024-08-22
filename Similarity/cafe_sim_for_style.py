import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np


# 저장경로 
save_path = './results'


# 스타일 키워드 및 카페 키워드 불러오기 
keyword_path = '../Keyword/cafe_keyword/split_cafe_keywords.json'
style_path = '../Keyword/style_keyword_gpt.json'

with open(keyword_path, 'r', encoding='utf-8') as f:
    cafe_dict = json.load(f) # 카페키워드 (json->dict)
with open(style_path, 'r', encoding='utf-8') as f:
    style_dict = json.load(f)   # 스타일키워드(json->dict)

# 데이터프레임으로 만들기 (cafe_df, style_df)
cafe_dict_val = [" ".join(value_list) for value_list in cafe_dict.values()]
cafe_df = pd.DataFrame({'카페이름' : cafe_dict.keys(), '키워드' : cafe_dict_val})  

style_dict_val = [" ".join(value_list) for value_list in style_dict.values()]
style_df = pd.DataFrame({'스타일' : style_dict.keys(), '키워드' : style_dict_val})

# CountVectorizer를 사용해 텍스트를 벡터화
def countvect_similarity(cafe_df, style_df):
    vectorizer = CountVectorizer()

    # 스타일 키워드 학습, 벡터화
    cafe_vectors = vectorizer.fit_transform(cafe_df['키워드'])
    style_vectors = vectorizer.transform(style_df['키워드'])

    # 코사인 유사도 계산
    similarity_matrix = cosine_similarity(style_vectors, cafe_vectors)

    # 유사도 순으로 스타일 정렬 및 유사도 값 추출
    sorted_cafes = []
    sorted_similarities = []

    for i in range(similarity_matrix.shape[0]):
        sorted_idx = similarity_matrix[i].argsort()[::-1]
        sorted_cafes.append(cafe_df['카페이름'].iloc[sorted_idx].tolist())
        sorted_similarities.append(similarity_matrix[i][sorted_idx].tolist())

    # 결과를 데이터프레임으로 정리
    countvect_result_df = pd.DataFrame({
        '스타일': style_df['스타일'],
        '유사한 스타일': sorted_cafes,
        '유사도': sorted_similarities
    })

    # 결과 데이터프레임 저장
    countvect_result_df.to_csv(f'{save_path}/스타일별카페_countvect.csv')


# CountVectorizer를 사용해 텍스트를 벡터화
def tfidf_similarity(cafe_df, style_df):
    vectorizer = TfidfVectorizer()

    # 스타일 키워드 학습, 벡터화
    cafe_vectors = vectorizer.fit_transform(cafe_df['키워드'])
    style_vectors = vectorizer.transform(style_df['키워드'])

    # 코사인 유사도 계산
    similarity_matrix = cosine_similarity(style_vectors, cafe_vectors)

    # 유사도 순으로 스타일 정렬 및 유사도 값 추출
    sorted_cafes = []
    sorted_similarities = []

    for i in range(similarity_matrix.shape[0]):
        sorted_idx = similarity_matrix[i].argsort()[::-1]
        sorted_cafes.append(cafe_df['카페이름'].iloc[sorted_idx].tolist())
        sorted_similarities.append(similarity_matrix[i][sorted_idx].tolist())

    # 결과를 데이터프레임으로 정리
    countvect_result_df = pd.DataFrame({
        '스타일': style_df['스타일'],
        '유사한 스타일': sorted_cafes,
        '유사도': sorted_similarities
    })

    # 결과 데이터프레임 저장
    countvect_result_df.to_csv(f'{save_path}/스타일별카페_tfidf.csv')


# 함수 진행
countvect_similarity(cafe_df, style_df)
tfidf_similarity(cafe_df, style_df)