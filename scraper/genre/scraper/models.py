from django.db import models

class Genre(models.Model):
    GENRE_CHOICES = [
        ('hiphop', '힙합'),
        ('indie_rock', '인디/락'),
        ('kpop', 'K-POP'),
    ]
    
    name = models.CharField(max_length=20, choices=GENRE_CHOICES, unique=True)
    display_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = '장르'
        verbose_name_plural = '장르들'


class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name='음반명')
    artist = models.CharField(max_length=200, verbose_name='아티스트')
    year = models.IntegerField(verbose_name='연도')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='albums')
    
    def __str__(self):
        return f"{self.title} - {self.artist}"
    
    class Meta:
        verbose_name = '음반'
        verbose_name_plural = '음반들'


class Song(models.Model):
    title = models.CharField(max_length=200, verbose_name='곡명')
    artist = models.CharField(max_length=200, verbose_name='아티스트')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='songs')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='songs')
    lyrics = models.TextField(verbose_name='가사', blank=True)
    year = models.IntegerField(verbose_name='연도', null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.artist}"
    
    class Meta:
        verbose_name = '곡'
        verbose_name_plural = '곡들'


class WordFrequency(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='word_frequencies')
    word = models.CharField(max_length=100, verbose_name='단어')
    frequency = models.IntegerField(verbose_name='빈도수')
    pos = models.CharField(max_length=10, verbose_name='품사', default='명사')
    
    def __str__(self):
        return f"{self.word} ({self.frequency})"
    
    class Meta:
        verbose_name = '단어 빈도'
        verbose_name_plural = '단어 빈도들'
        unique_together = ['genre', 'word', 'pos']  