import os
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def index(request):
    """가사 분석 메인 페이지"""
    # 기본 통계 정보
    csv_path = os.path.join(settings.BASE_DIR, '..', 'scraper', 'genre', 'csv', 'melon_song_words.csv')
    
    context = {
        'total_songs': 0,
        'total_words': 0,
    }
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            context['total_songs'] = len(df['songId'].unique()) if 'songId' in df.columns else 0
            context['total_words'] = len(df) if len(df) > 0 else 0
        except:
            pass
    
    return render(request, 'lyrics/index.html', context)

def wordcloud_view(request):
    """장르별 워드클라우드 생성 및 표시"""
    genre = request.GET.get('genre', '전체')
    
    # CSV 파일 경로
    csv_path = os.path.join(settings.BASE_DIR, '..', 'scraper', 'genre', 'csv', 'melon_song_words.csv')
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            
            # 장르별 필터링
            if genre != '전체' and 'genre' in df.columns:
                df_filtered = df[df['genre'] == genre]
            else:
                df_filtered = df
            
            if len(df_filtered) > 0:
                # 워드클라우드 데이터 준비
                word_data = df_filtered.groupby('word').size().reset_index(name='count')
                top_words = word_data.nlargest(30, 'count')
                
                context = {
                    'word_data': top_words.to_dict('records'),
                    'genre': genre,
                    'total_songs': len(df_filtered['songId'].unique()) if 'songId' in df_filtered.columns else 0,
                    'total_words': len(df_filtered)
                }
            else:
                context = {
                    'word_data': [],
                    'genre': genre,
                    'total_songs': 0,
                    'total_words': 0,
                    'error': f'{genre} 장르의 데이터가 없습니다.'
                }
                
        except Exception as e:
            context = {
                'word_data': [],
                'genre': genre,
                'total_songs': 0,
                'total_words': 0,
                'error': f'CSV 파일 읽기 오류: {str(e)}'
            }
    else:
        context = {
            'word_data': [],
            'genre': genre,
            'total_songs': 0,
            'total_words': 0,
            'error': 'CSV 파일이 없습니다. 먼저 가사 분석을 실행해주세요.'
        }
    
    return render(request, 'lyrics/wordcloud.html', context)

def analysis_view(request):
    """가사 분석 결과 페이지"""
    return render(request, 'lyrics/analysis.html')