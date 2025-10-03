from django.conf import settings

import os
import pandas as pd
import numpy as np

TOP3_SONGS_IN_GENRE_PATH = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top3_songs_in_genre.csv')
TOP5_GENRE = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top5_genre_count.csv')
TOP10_COUNT = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top10_count.csv')
TOP10_RANK = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top10_rank.csv')

SPRING_COLORS = [
    'rgba(255, 255, 153, 0.75)',
    'rgba(152, 255, 152, 0.75)',
    'rgba(173, 216, 230, 0.75)',
    'rgba(221, 160, 221, 0.75)',
    'rgba(255, 192, 203, 0.75)',
]

def get_main_chart(season):
    df_top5 = pd.read_csv(TOP10_COUNT)
    df_top5_rank = pd.read_csv(TOP10_RANK)

    if season == 'spring':
        df_top5 = df_top5[df_top5['계절'] == '봄']
        df_top5_rank = df_top5_rank[df_top5_rank['계절'] == '봄']
    elif season == 'summer':
        df_top5 = df_top5[df_top5['계절'] == '여름']
        df_top5_rank = df_top5_rank[df_top5_rank['계절'] == '여름']
    elif season == 'fall':
        df_top5 = df_top5[df_top5['계절'] == '가을']
        df_top5_rank = df_top5_rank[df_top5_rank['계절'] == '가을']
    else:
        df_top5 = df_top5[df_top5['계절'] == '겨울']
        df_top5_rank = df_top5_rank[df_top5_rank['계절'] == '겨울']

    top5_song_name = df_top5['곡명'].tolist()[:5]
    top5_chart_in_count = df_top5['count'].tolist()[:5]

    df_top5_rank['연_월'] = df_top5_rank['Year'].apply(str) + '_' + df_top5_rank['Month'].apply(lambda x : '0' + str(x) if x < 10 else str(x))
    df_top5_rank = df_top5_rank[df_top5_rank['곡명'].isin(top5_song_name)]
    df_top5_rank = df_top5_rank.pivot_table(index = '연_월', columns = '곡명', values = '순위')
    top5_rank_labels = df_top5_rank.index.to_list()
    top5_rank = []
    for i in top5_song_name:
        not_available = True
        ranking = []
        for j in df_top5_rank[i].to_list():
            if pd.isna(j) and not_available:
                ranking.append(-25)
            elif pd.isna(j):
                ranking.append(125)
            else:
                ranking.append(j)
                not_available = False
        top5_rank.append({'label' : i, 'data' : ranking, 'fill' : False})

    return top5_song_name, top5_chart_in_count, top5_rank_labels, top5_rank