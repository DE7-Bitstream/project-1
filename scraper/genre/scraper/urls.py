from django.urls import path
from .. import views

app_name = 'lyrics_analyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/<str:genre>/', views.analyze_genre, name='analyze_genre'),
    path('scrape/', views.scrape_songs, name='scrape_songs'),
]