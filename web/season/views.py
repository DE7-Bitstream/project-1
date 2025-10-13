from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from season.data_processor import get_pie_chart, get_bar_chart

# Create your views here.
def index(request):
    return render(request, 'season/season_index.html')


class BaseSeasonView(generic.TemplateView):
    """
    계절별 뷰의 공통 로직을 담은 기본 클래스
    중복 코드를 제거하고 유지보수성을 향상
    """
    season = None  # 하위 클래스에서 반드시 정의해야 함
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pie Chart 데이터 가져오기
        top5_genre, top5_genre_count, top5_selector = get_pie_chart(self.season)
        context['top5_genre'] = top5_genre
        context['top5_genre_count'] = top5_genre_count
        context['top5_selector'] = top5_selector
        
        # 초기 장르 설정 (기본값: '댄스')
        default_genre = '댄스'
        top3_song_names, top3_song_counts, top3_song_images = get_bar_chart(
            self.season, 
            default_genre
        )
        context['top3_songs'] = list(zip(top3_song_names, top3_song_counts, top3_song_images))
        context['selected_genre'] = default_genre
        
        return context
    
    def render_to_response(self, context, **response_kwargs):
        """AJAX 요청 처리"""
        if self.request.GET.get('ajax') == '1':
            selected_genre = self.request.GET.get('genre', '댄스')
            top3_song_names, top3_song_counts, top3_song_images = get_bar_chart(
                self.season, 
                selected_genre
            )
            context['top3_songs'] = list(zip(top3_song_names, top3_song_counts, top3_song_images))
            context['selected_genre'] = selected_genre
            
            return JsonResponse({'top3_songs': context['top3_songs']})
        
        return super().render_to_response(context, **response_kwargs)


class SpringView(BaseSeasonView):
    """봄 시즌 뷰"""
    template_name = 'season/season_spring.html'
    season = 'spring'


class SummerView(BaseSeasonView):
    """여름 시즌 뷰"""
    template_name = 'season/season_summer.html'
    season = 'summer'


class FallView(BaseSeasonView):
    """가을 시즌 뷰"""
    template_name = 'season/season_fall.html'
    season = 'fall'


class WinterView(BaseSeasonView):
    """겨울 시즌 뷰"""
    template_name = 'season/season_winter.html'
    season = 'winter'
