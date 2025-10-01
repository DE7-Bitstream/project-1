from django.shortcuts import render
from django.views import View
from .models import WeeklyChart
from collections import defaultdict

class WeeklyChartView(View):
    def get(self, request):
        # GET 파라미터
        start_month = int(request.GET.get("start_month", 1))
        start_week = int(request.GET.get("start_week", 1))
        end_month = int(request.GET.get("end_month", 1))
        end_week = int(request.GET.get("end_week", 5))
        max_rank = int(request.GET.get("max_rank", 5))
        year = int(request.GET.get("year", 2020))

        # 월별 최대 주차 계산
        month_max_week = {}
        for m in range(1, 13):
            max_week_entry = WeeklyChart.objects.filter(year=year, month=m).order_by('-week_number_in_month').first()
            month_max_week[m] = max_week_entry.week_number_in_month if max_week_entry else 5

        # 데이터 필터링
        data = WeeklyChart.objects.filter(
            year=year,
            month__gte=start_month,
            month__lte=end_month,
            week_number_in_month__gte=start_week,
            week_number_in_month__lte=end_week,
            rank__lte=max_rank
        ).order_by('month', 'week_number_in_month', 'rank')

        # 곡별 데이터 구조화
        song_data = defaultdict(lambda: {"x": [], "y": []})
        for entry in data:
            week_label = f"{entry.month}월 {entry.week_number_in_month}주차"
            song_data[entry.song]["x"].append(week_label)
            song_data[entry.song]["y"].append(entry.rank)

        context = {
            "song_data": song_data,
            "year": year,
            "max_rank": max_rank,
            "start_month": start_month,
            "start_week": start_week,
            "end_month": end_month,
            "end_week": end_week,
            "year_list": list(range(2020, 2026)),
            "month_list": list(range(1, 13)),
            "month_max_week": month_max_week,
        }
        return render(request, "weekly_chart/weekly_chart.html", context)
