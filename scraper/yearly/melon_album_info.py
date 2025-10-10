import requests
from bs4 import BeautifulSoup
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
BASE_URL = 'https://www.melon.com/album/detail.htm?albumId='
SLEEP_TIME_SECONDS = 1

def get_album_meta_data(album_id_list):
    
    album_meta_data = []

    with requests.Session() as session:
        session.headers.update(HEADERS)

        for idx, album_id in enumerate(album_id_list):
            url = f'{BASE_URL}{album_id}'
            try:
                # 1. HTML 요청
                response = session.get(url, timeout=10)
                response.raise_for_status() # HTTP 오류 발생 시 예외 발생

                # 2. BeautifulSoup 파싱
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 메타데이터를 포함하는 부모 요소 선택
                meta_dl = soup.select_one('#conts > div.section_info > div > div.entry > div.meta > dl')
                
                if not meta_dl:
                    print(f"❌ 오류: 앨범 ID {album_id}에서 메타데이터 섹션을 찾을 수 없습니다. (페이지 구조 변경 또는 ID 오류)")
                    continue

                # 3. 각 dd 요소별 데이터 추출
                dd_list = meta_dl.select('dd')
                
                release_date = dd_list[0].text.strip()
                genre = dd_list[1].text.strip()
                distributor = dd_list[2].text.strip()
                enterteinment = dd_list[3].text.strip()

                data = {
                    "album_id": album_id,
                    "release_date": release_date,
                    "genre": genre,
                    "distributor": distributor,
                    "enterteinment": enterteinment,
                }
                album_meta_data.append(data)
                print(f"✅ 앨범 {album_id} - {idx + 1}/{len(album_id_list)} 수집 완료.")
                time.sleep(SLEEP_TIME_SECONDS)

            except requests.exceptions.RequestException as e:
                print(f"❌ 오류: 앨범 ID {album_id} 요청 중 HTTP/네트워크 오류 발생: {e}")
                time.sleep(SLEEP_TIME_SECONDS * 2) # 오류 시 더 오래 대기
            except Exception as e:
                print(f"❌ 오류: 앨범 ID {album_id} 처리 중 예상치 못한 오류 발생: {e}")
                time.sleep(SLEEP_TIME_SECONDS * 2) # 오류 시 더 오래 대기
                
    return album_meta_data


if __name__ == '__main__':

    # unique한 album_id값 가져오기
    album_id_list = get_column_unique_data('melon_yearly_top100', 'album_id')
    # album_id 기준으로 메타데이터 스크래핑
    results = get_album_meta_data(album_id_list)
    # 스크래핑한 데이터 csv 저장
    write_data_to_csv('melon_album_info', results)
