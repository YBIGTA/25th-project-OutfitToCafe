def calculate_score(cafe_data, selfie_weights):
    score = 0
    # 셀피의 각 키워드에 대해 카페의 키워드와 매칭하여 점수 계산
    # 예) 셀카 분석값 -> [고프코어: 0.7, 시티보이: 0.2, 시크: 0.1]
    # 카페 1의 키워드별 유사도 -> [고프코어: 0.78, 시티보이: 0.22, 시크: 0.55, 걸리쉬: 0.12, ...]
    # 셀카에 대한 카페 1의 evaluation value = 0.7 * 0.78 + 0.2 *  0.22 + 0,1 * 0.55
    # 다음과 같은 연산을 cafe_vectorize에 있는 모든 카페에 대해 진행
    for keyword, weight in selfie_weights.items():
        for cafe_keyword in cafe_data:
            if cafe_keyword[0] == keyword:
                score += weight * cafe_keyword[1]
    return score