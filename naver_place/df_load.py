import pandas as pd

# 파일 경로
file_path = 'C:/Users/lgsc0/Downloads/카페별스타일_countvect.csv'

# 파일을 ISO-8859-1 인코딩으로 읽기
df = pd.read_csv(file_path, encoding='utf-8')

# 데이터 확인 (선택 사항)
print(df.head())

# 출력 파일 경로 설정
output_path = 'C:/Users/lgsc0/Desktop/신기플/cafe_avg.csv'

# DataFrame을 새로운 CSV 파일로 저장
df.to_csv(output_path, encoding='utf-8-sig', index=False)

print(f"파일이 성공적으로 저장되었습니다: {output_path}")