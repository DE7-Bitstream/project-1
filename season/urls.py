from django.urls import path
from . import views

app_name = 'season'
urlpatterns =[
    path('', views.index, name = 'season_index')
]