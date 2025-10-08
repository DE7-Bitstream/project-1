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
BASE_URL = 'https://www.melon.com/artist/timeline.htm?artistId='
SLEEP_TIME_SECONDS = 1

def get_creator_meta_data(creator_id_list):

    creator_meta_data = []

    with requests.Session() as session:
        session.headers.update(HEADERS)

        for idx, creator_id in enumerate(creator_id_list):
            
            url = f'{BASE_URL}{creator_id}'

            try:
                # 1. HTML 요청 및 오류 처리
                response = session.get(url, timeout=10)
                response.raise_for_status()

                # 2. BeautifulSoup 파싱
                soup = BeautifulSoup(response.text, 'html.parser')

                # 3. 크리에이터 이름 추출
                artist_tag = soup.select_one('div.wrap_atist_info p.title_atist')
                if artist_tag:
                    strong_tag = artist_tag.find('strong')
                    if strong_tag:
                        strong_tag.decompose()
                    creator_name = artist_tag.text.strip()
                data = {
                    'creator_id': creator_id,
                    'creator_name': creator_name
                }
                creator_meta_data.append(data)
                print(f"✅ 크리에이터 {creator_id} - {idx + 1}/{len(creator_id_list)} 수집 완료.") 
                time.sleep(SLEEP_TIME_SECONDS)

            except requests.exceptions.RequestException as e:
                print(f"❌ 오류: 크리에이터 ID {creator_id} 요청 중 HTTP/네트워크 오류: {e}")
                time.sleep(SLEEP_TIME_SECONDS * 2) # 오류 시 더 오래 대기
            except Exception as e:
                print(f"❌ 오류: 크리에이터 ID {creator_id} 파싱 중 예상치 못한 오류: {e}")
                time.sleep(SLEEP_TIME_SECONDS * 2)
                
    return creator_meta_data

if __name__ == '__main__':
    # '|' 로 연결된 작사가, 작곡가, 편곡자 컬럼에서 유니크한 id 값 가져오기
    creator_id_list = extract_unique_ids_from_piped_data('melon_song_info', ['lyricists', 'composers', 'arrangers'])
    # id 값 기반으로 창작자 이름 스크래핑
    results = get_creator_meta_data(list(creator_id_list))
    # 스크래핑한 데이터 csv 저장
    write_data_to_csv('melon_creator_info', results)
