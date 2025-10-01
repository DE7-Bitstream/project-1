from django.shortcuts import render
from django.views import View
from .models import WeeklyChart
from collections import defaultdict

class WeeklyChartView(View):
    def get(self, request):
        # GET 파라미터
        start_year = int(request.GET.get("start_year", 2025))
        start_month = int(request.GET.get("start_month", 1))
        end_year = int(request.GET.get("end_year", 2025))
        end_month = int(request.GET.get("end_month", 2))
        max_rank = int(request.GET.get("max_rank", 10))  # 서버에서 최대 표시 rank 제한
            

        # 데이터 필터링
        data = WeeklyChart.objects.filter(
            rank__lte=max_rank  # max_rank 이하
        ).filter(
            year__gt=start_year # 시작 연도 이후
        ) | WeeklyChart.objects.filter(
            rank__lte=max_rank,
            year=start_year,
            month__gte=start_month # 시작 연도, 월 이후
        )
        data = data.filter(
            year__lt=end_year # 종료 연도 이전
        ) | data.filter(
            year=end_year, 
            month__lte=end_month # 종료 연도, 월 이전
        )

        data = data.order_by('year', 'month', 'week_number_in_month', 'rank')

        # 곡별 데이터 구조화
        song_data = defaultdict(lambda: {"x": [], "y": [], "artist": ""})
        for entry in data:
            week_label = f"{entry.year}-{entry.month}월 {entry.week_number_in_month}주차"
            song_data[entry.song]["x"].append(week_label)
            song_data[entry.song]["y"].append(entry.rank)
            song_data[entry.song]["artist"] = entry.artist

        context = {
            "song_data": song_data,
            "start_year": start_year,
            "start_month": start_month,
            "end_year": end_year,
            "end_month": end_month,
            "max_rank": max_rank,
            "year_list": list(range(2020, 2026)),
            "month_list": list(range(1, 13)),
        }
        return render(request, "weekly_chart/weekly_chart.html", context)
