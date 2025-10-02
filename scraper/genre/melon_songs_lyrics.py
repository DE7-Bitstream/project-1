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
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/140.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# ====== 가사 가져오기 함수 ======
def get_melon_lyrics(song_id: str) -> str:
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
    csv_path = r"C:\Users\yoond\Web Scrapping\csv\melon_genre_steady_songs.csv"
    df = pd.read_csv(csv_path)

    lyrics_list = []
    total = len(df)

    for idx, row in df.iterrows():
        song_id = row["songId"]

        # 가사 가져오기
        lyrics = get_melon_lyrics(song_id)
        lyrics_list.append(lyrics)

        # 진행률 표시
        progress = (idx + 1) / total * 100
        print(f"진행률: {progress:.2f}% ({idx+1}/{total})", end="\r")

        time.sleep(1)  # 요청 간격 (차단 방지)

    # DataFrame에 가사 추가
    df["lyrics"] = lyrics_list

    save_path = r"C:\Users\yoond\Web Scrapping\csv\melon_genre_steady_songs_with_lyrics.csv"
    df.to_csv(save_path, index=False, encoding="utf-8-sig")
    print(f"\n✅ 가사 저장 완료: {save_path}")
    print(df.head())

if __name__ == "__main__":
    main()
    driver.quit()
