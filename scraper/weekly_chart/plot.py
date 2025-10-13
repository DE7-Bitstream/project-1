import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from __init__ import *

# 한글 폰트 설정 (MacOS 기준)
matplotlib.rcParams['font.family'] = 'AppleGothic'
matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# CSV 불러오기
df = pd.read_csv(f"{CSV_DIR}/melon_chart_weekly_2024.csv")

# Top 10 곡만 선택
df = df[df['rank'] <= 10]

# 7월 데이터만 선택
df_july = df[df['month'] == 7]

# x축 라벨 생성 (week_number_in_month 기준)
df_july['week_label'] = df_july['week_number_in_month'].astype(str)

# 연도별로 그래프 생성
years = df_july['year'].unique()
for year in years:
    year_df = df_july[df_july['year'] == year]
    
    plt.figure(figsize=(12, 6))
    plt.title(f"{year}년도 7월 주간 차트 Top 10 Rank 변동")
    plt.xlabel("주차")
    plt.ylabel("등수")
    plt.gca().invert_yaxis()  # 1위가 위로 오도록
    
    # 곡별로 라인 그리기
    for song in year_df['song_name'].unique():
        song_df = year_df[year_df['song_name'] == song]
        plt.plot(song_df['week_label'], song_df['rank'], marker='o', label=song)
        # rank 정수로 표시
        for x, y in zip(song_df['week_label'], song_df['rank']):
            plt.text(x, y, str(int(y)), fontsize=8, ha='center', va='bottom')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # 곡명이 많으면 그래프 바깥으로
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
