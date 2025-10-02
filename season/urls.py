from django.urls import path
from . import views
from .views import SpringView, SummerView, FallView, WinterView

app_name = 'season'
urlpatterns =[
    path('', views.index, name = 'season_index'),
    path('spring/', SpringView.as_view(), name = 'season_spring'),
    path('summer/', SummerView.as_view(), name = 'season_summer'),
    path('fall/', FallView.as_view(), name = 'season_fall'),
    path('winter/', WinterView.as_view(), name = 'season_winter'),
]