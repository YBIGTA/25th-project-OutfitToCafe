# Python 이미지 사용
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR /code

# 필요한 패키지 설치
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY . /code/
