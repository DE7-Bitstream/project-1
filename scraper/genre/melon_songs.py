import os
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ========= 설정 =========
HEADLESS = False  # 처음엔 False로 돌려서 눈으로 확인 권장. 안정화되면 True로 변경
PAGE_SLEEP = 2.0  # 페이지 로딩 대기
ROW_SLEEP = 0.5   # 과도한 요청 방지

# ========= 드라이버 준비 =========
options = Options()
if HEADLESS:
    options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1366,900")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

album_pattern = re.compile(r"goAlbumDetail\('(\d+)'\)")
song_pattern  = re.compile(r"goSongDetail\('(\d+)'\)")

def _safe_text(ele, css):
    try:
        return ele.find_element(By.CSS_SELECTOR, css).text.strip()
    except:
        return ""

def _safe_texts(ele, css):
    try:
        return [a.text.strip() for a in ele.find_elements(By.CSS_SELECTOR, css) if a.text.strip()]
    except:
        return []

def scrape_genre_steady(genre_name: str, gnr_code: str, steady: bool = True):
    """
    멜론 장르 스테디셀러에서 제목/가수 + songId + albumId 추출 (안정화 버전)
    """
    steady_flag = "Y" if steady else "N"
    max_pages = 4
    results = []

    for page in range(1, max_pages + 1):
        url = f"https://www.melon.com/genre/song_list.htm?gnrCode={gnr_code}&steadyYn={steady_flag}&page={page}"
        driver.get(url)

        # 컨테이너 로딩 대기
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.service_list_song")))
        except Exception as e:
            print(f"[WARN] {genre_name} {page}페이지 컨테이너 대기 실패: {e}")
            time.sleep(PAGE_SLEEP)

        time.sleep(PAGE_SLEEP)  # 추가 안정 대기

        # 1차: tr[data-song-no], 2차: 기존 tr 선택자 폴백
        rows = []
        try:
            rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr[data-song-no]")))
        except:
            pass
        if not rows:
            try:
                rows = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.service_list_song table tbody tr")
                ))
            except Exception as e:
                print(f"[WARN] {genre_name} {page}페이지 노래 행을 찾지 못함: {e}")
                continue

        for row in rows:
            # songId: 우선 data-song-no, 없다면 href에서 정규식 추출
            song_id = row.get_attribute("data-song-no") or ""
            if not song_id:
                try:
                    for a in row.find_elements(By.TAG_NAME, "a"):
                        href = a.get_attribute("href") or ""
                        m = song_pattern.search(href)
                        if m:
                            song_id = m.group(1)
                            break
                except:
                    pass

            # albumId: href에서 정규식 추출
            album_id = ""
            try:
                for a in row.find_elements(By.TAG_NAME, "a"):
                    href = a.get_attribute("href") or ""
                    m = album_pattern.search(href)
                    if m:
                        album_id = m.group(1)
                        break
            except:
                pass

            # 제목
            title = _safe_text(row, "div.ellipsis.rank01 a")
            if not title:
                # 폴백(드물게 구조가 다를 때)
                title = _safe_text(row, "div.ellipsis.rank01")

            # 가수 (여러 명일 수 있음)
            artists = _safe_texts(row, "div.ellipsis.rank02 a")
            artist = "|".join(artists) if artists else _safe_text(row, "div.ellipsis.rank02")

            if title and artist:
                results.append({
                    "genre": genre_name,
                    "title": title,
                    "artist": artist,
                    "songId": song_id,
                    "albumId": album_id
                })

            time.sleep(ROW_SLEEP)

        print(f"  - {genre_name} p{page}: {len(results)} 누적")

    return results

if __name__ == "__main__":
    genre_codes = {
        "발라드": "GN0100",
        "댄스": "GN0200",
        "랩/힙합": "GN0300",
        "록/메탈": "GN0500",
    }

    all_songs = []
    for genre_name, code in genre_codes.items():
        print(f"➤ {genre_name} 스테디셀러 스크래핑 시작")
        part = scrape_genre_steady(genre_name, code, steady=True)
        print(f"  ▶ {genre_name} 수집: {len(part)}")
        all_songs.extend(part)
        time.sleep(1.0)

    driver.quit()

    # 결과 확인 & 저장
    df = pd.DataFrame(all_songs)
    if df.empty:
        print("❌ 결과가 비어 있습니다. HEADLESS=False로 두고 다시 시도해 보세요.")
    else:
        csv_dir = os.path.join(os.getcwd(), "csv")
        os.makedirs(csv_dir, exist_ok=True)
        csv_path = os.path.join(csv_dir, "melon_genre_steady_songs.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print("✅ 저장 완료:", csv_path)
        print(df.head(10))
