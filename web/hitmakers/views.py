from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q, Avg
from .models import YearlyChart, SongCreator


def chart_view(request):
    """메인 차트 페이지"""
    years = YearlyChart.objects.values_list('year', flat=True).distinct().order_by('-year')
    context = {
        'years': list(years),
    }
    return render(request, 'hitmakers/index.html', context)


def get_chart_data(request):
    """선택된 연도와 카테고리에 따른 차트 데이터 반환"""
    year = request.GET.get('year')
    category = request.GET.get('category')
    
    if not year or not category:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
    
    try:
        year = int(year)
    except ValueError:
        return JsonResponse({'error': 'Invalid year'}, status=400)
    
    # 카테고리별 필드 매핑
    # 'get_aggregated_data' 함수에서 집계 로직 분기를 위한 config
    category_config = {
        '기획사': {
            'field': 'album__entertainment',
            'use_creator': False
        },
        '유통사': {
            'field': 'album__distributor',
            'use_creator': False
        },
        '작곡가': {
            'field': 'song__song_creators__creator__name',
            'use_creator': True,
            'role': SongCreator.ROLE_COMPOSER
        },
        '작사가': {
            'field': 'song__song_creators__creator__name',
            'use_creator': True,
            'role': SongCreator.ROLE_LYRICIST
        }
    }
    
    if category not in category_config:
        return JsonResponse({'error': 'Invalid category'}, status=400)
    
    config = category_config[category]
    data = get_aggregated_data(year, config)
    
    return JsonResponse(data, safe=False)


def get_aggregated_data(year, config):
    """공통 데이터 집계 로직"""
    queryset = YearlyChart.objects.filter(year=year)
    
    # 작곡가/작사가인 경우 role 필터 추가
    if config['use_creator']:
        queryset = queryset.filter(song__song_creators__role=config['role'])
    
    results = (
        queryset
        .values(config['field'])
        .annotate(
            count=Count('song', distinct=True),
            avg_rank=Avg('rank')  # 평균 순위
        )
        .order_by('-count', 'avg_rank')[:5] # 정렬기준 : 보유곡수(내림차순) > 평균순위(오름차순)
    )
    
    return [
        {
            'label': item[config['field']] or '미상',
            'value': item['count'],
            'avg_rank': round(item['avg_rank'], 1)  # 소수점 1자리
        }
        for item in results
    ]


def get_top_songs(request):
    """특정 라벨의 상위 3곡 반환"""
    year = request.GET.get('year')
    category = request.GET.get('category')
    label = request.GET.get('label')
    
    if not all([year, category, label]):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
    
    try:
        year = int(year)
    except ValueError:
        return JsonResponse({'error': 'Invalid year'}, status=400)
    
    # 카테고리별 필터 조건 매핑
    filter_config = {
        '기획사': Q(album__entertainment=label),
        '유통사': Q(album__distributor=label),
        '작곡가': Q(
            song__song_creators__role=SongCreator.ROLE_COMPOSER,
            song__song_creators__creator__name=label
        ),
        '작사가': Q(
            song__song_creators__role=SongCreator.ROLE_LYRICIST,
            song__song_creators__creator__name=label
        )
    }
    
    if category not in filter_config:
        return JsonResponse({'error': 'Invalid category'}, status=400)
    
    charts = (
        YearlyChart.objects
        .filter(year=year)
        .filter(filter_config[category])
        .select_related('song')
        .order_by('rank')[:3]
    )
    
    songs = [
        {
            'rank': chart.rank,
            'singer': chart.song.singer,
            'title': chart.song.title
        }
        for chart in charts
    ]
    
    return JsonResponse(songs, safe=False)