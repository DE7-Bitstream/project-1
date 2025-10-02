from django.urls import path
from . import views

urlpatterns = [
  path('', views.WeeklyChartView.as_view(), name='weekly_chart'),
]