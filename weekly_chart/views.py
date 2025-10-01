from django.shortcuts import render
from django.views import View
from .models import WeeklyChart
from collections import defaultdict

class WeeklyChartView(View):
    def get(self, request):
        year = 2020
        month = 1
        data = WeeklyChart.objects.filter(year=year, month=month, rank__lte=5).order_by('week_number_in_month', 'rank')

        song_data = defaultdict(lambda: {"x": [], "y": []})
        for entry in data:
            week_label = f"{month}월 {entry.week_number_in_month}주차"
            song_data[entry.song]["x"].append(week_label)
            song_data[entry.song]["y"].append(entry.rank)

        context = {
            "song_data": song_data,
        }
        return render(request, "weekly_chart/weekly_chart.html", context)
