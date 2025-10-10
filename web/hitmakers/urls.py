from django.urls import path
from . import views

app_name = 'hitmakers'
urlpatterns = [
    path('', views.chart_view, name='hitmakers_index'),
    path('api/chart-data/', views.get_chart_data, name='chart_data'),
    path('api/top-songs/', views.get_top_songs, name='top_songs'),
]

