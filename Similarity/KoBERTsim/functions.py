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

# 모든 파일 가져오기 
def get_all_file_lists(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# jaccard 유사도 계산
def jaccard_similarity(set1, set2):
    # 집합으로 변환
    set1 = set(set1) if isinstance(set1, str) else set1
    set2 = set(set2) if isinstance(set2, str) else set2

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0.0
    return intersection / union


