import torch
from transformers import AutoTokenizer, AutoModel
import os
from sklearn.metrics.pairwise import cosine_similarity

# KoBERT 토크나이저와 모델 로드
tokenizer = AutoTokenizer.from_pretrained('skt/kobert-base-v1')
model = AutoModel.from_pretrained('skt/kobert-base-v1')

# BERT 임베딩 생성 함수
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    
    # Ensure token_type_ids are within bounds
    if 'token_type_ids' in inputs:
        inputs['token_type_ids'] = torch.zeros_like(inputs['input_ids'])

    with torch.no_grad():
        outputs = model(**inputs)

    # [CLS] 토큰의 벡터 추출
    return outputs.last_hidden_state[:, 0, :].numpy()

# # 테스트용 코드
# text = "한국어 모델을 테스트합니다."
# embedding = get_bert_embedding(text)
# print(embedding)

# 모든 파일 가져오기 
def get_all_file_lists(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
