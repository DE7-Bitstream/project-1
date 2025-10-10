import csv, os

from django.core.management.base import BaseCommand

from season.models import GenreCount, TopSongs, SongImage

BASE_PATH = os.path.join('dataframes', 'season')

class Command(BaseCommand):
    def handle(self, *args, **options):
        # GenreCount
        path = os.path.join(BASE_PATH, 'all_season_top5_genre_count.csv')
        with open(path, encoding = 'utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                genre = row['장르']
                if '드라마' in genre:
                    genre = '국내드라마'

                GenreCount.objects.update_or_create(
                    genre = genre,
                    season = row['계절'],
                    genre_count = row['count']
                )

        # TopSongs
        path = os.path.join(BASE_PATH, 'all_season_top3_songs_in_genre.csv')
        with open(path, encoding = 'utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                genre = row['장르']
                if '드라마' in genre:
                    genre = '국내드라마'

                TopSongs.objects.update_or_create(
                    genre = genre,
                    song_name = row['곡명'],
                    season = row['계절'],
                    chart_count = row['count']
                )

        # SongImage
        path = os.path.join(BASE_PATH, 'album_url.csv')
        with open(path, encoding = 'utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                SongImage.objects.update_or_create(
                    song_name = row['곡명'],
                    album_url = row['주소']
                )

        self.stdout.write(self.style.SUCCESS('모든 데이터 등록 완료'))