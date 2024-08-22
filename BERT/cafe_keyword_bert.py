import os
import json
from transformers import BertModel, BertTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity

from google.colab import drive
drive.mount('/content/drive')

# BERT 모델과 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# 임베딩 추출 함수
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()
    return embeddings

# 스타일별 키워드 리스트
style_keywords = {
    "캐주얼": [
        "다양한 메뉴", "편리한 위치", "작업하기 좋은 카페", "공부하기 좋은 카페", "친구", "편안한 분위기",
        "아늑함", "출근길", "모임", "아늑한", "여유로운", "인생 카페", "편안한", "공부", "저렴한",
        "휴식 공간", "햇살"
    ],
    "미니멀": [
        "깔끔한 인테리어", "모던한 분위기", "화이트 톤", "조용한 공간", "채광, 자연광", "핸드드립",
        "원두로스팅", "작업하기 좋은 카페", "공부하기 좋은 카페", "여유로운", "친절", "넓은", "쾌적한",
        "밝은", "플렌테리어", "청결한 매장", "비 오는 날", "더치커피"
    ],
    "걸리시": [
        "밝은 분위기", "달달한 음료", "포토스팟", "사진 찍기 넘 좋아요", "너무 예뻐요", "분홍색",
        "귀여운 디저트", "사진찍기 좋은", "애견동반", "딸기 케이크", "인스타그램", "복숭아", "케이크",
        "쇼핑", "하트", "상큼함", "딸기라떼", "예쁜 접시", "수다", "아기자기한", "상큼한", "달콤한",
        "쿠키", "메론소다", "수제 브라우니", "앙버터"
    ],
    "클래식": [
        "깔끔함", "차가 맛있는", "쾌적한", "고급스러운", "조용한", "깊고 진한", "직장", "원두 선택",
        "합리적", "여유로운", "성숙한", "고급스러움", "까눌레", "세련된", "갤러리", "향긋한 분위기",
        "다양한 차 종류", "다과", "건강한 재료"
    ],
    "시크": [
        "조용한", "깔끔한", "현대적인", "커피의 맛", "모던한", "깔끔한 맛", "세심한", "차분한",
        "크림 라떼", "원두", "진한", "로스팅 원두", "신선한 재료", "세련된", "향수", "갤러리"
    ],
    "고프코어": [
        "대화하기 좋은", "아늑한", "특별한", "모던한", "아인슈페너", "작업하기 좋은", "우드톤",
        "작은 카페", "개인카페", "협소한", "아지트", "아담한 매장", "크루아상", "스페셜티", "단골",
        "오트밀크"
    ],
    "스트릿": [
        "힙한 분위기", "독창적인", "루프탑", "국제적 분위기", "바 형태", "화려한", "네온", "LP",
        "검정색", "음악", "노키즈존"
    ],
    "워크웨어": [
        "베이커리", "풍부한 맛", "작업", "공부", "테이크아웃", "우드톤", "스탠딩"
    ],
    "스포티": [
        "힙한", "문화공간", "경기", "작업", "과제", "단백질", "제로칼로리", "디카페인", "샐러드", "건강한"
    ],
    "로맨틱": [
        "데이트", "사랑스러운", "루프탑", "달콤한", "부드러운", "친절한", "정성", "애견 동반",
        "라떼 아트", "부드러운 음악", "배려", "특별한 날", "샹들리에", "옥상테라스", "무화과 시나몬 스콘",
        "귀여운 비주얼", "프레지에", "친구", "브런치"
    ],
    "시티보이": [
        "부드러운 크림", "베이커리", "풍부한 맛", "재즈", "LP", "턴테이블", "모던", "숨겨진", "말차",
        "조용한", "독서", "여유로운 시간", "편안한 음악", "콜드브루", "깔끔한 분위기", "스페셜티",
        "핸드드립", "트렌디", "오트밀크"
    ],
    "레트로": [
        "빈티지한 분위기", "엔티크", "자연", "전통적", "따뜻한 인테리어", "화분", "우드톤 인테리어",
        "주택 개조", "공방", "후르츠 산도", "감성적인", "핫플", "개성약과", "구경하는 재미",
        "시끄러운", "돌채라떼", "트렌디", "포토존", "친구", "이국적인"
    ]
}

# 스타일 키워드를 하나의 문자열로 결합하여 임베딩 추출
style_embeddings = {style: get_embedding(" ".join(keywords)) for style, keywords in style_keywords.items()}

# JSON 파일 불러오기
with open('/content/drive/MyDrive/keyword_without_weight.json', 'r') as f:
    cafe_keywords = json.load(f)

# 카페별 키워드 임베딩과 스타일 키워드 임베딩의 유사도 계산
cafe_similarities = {}

for cafe, keywords in cafe_keywords.items():
    cafe_combined_keywords = " ".join(keywords)
    cafe_embedding = get_embedding(cafe_combined_keywords)

    similarities = {}
    for style, style_embedding in style_embeddings.items():
        similarity = cosine_similarity(cafe_embedding, style_embedding)[0][0]
        similarities[style] = float(similarity)  # float32를 float로 변환

    # 유사도 높은 순으로 정렬
    sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)

    # 카페 이름과 함께 결과 저장
    cafe_similarities[cafe] = sorted_similarities

# 결과 출력
for cafe, sorted_similarities in cafe_similarities.items():
    print(f"카페: {cafe}")
    for rank, (style, similarity) in enumerate(sorted_similarities, 1):
        print(f"  {rank}위: '{style}' 스타일과의 유사도: {similarity:.4f}")
    print("\n")

# 결과를 JSON 파일로 저장
output_file = '/content/drive/MyDrive/cafe_keyword_similarity_sorted_results.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(cafe_similarities, f, ensure_ascii=False, indent=4)

# 전체 카페 갯수 출력
total_cafes = len(cafe_similarities)
print(f"총 {total_cafes}개의 카페가 분석되었습니다.")
print(f"결과가 {output_file} 파일로 저장되었습니다.")