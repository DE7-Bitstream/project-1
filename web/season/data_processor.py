from django.conf import settings

import os
import pandas as pd

TOP3_SONGS_IN_GENRE_PATH = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top3_songs_in_genre.csv')
TOP5_GENRE = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top5_genre_count.csv')
TOP10_COUNT = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top10_count.csv')
TOP10_RANK = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top10_rank.csv')

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
