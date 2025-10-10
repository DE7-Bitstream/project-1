from django.conf import settings

import os
import pandas as pd
import numpy as np

TOP3_SONGS_IN_GENRE = os.path.join(settings.SEASON_DATAFRAME_DIR, 'all_season_top3_songs_in_genre.csv')
TOP5_GENRE = os.path.join(settings.SEASON_DATAFRAME_DIR, 'all_season_top5_genre_count.csv')
TOP10_COUNT = os.path.join(settings.SEASON_DATAFRAME_DIR, 'all_season_top10_count.csv')
TOP10_RANK = os.path.join(settings.SEASON_DATAFRAME_DIR, 'all_season_top10_rank.csv')

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



def get_main_chart(season):
    df_top5 = pd.read_csv(TOP10_COUNT)
    df_top5_rank = pd.read_csv(TOP10_RANK)

    df_top5 = select_season(df_top5, season)
    df_top5_rank = select_season(df_top5_rank, season)

    top5_song_name = df_top5['곡명'].tolist()[:5]
    top5_chart_in_count = df_top5['count'].tolist()[:5]

    df_top5_rank['연_월'] = df_top5_rank['Year'].apply(str) + '_' + df_top5_rank['Month'].apply(lambda x : '0' + str(x) if x < 10 else str(x))
    df_top5_rank = df_top5_rank[df_top5_rank['곡명'].isin(top5_song_name)]
    df_top5_rank = df_top5_rank.pivot_table(index = '연_월', columns = '곡명', values = '순위')
    top5_rank_labels = df_top5_rank.index.to_list()
    top5_rank = []
    for idx, i in enumerate(top5_song_name):
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
        top5_rank.append({'label' : i,
                          'data' : ranking,
                          'fill' : False,
                          'borderColor' : COLORS[idx],
                          'backgroundColor' : COLORS[idx]})

    return top5_song_name, top5_chart_in_count, top5_rank_labels, top5_rank