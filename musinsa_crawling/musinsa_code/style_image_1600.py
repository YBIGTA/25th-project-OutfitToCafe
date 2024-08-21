import os
import shutil
from PIL import Image

# 원본 이미지 파일이 들어있는 폴더 경로를 지정합니다.
source_folder_path = '/Users/macbook/Documents/YBIGTA_24_SUMMER_PROJECT/musinsa_crawling/musinsa_image/{스타일}'

# 이미지를 복사할 대상 폴더 경로를 지정합니다.
destination_folder_path = '/Users/macbook/Documents/YBIGTA_24_SUMMER_PROJECT/musinsa_crawling/musinsa_image/{스타일}_1600'

# 대상 폴더가 존재하지 않으면 생성합니다.
os.makedirs(destination_folder_path, exist_ok=True)

# 원본 폴더 내의 모든 jpg 파일 경로를 가져옵니다.
image_files = [os.path.join(source_folder_path, f) for f in os.listdir(source_folder_path) if f.endswith('.jpg')]

# 파일을 생성된 날짜 순으로 정렬합니다.
image_files.sort(key=lambda x: os.path.getctime(x))

# 최대 1600장의 이미지만 가져옵니다.
image_files = image_files[:1600]

# 이미지를 대상 폴더로 복사합니다.
for image_file in image_files:
    shutil.copy(image_file, destination_folder_path)

print(f'Total number of images copied: {len(image_files)}')
