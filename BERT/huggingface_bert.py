from transformers import BertModel, BertTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# BERT 모델과 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# 텍스트와 키워드 리스트
text = """
성수동에 위치한 카페 "오푸"는 독특한 디저트와 아늑한 분위기로 많은 방문객들의 사랑을 받고 있습니다. 
이 카페의 시그니처 메뉴인 소파 모양의 디저트는 시각적으로도 매력적이며, 아이스크림 케이크 형태로 제공되어 색다른 경험을 선사합니다. 
디저트 안에는 딸기 맛이 들어 있어 상큼함을 더하며, 소파의 크림 부분은 약간 느끼할 수 있어 다른 음료와의 조화를 추천합니다. 
음료 또한 다양하고 맛있습니다. 특히 오푸라떼와 트러플 라떼는 독특한 조합으로 많은 호평을 받고 있으며, 
밤라떼는 달콤한 맛이 일품으로, 커피 애호가들에게 적합한 선택입니다. 공간은 넓고 인테리어가 감각적이며, 
쾌적한 환경을 제공해 여유롭게 즐길 수 있는 분위기를 자아냅니다. 친절한 직원들과 함께하는 이 카페는 
인스타그램에서도 화제를 모으고 있어 포토존으로도 인기가 많습니다. 전반적으로 "오푸"는 독특한 디저트와 맛있는 음료, 
아늑한 분위기가 어우러져 특별한 시간을 보낼 수 있는 곳으로, 한 번 방문해 볼 만한 가치가 있습니다.
"""

keywords = ["저는 주로 귀여운 스타일의 옷을 입습니다", 
            "커피를 정말 좋아합니다", 
            "나는 프리미엄 커피를 마시고, 커피 맛이 정말 중요해.", 
            "올블랙 옷을 입었다 ㅋ", 
            "나 우유맛 아이스크림이 먹고 싶어", 
            "피자 땡긴다", 
            "캐주얼", 
            "오늘 옷 스타일이 스포티하네", 
            "조용한 카페에서 공부하고 싶어", 
            "스트릿", 
            "로맨틱", 
            "시티보이", 
            "레트로"]
            
# BERT 임베딩 생성 함수
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # [CLS] 토큰의 벡터 추출
    return outputs.last_hidden_state[:, 0, :].numpy()

# 텍스트와 키워드들에 대해 BERT 임베딩 생성
text_embedding = get_bert_embedding(text)
keyword_embeddings = [get_bert_embedding(keyword) for keyword in keywords]

# 코사인 유사도 계산
cosine_similarities = [cosine_similarity(text_embedding, keyword_embedding).flatten()[0] for keyword_embedding in keyword_embeddings]

# 유사도 결과를 데이터프레임으로 저장
similarity_df = pd.DataFrame({'keyword': keywords, 'similarity': cosine_similarities})

# 유사도 결과 출력 (소수점 6자리 포맷팅 적용)
similarity_df['similarity'] = similarity_df['similarity'].apply(lambda x: f'{x:.6f}')

print(similarity_df)