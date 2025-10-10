from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from .data_processor import get_pie_chart, get_bar_chart

# Create your views here.
def index(request):
    return render(request, 'season/season_index.html')

class SpringView(generic.TemplateView):
    template_name = 'season/season_spring.html'
    season = 'spring'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 여기에 차트 데이터 추가
        top5_genre, top5_genre_count, top5_selector = get_pie_chart(self.season)
        context['top5_genre'] = top5_genre
        context['top5_genre_count'] = top5_genre_count
        context['top5_selector'] = top5_selector

        # 초기값
        selected_genre = self.request.GET.get('genre', '댄스')
        top3_song_names, top3_song_counts = get_bar_chart(self.season, '댄스')
        context['top3_songs'] = list(zip(top3_song_names, top3_song_counts))
        context['selected_genre'] = '댄스'

        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('ajax') == '1':
            selected_genre = self.request.GET.get('genre', '댄스')
            top3_song_names, top3_song_counts = get_bar_chart(self.season, selected_genre)
            context['top3_songs'] = list(zip(top3_song_names, top3_song_counts))
            context['selected_genre'] = selected_genre

            return JsonResponse({'top3_songs' : context['top3_songs']})

        return super().render_to_response(context, **response_kwargs)
    
    
class SummerView(generic.TemplateView):
    template_name = 'season/season_summer.html'
    season = 'summer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 여기에 차트 데이터 추가
        top5_genre, top5_genre_count, top5_selector = get_pie_chart(self.season)
        context['top5_genre'] = top5_genre
        context['top5_genre_count'] = top5_genre_count
        context['top5_selector'] = top5_selector

        # 초기값
        selected_genre = self.request.GET.get('genre', '댄스')
        top3_song_names, top3_song_counts = get_bar_chart(self.season, '댄스')
        context['top3_songs'] = list(zip(top3_song_names, top3_song_counts))
        context['selected_genre'] = '댄스'

        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('ajax') == '1':
            selected_genre = self.request.GET.get('genre', '댄스')
            top3_song_names, top3_song_counts = get_bar_chart(self.season, selected_genre)
            context['top3_songs'] = list(zip(top3_song_names, top3_song_counts))
            context['selected_genre'] = selected_genre

            return JsonResponse({'top3_songs' : context['top3_songs']})

        return super().render_to_response(context, **response_kwargs)
    
class FallView(generic.TemplateView):
    template_name = 'season/season_fall.html'
    season = 'fall'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 여기에 차트 데이터 추가
        top5_genre, top5_genre_count, top5_selector = get_pie_chart(self.season)
        context['top5_genre'] = top5_genre
        context['top5_genre_count'] = top5_genre_count
        context['top5_selector'] = top5_selector

        # 초기값
        selected_genre = self.request.GET.get('genre', '댄스')
        top3_song_names, top3_song_counts = get_bar_chart(self.season, '댄스')
        context['top3_songs'] = list(zip(top3_song_names, top3_song_counts))
        context['selected_genre'] = '댄스'

        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('ajax') == '1':
            selected_genre = self.request.GET.get('genre', '댄스')
            top3_song_names, top3_song_counts = get_bar_chart(self.season, selected_genre)
            context['top3_songs'] = list(zip(top3_song_names, top3_song_counts))
            context['selected_genre'] = selected_genre

            return JsonResponse({'top3_songs' : context['top3_songs']})

        return super().render_to_response(context, **response_kwargs)
    
class WinterView(generic.TemplateView):
    template_name = 'season/season_winter.html'
    season = 'winter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 여기에 차트 데이터 추가
        top5_genre, top5_genre_count, top5_selector = get_pie_chart(self.season)
        context['top5_genre'] = top5_genre
        context['top5_genre_count'] = top5_genre_count
        context['top5_selector'] = top5_selector

        # 초기값
        selected_genre = self.request.GET.get('genre', '댄스')
        top3_song_names, top3_song_counts = get_bar_chart(self.season, '댄스')
        context['top3_songs'] = list(zip(top3_song_names, top3_song_counts))
        context['selected_genre'] = '댄스'

        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('ajax') == '1':
            selected_genre = self.request.GET.get('genre', '댄스')
            top3_song_names, top3_song_counts = get_bar_chart(self.season, selected_genre)
            context['top3_songs'] = list(zip(top3_song_names, top3_song_counts))
            context['selected_genre'] = selected_genre

            return JsonResponse({'top3_songs' : context['top3_songs']})

        return super().render_to_response(context, **response_kwargs)