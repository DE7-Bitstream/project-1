from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='lyrics_index'),
    path('wordcloud/', views.wordcloud_view, name='wordcloud'),
    path('analysis/', views.analysis_view, name='analysis'),
]