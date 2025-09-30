from django.shortcuts import render
from django.views import View

class WeeklyChartView(View):
    def get(self, request):
        return render(request, 'weekly_chart/weekly_chart.html', {})