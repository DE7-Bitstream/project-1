from django.db import models

# Create your models here.
class GenreCount(models.Model):
    genre = models.CharField(max_length = 20)
    genre_count = models.IntegerField()
    season = models.CharField(max_length = 10)

    def __str__(self):
        return f'genre : {self.genre} genre_count : {self.genre_count} season : {self.season}'

class TopSongs(models.Model):
    genre = models.CharField(max_length = 100)
    song_name = models.CharField(max_length = 100)
    chart_count = models.IntegerField()
    season = models.CharField(max_length = 10)

    def __str__(self):
        return f'genre : {self.genre} song_name : {self.song_name} chart_count : {self.chart_count} season : {self.season}'

class SongImage(models.Model):
    song_name = models.CharField(max_length = 100)
    album_url = models.CharField(max_length = 200)

    def __str__(self):
        return f'song_name : {self.song_name} album_url : {self.album_url}'