from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Genre, Song, Album, WordFrequency
from .scraper import KoreanMusicAwardsScraper, LyricsScraper
from .analyzer import LyricsAnalyzer
from .wordcloud_generator import WordCloudGenerator
import os


def index(request):
    """메인 페이지"""
    # 장르별 통계
    genres = Genre.objects.all()
    
    stats = []
    for genre in genres:
        song_count = Song.objects.filter(genre=genre).count()
        album_count = Album.objects.filter(genre=genre).count()
        stats.append({
            'genre': genre,
            'song_count': song_count,
            'album_count': album_count,
        })
    
    context = {
        'stats': stats,
    }
    return render(request, 'index.html', context)


def scrape_songs(request):
    """노래 스크래핑 실행"""
    if request.method == 'POST':
        genre_name = request.POST.get('genre')
        
        try:
            # 장르 가져오기 또는 생성
            genre, created = Genre.objects.get_or_create(
                name=genre_name,
                defaults={'display_name': _get_genre_display_name(genre_name)}
            )
            
            # 스크래퍼 초기화
            kma_scraper = KoreanMusicAwardsScraper()
            lyrics_scraper = LyricsScraper()
            
            # 한국대중음악상에서 수상작 목록 가져오기
            awards_data = kma_scraper.get_genre_awards(genre_name)
            
            saved_count = 0
            
            for item in awards_data:
                if item['type'] == 'song':
                    # 노래 직접 저장
                    lyrics = lyrics_scraper.search_and_get_lyrics(
                        item['title'], 
                        item['artist']
                    )
                    
                    song, created = Song.objects.get_or_create(
                        title=item['title'],
                        artist=item['artist'],
                        genre=genre,
                        defaults={
                            'lyrics': lyrics,
                            'year': item.get('year'),
                        }
                    )
                    
                    if created:
                        saved_count += 1
                    
                    lyrics_scraper.delay()
                
                elif item['type'] == 'album':
                    # 음반의 경우 수록곡 먼저 가져오기
                    album, _ = Album.objects.get_or_create(
                        title=item['title'],
                        artist=item['artist'],
                        genre=genre,
                        defaults={'year': item.get('year', 2024)}
                    )
                    
                    # 음반 수록곡 목록 가져오기
                    album_songs = lyrics_scraper.get_album_songs(
                        item['title'],
                        item['artist']
                    )
                    
                    # 각 수록곡의 가사 가져오기
                    for song_info in album_songs:
                        lyrics = lyrics_scraper.search_and_get_lyrics(
                            song_info['title'],
                            song_info['artist']
                        )
                        
                        song, created = Song.objects.get_or_create(
                            title=song_info['title'],
                            artist=song_info['artist'],
                            genre=genre,
                            defaults={
                                'lyrics': lyrics,
                                'album': album,
                                'year': item.get('year'),
                            }
                        )
                        
                        if created:
                            saved_count += 1
                        
                        lyrics_scraper.delay()
            
            messages.success(request, f'{genre.display_name} 장르의 노래 {saved_count}곡을 저장했습니다.')
            
        except Exception as e:
            messages.error(request, f'스크래핑 중 오류 발생: {str(e)}')
    
    return redirect('scraper:index')


def analyze_genre(request, genre):
    """장르별 가사 분석 및 워드클라우드 생성"""
    try:
        genre_obj = Genre.objects.get(name=genre)
    except Genre.DoesNotExist:
        messages.error(request, '해당 장르를 찾을 수 없습니다.')
        return redirect('scraper:index')
    
    # 해당 장르의 모든 노래 가사 가져오기
    songs = Song.objects.filter(genre=genre_obj)
    
    if not songs.exists():
        messages.warning(request, f'{genre_obj.display_name} 장르의 노래가 없습니다. 먼저 스크래핑을 실행하세요.')
        return redirect('scraper:index')
    
    # 가사 리스트 추출
    lyrics_list = [song.lyrics for song in songs if song.lyrics]
    
    if not lyrics_list:
        messages.warning(request, '분석할 가사가 없습니다.')
        return redirect('scraper:index')
    
    # 텍스트 분석
    analyzer = LyricsAnalyzer()
    
    # 명사 추출 및 빈도 분석
    word_freq_list = analyzer.analyze_lyrics_batch(lyrics_list)
    
    # WordFrequency 모델에 저장
    WordFrequency.objects.filter(genre=genre_obj).delete()  # 기존 데이터 삭제
    
    for word, freq in word_freq_list:
        WordFrequency.objects.create(
            genre=genre_obj,
            word=word,
            frequency=freq,
            pos='명사'
        )
    
    messages.success(request, f'{genre_obj.display_name} 장르의 가사 분석이 완료되었습니다.')
    return redirect('scraper:wordcloud')


def wordcloud_view(request):
    """워드클라우드 시각화 페이지"""
    genres = Genre.objects.all()
    
    # 선택된 장르들 (기본값: 모든 장르)
    selected_genres = request.GET.getlist('genres')
    if not selected_genres:
        selected_genres = [g.name for g in genres]
    
    # 각 장르별 워드클라우드 데이터
    wordcloud_data = []
    word_freq_dicts = []
    genre_names = []
    
    for genre in genres:
        if genre.name in selected_genres:
            # 해당 장르의 단어 빈도 가져오기
            word_freqs = WordFrequency.objects.filter(genre=genre).order_by('-frequency')[:100]
            
            if word_freqs.exists():
                # {단어: 빈도수} 딕셔너리 생성
                word_freq_dict = {wf.word: wf.frequency for wf in word_freqs}
                
                # 워드클라우드 생성
                wc_generator = WordCloudGenerator()
                wordcloud = wc_generator.generate(word_freq_dict, genre.name)
                
                if wordcloud:
                    # base64 이미지로 변환
                    image_data = wc_generator.get_base64_image(wordcloud)
                    
                    # 상위 20개 단어
                    top_words = list(word_freqs[:20].values('word', 'frequency'))
                    
                    wordcloud_data.append({
                        'genre': genre,
                        'image': image_data,
                        'top_words': top_words,
                        'total_words': word_freqs.count(),
                    })
                    
                    word_freq_dicts.append(word_freq_dict)
                    genre_names.append(genre.name)
    
    # 비교 워드클라우드 생성 (선택된 장르가 2개 이상일 때)
    comparison_image = None
    if len(word_freq_dicts) > 1:
        wc_generator = WordCloudGenerator()
        comparison_image = wc_generator.generate_comparison(word_freq_dicts, genre_names)
    
    # 통계 정보
    analyzer = LyricsAnalyzer()
    statistics = []
    
    for genre in genres:
        if genre.name in selected_genres:
            songs = Song.objects.filter(genre=genre)
            lyrics_list = [s.lyrics for s in songs if s.lyrics]
            stats = analyzer.get_statistics(lyrics_list)
            stats['genre'] = genre
            statistics.append(stats)
    
    context = {
        'genres': genres,
        'selected_genres': selected_genres,
        'wordcloud_data': wordcloud_data,
        'comparison_image': comparison_image,
        'statistics': statistics,
    }
    
    return render(request, 'wordcloud.html', context)


def _get_genre_display_name(genre_code):
    """장르 코드를 표시 이름으로 변환"""
    names = {
        'hiphop': '힙합 / 랩',
        'indie_rock': '인디 / 락',
        'kpop': 'K-POP',
    }
    return names.get(genre_code, genre_code)   