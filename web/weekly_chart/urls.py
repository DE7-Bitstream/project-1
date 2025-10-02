from django.urls import path
from . import views

app_name = 'weekly_chart'
urlpatterns = [
  path('', views.WeeklyChartView.as_view(), name='weekly_chart_index'),
]