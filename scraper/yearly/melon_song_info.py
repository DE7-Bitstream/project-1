import requests
from bs4 import BeautifulSoup
import re
import time
from csv_utils import *

# 상수값 정의
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.melon.com/", # 멜론 내부 링크에서 온 것처럼 설정
    "Connection": "keep-alive"
}
BASE_URL = 'https://www.melon.com/song/detail.htm?songId='
SLEEP_TIME_SECONDS = 1


def get_song_meta_data(unique_id_list):

    song_meta_data = []

    with requests.Session() as session:
        session.headers.update(HEADERS)

        for idx, (song_id, album_id) in enumerate(unique_id_list):
            
            url = f'{BASE_URL}{song_id}'

            try:
                # 1. HTML 요청 및 오류 처리
                response = session.get(url, timeout=10)
                response.raise_for_status() 

                # 2. BeautifulSoup 파싱
                soup = BeautifulSoup(response.text, 'html.parser')

                # 제목
                title_tag = soup.select_one('div.song_name')
                if title_tag:
                    strong_tag = title_tag.find('strong')
                    if strong_tag:
                        strong_tag.decompose() # '곡명' 텍스트를 포함하는 <strong> 태그를 제거
                    # 남은 텍스트 전체(실제 제목)를 가져옴
                    title = title_tag.text.strip()
                # 가수
                singer = soup.select_one('.artist a span:nth-of-type(1)').text.strip()
                # 장르
                genre = soup.select_one('.section_info dl.list dd:nth-child(6)').text.strip()

                # 작사/작곡/편곡자 초기화
                lyricists, composers, arrangers = [], [], []
                # 작사/작곡/편곡자 영역 추출
                creators = soup.select('.list_person li')

                for li in creators:
                    try:
                        creator_type_tag = li.select_one('.meta')
                        href_tag = li.select_one('a')
                        
                        if creator_type_tag and href_tag:
                            creator_type = creator_type_tag.text.strip()
                            href = href_tag.get('href')

                            match = re.search(r'goArtistDetail\((\d+)\)', href)
                            if match:
                                creator_id = match.group(1) 
                                if creator_type == '작사':
                                    lyricists.append(creator_id)
                                elif creator_type == '작곡':
                                    composers.append(creator_id)
                                elif creator_type == '편곡':
                                    arrangers.append(creator_id)
                    except Exception as e:
                        print(f"[WARN] song_id {song_id} 작사/작곡/편곡 정보 파싱 실패: {e}")

                data = {
                    'song_id': song_id,
                    'album_id': album_id,
                    'singer': singer,
                    'title': title,
                    "genre": genre,
                    'lyricists': "|".join(lyricists),
                    'composers': "|".join(composers),
                    'arrangers': "|".join(arrangers)
                }
                song_meta_data.append(data)
                print(f"✅ 곡 {song_id} - {idx + 1}/{len(unique_id_list)} 수집 완료.") 
                time.sleep(SLEEP_TIME_SECONDS)

            except requests.exceptions.RequestException as e:
                print(f"❌ 오류: 곡 ID {song_id} 요청 중 HTTP/네트워크 오류: {e}")
                time.sleep(SLEEP_TIME_SECONDS * 2) # 오류 시 더 오래 대기
            except Exception as e:
                print(f"❌ 오류: 곡 ID {song_id} 파싱 중 예상치 못한 오류: {e}")
                time.sleep(SLEEP_TIME_SECONDS * 2)
                
    return song_meta_data


if __name__ == '__main__':

    # unique한 song_id값 가져오기
    unique_id_list = get_column_unique_data('melon_yearly_top100', ['song_id', 'album_id'])
    # album_id 기준으로 메타데이터 스크래핑
    results = get_song_meta_data(unique_id_list)
    # 스크래핑한 데이터 csv 저장
    write_data_to_csv('melon_song_info', results)
