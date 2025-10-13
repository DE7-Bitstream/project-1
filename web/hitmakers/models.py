from django.db import models

class Creator(models.Model):
    creator_id = models.CharField(max_length=64, unique=True) 
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.creator_id})"


class Album(models.Model):
    album_id = models.CharField(max_length=64, unique=True)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    distributor = models.CharField(max_length=255)
    entertainment = models.CharField(max_length=255) 

    def __str__(self):
        return f"{self.album_id} - {self.entertainment}"


class Song(models.Model):
    song_id = models.CharField(max_length=64, unique=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    singer = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    creators = models.ManyToManyField(Creator, through='SongCreator', related_name='songs')

    def __str__(self):
        return f"곡 ID : {self.song_id} / 가수 : {self.singer} / 제목 : {self.title}"


class SongCreator(models.Model):
    ROLE_COMPOSER = "composer"
    ROLE_LYRICIST = "lyricist"
    ROLE_ARRANGER = "arranger"
    ROLE_CHOICES = [
        (ROLE_COMPOSER, "Composer"),
        (ROLE_LYRICIST, "Lyricist"),
        (ROLE_ARRANGER, "Arranger"),
    ]

    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="song_creators")
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name="creator_songs")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['song', 'creator', 'role'], name='unique_song_creator_role')
        ]


class YearlyChart(models.Model):
    year = models.IntegerField(db_index=True)
    rank = models.IntegerField()
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="yearly_charts")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='yearly_charts')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'song'], name='unique_year_song')
        ]
        indexes = [
            models.Index(fields=["year", "rank"]),
            models.Index(fields=["year", "song"]),
        ]

    def __str__(self):
        return f"{self.year} 년도 {self.rank} 위 ) {self.song.singer} - {self.song.title}"
