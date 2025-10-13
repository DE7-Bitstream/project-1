from django.db import models

from season.models import GenreCount, TopSongs, SongImage

def select_season(queryset, season):
    season_map = {
        'spring': '봄',
        'summer': '여름',
        'fall': '가을',
        'winter': '겨울'
    }
    
    return queryset.filter(season = season_map.get(season))



def select_genre(queryset, genre):
    genre_map = {
        '록/메탈': '록/메탈',
        'POP': 'POP',
        '랩/힙합': '랩/힙합',
        '발라드': '발라드',
        '댄스': '댄스',
        '국내드라마': '국내드라마'
    }

    return queryset.filter(genre = genre_map.get(genre))



def get_pie_chart(season):
    qs = GenreCount.objects.all()
    qs = select_season(qs, season)

    top5_genre = [g.genre for g in qs]
    top5_selector = top5_genre.copy()
    top5_genre = top5_genre + ['']
    top5_genre_count = [g.genre_count for g in qs]
    top5_genre_count = top5_genre_count + [1500 - sum(top5_genre_count)]

    return top5_genre, top5_genre_count, top5_selector



def get_bar_chart(season, genre):
    qs = TopSongs.objects.all()
    qs = select_season(qs, season)
    qs = select_genre(qs, genre)
    
    images_dict = {
        img.song_name : img.album_url
        for img in SongImage.objects.filter(song_name__in = [i.song_name for i in qs])
    }

    top3_song_names = []
    top3_song_counts = []
    top3_song_images = []
    for i in qs:
        top3_song_names.append(i.song_name)
        top3_song_counts.append(i.chart_count)
        top3_song_images.append(images_dict.get(i.song_name, "https://placehold.co/150x150"))

    return top3_song_names, top3_song_counts, top3_song_images



def get_line_chart(season):
    pass