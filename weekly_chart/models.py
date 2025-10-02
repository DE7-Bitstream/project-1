from django.db import models

class WeeklyChart(models.Model):
    rank = models.IntegerField()  # 순위
    year = models.IntegerField()  # 연도
    month = models.IntegerField()  # 월
    week_number_in_month = models.IntegerField()  # 월 내 주차
    song = models.CharField(max_length=255)  # 곡명
    artist = models.CharField(max_length=255)  # 아티스트명

    def __str__(self):
        return f"{self.year} Y {self.month} M {self.week_number_in_month} W - {self.rank} - {self.song} by {self.artist}"