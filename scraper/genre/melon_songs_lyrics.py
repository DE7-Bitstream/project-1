import os
import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ====== 드라이버 세팅 ======
options = Options()
options.add_argument("--headless")   # 필요시만 사용
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# ====== 가사 가져오기 함수 ======
def get_melon_lyrics(driver, wait, song_id: str) -> str:
    """멜론 곡 상세 페이지에서 가사 추출"""
    url = f"https://www.melon.com/song/detail.htm?songId={song_id}"
    driver.get(url)
    try:
        # 멜론 가사는 <div id="d_video_summary"> 안에 있음
        lyrics_elem = wait.until(
            EC.presence_of_element_located((By.ID, "d_video_summary"))
        )
        # <br> 태그를 줄바꿈으로 치환
        lyrics_html = lyrics_elem.get_attribute("innerHTML")
        lyrics_text = re.sub(r"<br\s*/?>", "\n", lyrics_html)
        return re.sub(r"<.*?>", "", lyrics_text).strip()
    except Exception as e:
        print(f"[WARN] 가사 없음 → songId={song_id}, error={e}")
        return ""

# ====== 메인 실행 ======
def main():
    """
    가사 크롤링 메인 함수
    
    개선사항:
    1. try-finally로 driver 리소스 관리
    2. 절대 경로 -> 상대 경로 사용
    3. 에러 발생 시에도 driver가 확실히 종료됨
    """
    # 절대 경로 대신 상대 경로 사용 - 다른 사람 컴퓨터에서도 작동
    csv_path = os.path.join(os.path.dirname(__file__), "csv", "melon_genre_steady_songs.csv")
    df = pd.read_csv(csv_path)
    
    # driver는 함수 내에서 생성하고 관리
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 10)
        
        lyrics_list = []
        total = len(df)

        for idx, row in df.iterrows():
            song_id = row["songId"]

            # 가사 가져오기
            lyrics = get_melon_lyrics(driver, wait, song_id)
            lyrics_list.append(lyrics)

            # 진행률 표시
            progress = (idx + 1) / total * 100
            print(f"진행률: {progress:.2f}% ({idx+1}/{total})", end="\r")

            time.sleep(1)  # 요청 간격 (차단 방지)

        # DataFrame에 가사 추가
        df["lyrics"] = lyrics_list

        # 절대 경로 대신 상대 경로 사용
        save_path = os.path.join(os.path.dirname(__file__), "csv", "melon_genre_steady_songs_with_lyrics.csv")
        df.to_csv(save_path, index=False, encoding="utf-8-sig")
        print(f"\n✅ 가사 저장 완료: {save_path}")
        print(df.head())
        
    except Exception as e:
        print(f"에러 발생: {e}")
        raise
    finally:
        # 에러가 발생해도 driver를 확실히 종료
        if driver:
            driver.quit()
            print("WebDriver 종료 완료")

if __name__ == "__main__":
    main()
