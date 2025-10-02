import requests
from bs4 import BeautifulSoup
import time
import random

class KoreanMusicAwardsScraper:
    """한국대중음악상 아카이브 스크래퍼"""
    
    BASE_URL = "https://koreanmusicawards.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_genre_awards(self, genre_type):
        """
        장르별 수상작 목록 가져오기
        genre_type: 'hiphop', 'indie_rock', 'kpop'
        
        실제 구현 시:
        1. 한국대중음악상 아카이브 페이지 접속
        2. 연도별로 순회
        3. 각 장르별 수상작(노래/음반) 파싱
        4. 리스트로 반환
        """
        # TODO: 실제 스크래핑 로직 구현
        # 현재는 샘플 데이터 반환
        return self._get_sample_data(genre_type)
    
    def scrape_archive_page(self, year):
        """특정 연도의 아카이브 페이지 스크래핑"""
        try:
            url = f"{self.BASE_URL}/archive/{year}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # TODO: 실제 HTML 구조 파악 후 파싱 로직 작성
            # 예시:
            # awards = soup.find_all('div', class_='award-item')
            # for award in awards:
            #     title = award.find('h3').text
            #     artist = award.find('span', class_='artist').text
            
            return []
        except Exception as e:
            print(f"Error scraping archive page: {e}")
            return []
    
    def _get_sample_data(self, genre_type):
        """테스트용 샘플 데이터 - 실제 한국 노래들"""
        sample_data = {
            'hiphop': [
                {'type': 'song', 'title': '팔레트', 'artist': '아이유', 'year': 2017},
                {'type': 'song', 'title': 'Love Lee', 'artist': 'AKMU', 'year': 2023},
                {'type': 'song', 'title': '에잇', 'artist': '아이유', 'year': 2020},
                {'type': 'album', 'title': 'LOVE YOURSELF 轉 Tear', 'artist': 'BTS', 'year': 2018},
            ],
            'indie_rock': [
                {'type': 'song', 'title': '봄날', 'artist': 'BTS', 'year': 2017},
                {'type': 'song', 'title': '사건의 지평선', 'artist': '윤하', 'year': 2024},
                {'type': 'song', 'title': '밤편지', 'artist': '아이유', 'year': 2017},
                {'type': 'album', 'title': '5집 Piece', 'artist': '윤하', 'year': 2024},
            ],
            'kpop': [
                {'type': 'song', 'title': 'Super Shy', 'artist': 'NewJeans', 'year': 2023},
                {'type': 'song', 'title': 'Ditto', 'artist': 'NewJeans', 'year': 2022},
                {'type': 'song', 'title': 'OMG', 'artist': 'NewJeans', 'year': 2023},
                {'type': 'album', 'title': 'Get Up', 'artist': 'NewJeans', 'year': 2023},
            ]
        }
        return sample_data.get(genre_type, [])


