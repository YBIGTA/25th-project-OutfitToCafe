import json
import random
import os

# 키워드 목록
keywords = [
    "미니멀", "캐주얼", "걸리시", "고프코어", "시티보이", "레트로", 
    "로맨틱", "클래식", "시크", "스트릿", "스포티", "워크웨어"
]

# 저장 경로 설정
output_directory = "C:/Users/lgsc0/Desktop/신기플/selfie_analyze"
os.makedirs(output_directory, exist_ok=True)  # 디렉토리가 없을 경우 생성

# 9개의 파일을 생성
for i in range(1, 10):
    # 12개의 가중치를 랜덤으로 생성하고, 총합을 1로 맞춤
    weights = [random.random() for _ in range(12)]
    total = sum(weights)
    normalized_weights = [round(w / total, 3) for w in weights]
    
    # 무작위로 5~6개의 키워드를 골라서 그들의 값을 0으로 설정
    zero_indices = random.sample(range(12), random.randint(5, 8))
    for index in zero_indices:
        normalized_weights[index] = 0.0
    
    # 0이 아닌 값들의 총합을 계산하고 다시 분배
    remaining_value = 1 - sum(normalized_weights)
    non_zero_indices = [j for j in range(12) if j not in zero_indices]
    if non_zero_indices:  # 값이 0이 아닌 키워드가 있을 경우만 분배
        for j in non_zero_indices:
            normalized_weights[j] = round(normalized_weights[j] / sum(normalized_weights[j] for j in non_zero_indices) * remaining_value, 3)
    
    # 총합이 1이 되도록 조정
    final_total = sum(normalized_weights)
    if final_total != 1.0:
        difference = 1.0 - final_total
        # 가장 큰 값을 가진 인덱스를 찾아 미세 조정
        max_index = max(non_zero_indices, key=lambda k: normalized_weights[k])
        normalized_weights[max_index] = round(normalized_weights[max_index] + difference, 3)
    
    # 딕셔너리 형태로 구성
    data = {keywords[j]: normalized_weights[j] for j in range(12)}
    
    # 파일명 생성 및 파일 저장
    filename = f'selfie_ex_{i}.json'
    filepath = os.path.join(output_directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
