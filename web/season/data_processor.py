from django.conf import settings

import os
import pandas as pd
import numpy as np

TOP3_SONGS_IN_GENRE = os.path.join(settings.SEASON_DATAFRAME_DIR, 'all_season_top3_songs_in_genre.csv')
TOP5_GENRE = os.path.join(settings.SEASON_DATAFRAME_DIR, 'all_season_top5_genre_count.csv')

COLORS = [
    'rgba(255, 205, 86, 0.5)',
    'rgba(75, 192, 192, 0.5)',
    'rgba(54, 162, 235, 0.5)',
    'rgba(153, 102, 255, 0.5)',
    'rgba(255, 99, 132, 0.5)',
]

def select_season(df, season):
    if '장르' in df:
        df['장르'] = df['장르'].apply(lambda x : '국내드라마' if '드라마' in x else x)

    if season == 'spring':
        df = df[df['계절'] == '봄']
    elif season == 'summer':
        df = df[df['계절'] == '여름']
    elif season == 'fall':
        df = df[df['계절'] == '가을']
    else:
        df = df[df['계절'] == '겨울']

    return df



def select_genre(df, genre):
    if genre == '록/메탈':
        df = df[df['장르'] == '록/메탈']
    elif genre == 'POP':
        df = df[df['장르'] == 'POP']
    elif genre == '랩/힙합':
        df = df[df['장르'] == '랩/힙합']
    elif genre == '발라드':
        df = df[df['장르'] == '발라드']
    elif genre == '댄스':
        df = df[df['장르'] == '댄스']
    else:
        df = df[df['장르'] == '국내드라마']

    return df



def get_pie_chart(season):
    df_top5_genre = pd.read_csv(TOP5_GENRE)
    df_top5_genre = select_season(df_top5_genre, season)

    top5_genre = df_top5_genre['장르'].tolist()
    top5_genre = top5_genre + ['']
    top5_selector = df_top5_genre['장르'].tolist()
    top5_genre_count = df_top5_genre['count'].tolist()
    top5_genre_count = top5_genre_count + [1500 - sum(top5_genre_count)]

    return top5_genre, top5_genre_count, top5_selector



def get_bar_chart(season, genre):
    df_season_genre_top3 = pd.read_csv(TOP3_SONGS_IN_GENRE)
    df_season_genre_top3 = select_season(df_season_genre_top3, season)
    df_season_genre_top3 = select_genre(df_season_genre_top3, genre)

    top3_song_names = df_season_genre_top3['곡명'].tolist()
    top3_song_counts = df_season_genre_top3['count'].tolist()

    return top3_song_names, top3_song_counts



def get_line_chart(season):
    pass