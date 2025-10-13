from django.shortcuts import render
from django.views import View
from .models import WeeklyChart
from collections import defaultdict

class WeeklyChartView(View):
    def get_data(self, start_year, start_month, end_year, end_month, max_rank):
        '''
        주어진 기간과 랭킹 조건에 맞는 데이터를 쿼리
        '''
        data = WeeklyChart.objects.filter(rank__lte=max_rank) # max_rank 이하 데이터
        data = data.filter(year__gt=start_year) | WeeklyChart.objects.filter(
            rank__lte=max_rank, year=start_year, month__gte=start_month
        ) # start_year, start_month 이후 데이터
        data = data.filter(year__lt=end_year) | data.filter(
            year=end_year, month__lte=end_month
        ) # end_year, end_month 이전 데이터

        data = data.order_by("year", "month", "week_number_in_month", "rank")

        # 곡별 데이터 구조화
        song_data = defaultdict(lambda: {"x": [], "y": [], "artist": ""})
        for entry in data:
            week_label = f"{entry.year}-{entry.month}월 {entry.week_number_in_month}주차"
            song_data[entry.song]["x"].append(week_label)
            song_data[entry.song]["y"].append(entry.rank)
            song_data[entry.song]["artist"] = entry.artist

        return song_data
    
    # GET 요청
    def get(self, request):
        # 초기 화면 (기본값)
        start_year = 2025
        start_month = 8
        end_year = 2025
        end_month = 9
        max_rank = 10

        song_data = self.get_data(start_year, start_month, end_year, end_month, max_rank)
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

    # POST 요청
    def post(self, request): 
        start_year = int(request.POST.get("start_year", 2025))
        start_month = int(request.POST.get("start_month", 8))
        end_year = int(request.POST.get("end_year", 2025))
        end_month = int(request.POST.get("end_month", 9))
        max_rank = int(request.POST.get("max_rank", 10))

        song_data = self.get_data(start_year, start_month, end_year, end_month, max_rank)
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
