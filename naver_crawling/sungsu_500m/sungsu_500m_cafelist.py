import pandas as pd
data = pd.read_csv('./소상공인시장진흥공단_상가(상권)정보_서울_202403.csv')

df = data[data['상권업종소분류명'] == '카페']
len(df)

import pandas as pd
from math import radians, cos, sin, sqrt, atan2

# 기준 위도와 경도 (성수역의 위경도)
reference_lat = 37.54431924314278
reference_lon = 127.05643116143955

# Haversine 공식 사용
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구의 반경 (km)
    
    # 위도와 경도를 라디안으로 변환
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # 위도와 경도의 차이 계산
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine 공식 적용
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c * 1000  # 거리 (m)로 변환
    
    return distance

# 각 카페와 기준점 사이의 거리 계산
df['distance'] = df.apply(lambda row: haversine(reference_lat, reference_lon, row['위도'], row['경도']), axis=1)

# Nm 내의 카페 필터링
N = 500
filtered_cafes = df[df['distance'] <= N]


# 결과 출력
print(filtered_cafes['상호명'])