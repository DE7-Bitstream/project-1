from django.conf import settings

import os
import pandas as pd

TOP3_SONGS_IN_GENRE_PATH = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top3_songs_in_genre.csv')
TOP5_GENRE = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top5_genre_count.csv')
TOP10_COUNT = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top10_count.csv')
TOP10_RANK = os.path.join(settings.SEASON_DATAFRAME_DIR, 'every_season_top10_rank.csv')

def top5_chart_in(season):
    df = pd.read_csv(TOP10_COUNT)
    if season == 'spring':
        df = df[df['계절'] == '봄']
    elif season == 'summer':
        df = df[df['계절'] == '여름']
    elif season == 'fall':
        df = df[df['계절'] == '가을']
    elif season == 'winter':
        df = df[df['계절'] == '겨울']

    song_name = df['곡명'].tolist()[:5]
    chart_in_count = df['count'].tolist()[:5]

    return song_name, chart_in_count