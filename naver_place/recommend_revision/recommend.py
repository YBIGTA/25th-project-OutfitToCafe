import json
import os
from evaluation import calculate_score

# 셀카 분석 파일 경로 설정
selfie_file_path = 'C:/Users/lgsc0/Desktop/신기플/classification_results.json' #추후 상황에 맞게 변경

# 분석값 로드
if os.path.exists(selfie_file_path):
    print(f"파일을 확인했습니다: {selfie_file_path}")
    # 파일을 열어서 데이터를 읽어옴
    with open(selfie_file_path, 'r', encoding='utf-8') as file:
        selfie_data = json.load(file)
        print("파일을 불러왔습니다.")
else:
    print("파일을 찾을 수 없습니다.")
    exit()

# cafe_vectorize 파일 로드
cafe_vectorize = 'C:/Users/lgsc0/Desktop/신기플/cafe_vector.json' # 필요시 경로 설정 수정
with open(cafe_vectorize, 'r', encoding='utf-8') as f:
    cafe_avg_data = json.load(f)

# 동점 카페 순위 가리기 위해 가중치가 가장 높은 keyword 변수 설정
max_keyword = max(selfie_data, key=selfie_data.get)

# cafe 점수 저장할 슬롯
cafe_scores = {}

# evalutaion.py를 활용하여 카페 evaluation 진행
for cafe_name, cafe_data in cafe_avg_data.items():
    score = calculate_score(cafe_data, selfie_data)
    cafe_scores[cafe_name] = score

# 점수에 따라 카페를 정렬하고 상위 카페를 추천
top_cafes = sorted(cafe_scores.items(), key=lambda item: item[1], reverse=True)

# 동점 처리 -> 위에서 정의한 max_keyword의 value로 추가 정렬
final_recommendations = []
i = 0
while i < len(top_cafes):
    same_score_group = [top_cafes[i]]
    while i + 1 < len(top_cafes) and top_cafes[i][1] == top_cafes[i + 1][1]:
        same_score_group.append(top_cafes[i + 1])
        i += 1
    
    if len(same_score_group) > 1:
        same_score_group.sort(key=lambda x: cafe_avg_data[x[0]][max_keyword], reverse=True)
    
    final_recommendations.extend(same_score_group)
    i += 1

# "순위, 카페, 점수" 리스트 생성 
good_cafe = []
for rank, (cafe_name, score) in enumerate(final_recommendations[:3], start=1):
    good_cafe.append({
        'Rank': rank,
        'Cafe': cafe_name,
        'Score': score
    })

recommendations = {
    'selfie_file': selfie_file_path,
    'recommendations': good_cafe
}

# 추천 결과를 recommend.json 파일로 저장
output_file = 'C:/Users/lgsc0/Desktop/신기플/recommend.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(recommendations, f, ensure_ascii=False, indent=4)

print("카페 추천이 완료됐습니다")
