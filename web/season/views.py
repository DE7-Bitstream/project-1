from django.shortcuts import render
from django.views import generic
from .data_processor import get_main_chart

# Create your views here.
def index(request):
    return render(request, 'season/season_index.html')

class SpringView(generic.TemplateView):
    template_name = 'season/season_spring.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 여기에 차트 데이터 추가
        top5_song_name, top5_chart_in_count, top5_rank_labels, top5_rank = get_main_chart('spring')
        context['top5_song_name'] = top5_song_name
        context['top5_chart_in_count'] = top5_chart_in_count
        context['top5_rank_labels'] = top5_rank_labels
        context['top5_rank'] = top5_rank
        return context
    
class SummerView(generic.TemplateView):
    template_name = 'season/season_summer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 여기에 차트 데이터 추가
        return context
    
class FallView(generic.TemplateView):
    template_name = 'season/season_fall.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 여기에 차트 데이터 추가
        return context
    
class WinterView(generic.TemplateView):
    template_name = 'season/season_winter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 여기에 차트 데이터 추가
        return context