class LyricsScraper:
    """가사 스크래퍼 - 벅스, 멜론 등의 사이트에서 가사 수집"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_and_get_lyrics(self, title, artist):
        """
        곡 제목과 아티스트로 가사 검색 및 가져오기
        
        실제 구현 시:
        1. 가사 사이트에서 검색
        2. 검색 결과 중 가장 일치하는 곡 선택
        3. 가사 페이지 접속
        4. 가사 파싱 후 반환
        """
        # TODO: 실제 가사 사이트 스크래핑 로직
        # 저작권 문제로 샘플 가사 반환
        return self._get_sample_lyrics(title, artist)
    
    def get_album_songs(self, album_title, artist):
        """
        음반의 수록곡 목록 가져오기
        
        실제 구현 시:
        1. 음반 검색
        2. 수록곡 목록 파싱
        3. 각 곡의 정보 반환
        """
        return self._get_sample_album_songs(album_title, artist)
    
    def _get_sample_lyrics(self, title, artist):
        """테스트용 샘플 가사 - 실제 노래 스타일 반영"""
        sample_lyrics = {
            '팔레트': """
                스물다섯 살 물음표를 느낌표로 바꿀 나이
                파란색이 질려 버린 스물다섯 살 나이
                이제야 알겠어 날 좋아하는 게 뭔지
                진짜 어른이 되어가나 봐
                
                내가 좋아하는 걸 고르는 게 익숙해질 나이
                선명한 색깔들을 좋아하던 어린 날은 멀어져
                이젠 그냥 편한 게 좋아 편한 사람이 좋아
                
                스물다섯 나만의 팔레트를 찾아가
                좋아하는 것만 골라 담아
            """,
            'Love Lee': """
                사랑 사랑 사랑 너를 사랑해
                너무나 사랑스러운 사람
                매일매일 생각나 네 생각에 설레어
                이 마음을 어떻게 전하면 좋을까
                
                너의 웃음소리가 좋아
                너의 목소리가 좋아
                너의 모든 것이 좋아
                
                사랑한다는 말로는 부족해
                내 마음 다 담아 전하고 싶어
            """,
            '에잇': """
                삶은 살만한 거야 어떻게든 되는 거야
                버텨 버텨 견뎌 견뎌
                아무리 힘들어도
                
                내일은 분명 더 나아질 거야
                그러니까 웃어 웃어 웃어봐
                에잇 에잇 에잇
                
                힘든 하루 속에서도
                작은 행복을 찾아봐
                우리 함께 이겨내자
            """,
            '봄날': """
                보고 싶다 이렇게 말하니까 더 보고 싶다
                너희 사진을 보고 있어도 보고 싶다
                너무 야속한 시간 나는 우리가 밉다
                이젠 얼굴 한 번 보는 것도 힘들어진 우리가
                
                허공을 떠도는 작은 먼지처럼 작은 먼지처럼
                날리는 눈이 나라면 조금 더 빨리 네게 닿을 수 있을 텐데
                
                추운 겨울 끝을 지나 다시 봄날이 올 때까지
                꽃 피울 때까지 그곳에 좀 더 머물러줘
            """,
            '사건의 지평선': """
                너와 나의 경계선 그 끝에서
                빠져나올 수 없는 이 순간
                시간마저 멈춰버린 우리
                영원 속에 갇혀버린 사랑
                
                블랙홀 같은 네 눈빛에
                나는 점점 빨려 들어가
                빛조차 벗어날 수 없는
                이 사랑의 지평선
                
                너와 나의 시간이 멈춰버린
                사건의 지평선 너머로
            """,
            '밤편지': """
                이 밤 그날의 반딧불을 당신의 창 가까이 보낼게요
                사랑한다는 말이에요
                
                나 보기가 역겨워 가실 때에는
                말없이 고이 보내 드리우리다
                
                이 밤 너의 곁에 머물고 싶어
                이 밤이 끝나지 않길 바라며
                사랑한다는 말로는 부족해
                내 마음을 전하고 싶어
            """,
            'Super Shy': """
                I'm super shy super shy
                너를 볼 때마다 부끄러워
                말도 제대로 못하고
                얼굴만 빨개져
                
                친구들은 말해 용기 내라고
                하지만 나는 정말 수줍어
                
                너의 눈을 마주치면
                심장이 두근거려
                이 마음 들킬까 봐
                고개를 돌려버려
            """,
            'Ditto': """
                Stay in the middle like you a little
                Don't want no riddle 말해줘 say it back
                Oh say it ditto 아침은 너무 멀어
                
                같은 시간 속의 너와 나
                같은 마음으로 바라봐
                이 순간이 영원하길
                
                너도 나와 같다면
                우리 함께 영원히
                이 순간을 기억해줘
            """,
            'OMG': """
                Oh my oh my God 예상했어 나
                I was really hoping that he will come through
                Oh my oh my God 단 너뿐이야
                
                너를 보면 심장이 뛰어
                이건 정말 사랑인 걸까
                믿을 수가 없어
                
                꿈만 같은 이 순간
                네가 내 곁에 있다는 게
            """,
        }
        
        lyrics = sample_lyrics.get(title)
        if lyrics:
            return lyrics.strip()
        
        # 기본 샘플 가사
        return f"""
            {title} - {artist}
            
            사랑 그리움 추억 이별 눈물
            행복 슬픔 아픔 기억 마음
            시간 영원 순간 우리 함께
            
            너의 미소 너의 목소리
            나의 마음 나의 사랑
        """.strip()
    
    def _get_sample_album_songs(self, album_title, artist):
        """테스트용 샘플 음반 수록곡"""
        sample_albums = {
            'LOVE YOURSELF 轉 Tear': [
                {'title': 'Fake Love', 'artist': 'BTS'},
                {'title': '전하지 못한 진심', 'artist': 'BTS'},
                {'title': '낙원', 'artist': 'BTS'},
            ],
            '5집 Piece': [
                {'title': '사건의 지평선', 'artist': '윤하'},
                {'title': 'Point', 'artist': '윤하'},
            ],
            'Get Up': [
                {'title': 'Super Shy', 'artist': 'NewJeans'},
                {'title': 'ETA', 'artist': 'NewJeans'},
                {'title': 'Cool With You', 'artist': 'NewJeans'},
            ],
        }
        return sample_albums.get(album_title, [])
    
    def delay(self):
        """서버 부담을 줄이기 위한 딜레이"""
        time.sleep(random.uniform(1, 2))