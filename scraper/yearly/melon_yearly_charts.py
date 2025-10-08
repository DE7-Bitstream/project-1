import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from csv_utils import write_data_to_csv

# 크롤링 대상 설정
MELON_URL = "https://www.melon.com/chart/index.htm"
TARGET_DECADE = ['2020년대']
TARGET_YEARS = ['2024년', '2023년', '2022년', '2021년', '2020년']


# CSS 선택자 상수 정의
# 차트 파인더 버튼
SEL_CHART_FINDER_BTN = (By.CLASS_NAME, 'btn_chart_f')
# 연도차트 탭
SEL_YEAR_CHART_TAB = (By.CLASS_NAME, 'tab03')
# 연대 선택 라벨 목록
SEL_DECADE_LABELS = (By.XPATH, "//div[@class='box_chic nth1 view']//label")
# 연도 선택 라벨 목록
SEL_YEAR_LABELS = (By.XPATH, "//div[@class='box_chic nth2 view']//label")
# 국내종합 라디오 버튼 
SEL_STYLE_KOREAN = (By.XPATH, '//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[2]/span/label')
# 검색 버튼
SEL_SEARCH_BUTTON = (By.CLASS_NAME, 'even_span')
# 차트 테이블 바디
SEL_CHART_TBODY = (By.ID, "chartListObj")

# 정규 표현식 컴파일
SONG_ID_PATTERN = re.compile(r"goSongDetail\('(\d+)'\)")
ALBUM_ID_PATTERN = re.compile(r"goAlbumDetail\('(\d+)'\)")


def setup_driver():
    """WebDriver를 초기화하고 반환합니다."""
    options = Options()
    # 403 에러 방지를 위한 user_agent 정보 추가
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_argument(f"--user-agent={user_agent}")
    # 서버 환경에서 원활한 구동을 위한 옵션 추가
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # WebDriver Manager를 사용하여 Chrome 드라이버를 자동으로 설치 및 설정
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=service)
        return driver
    except Exception as e:
        print(f"❌ WebDriver 초기화 중 오류 발생: {e}")
        return None

def open_chart_finder(driver, wait):
    """멜론 차트 페이지에 접속하여 차트 파인더를 동적으로 제어합니다."""
    try:
        driver.get(MELON_URL)
        print(f"✅ {MELON_URL} 접속 완료.")

        # 1. 차트 파인더 클릭
        chart_finder_btn = wait.until(EC.element_to_be_clickable(SEL_CHART_FINDER_BTN))
        ActionChains(driver).click(chart_finder_btn).perform()
        print("✅ 차트 파인더 클릭.")

        # 2. 연도차트 선택
        year_chart_tab = wait.until(EC.element_to_be_clickable(SEL_YEAR_CHART_TAB))
        ActionChains(driver).click(year_chart_tab).perform()
        print("✅ 연도차트 탭 선택.")
        return True
    except Exception as e:
        print(f"❌ 페이지 이동/초기 설정 중 오류 발생: {e}")
        return False

def select_and_search_chart(driver, wait, year_label, style_selector=SEL_STYLE_KOREAN):
    """차트 조건을 설정하고 검색을 실행합니다."""
    try:
        # 국내종합 선택 (안정적으로 대기 후 클릭)
        style_btn = wait.until(EC.element_to_be_clickable(style_selector))
        style_btn.click()
        print(f"  ✅ {year_label.text} - 국내종합 선택 완료.")

        # 검색 버튼 클릭
        search_btn = wait.until(EC.element_to_be_clickable(SEL_SEARCH_BUTTON))
        search_btn.click()
        print(f"  ✅ {year_label.text} 차트 검색 실행.")

        wait.until(EC.presence_of_element_located(SEL_CHART_TBODY))
        return True

    except Exception as e:
        print(f"  ❌ 차트 검색 설정 중 오류 발생 ({year_label.text}): {e}")
        return False

def extract_song_and_album_ids(tr_element):
    """하나의 차트 행(tr)에서 노래 및 앨범 ID를 추출합니다."""
    song_id, album_id = None, None
    a_tags = tr_element.find_elements(By.TAG_NAME, "a")

    for a_tag in a_tags:
        # 이미 두 ID를 모두 찾았다면 루프를 종료
        if song_id is not None and album_id is not None:
            break

        current_href = a_tag.get_attribute('href')

        if current_href:
            # 1. 노래 ID 매칭 시도
            if song_id is None:
                match_song = SONG_ID_PATTERN.search(current_href)
                if match_song:
                    song_id = match_song.group(1)

            # 2. 앨범 ID 매칭 시도
            if album_id is None:
                match_album = ALBUM_ID_PATTERN.search(current_href)
                if match_album:
                    album_id = match_album.group(1)

    return song_id, album_id

def process_chart_data(driver, wait, year_text, yearly_charts):
    """현재 페이지의 차트 데이터를 파싱하고 저장합니다."""
    try:
        tbody_obj = wait.until(EC.presence_of_element_located(SEL_CHART_TBODY))
        tr_list = tbody_obj.find_elements(By.TAG_NAME, "tr")

        print(f"  📊 {year_text} 차트 {len(tr_list)}개 항목 파싱 시작.")
        rank = 0
        for tr in tr_list:
            rank += 1
            song_id, album_id = extract_song_and_album_ids(tr)

            if song_id and album_id:
                status = "✅ 성공"
            elif song_id:
                status = "⚠️ 앨범 ID 없음"
            elif album_id:
                status = "⚠️ 노래 ID 없음"
            else:
                status = "❌ 실패"

            data = {
                "year": year_text[:-1], # '2024년' -> '2024'
                "rank": rank,
                "song_id": song_id,
                "album_id": album_id
            }
            yearly_charts.append(data)
        print(f"  ✅ {year_text} 차트 파싱 완료. 총 {len(tr_list)}개 데이터 수집.")

    except Exception as e:
        print(f"  ❌ 차트 데이터 파싱 중 오류 발생 ({year_text}): {e}")


def main_scraper_logic():

    driver = setup_driver()
    if driver is None:
        return []

    wait = WebDriverWait(driver, 10)
    YEARLY_CHARTS = []
    
    try:
        if not open_chart_finder(driver, wait):
            return []

        # ========== 연대 선택 루프 ==========
        initial_decade_labels = wait.until(EC.presence_of_all_elements_located(SEL_DECADE_LABELS))

        # 실제 클릭할 요소에 접근하기 위해 텍스트와 요소를 매핑합니다.
        decade_map = {label.text: label for label in initial_decade_labels}

        for decade_text in TARGET_DECADE:
            if decade_text in decade_map:
                print(f"\n🚀 {decade_text} 선택 시작.")
                
                # 1. 연대 클릭: 연도 선택 창을 열고 연대 선택을 활성화합니다.
                current_decade_label = decade_map[decade_text]
                current_decade_label.click()
                
                # ========== 연도 선택 루프 ==========
                for year_text in TARGET_YEARS:
                    print(f"  🗓️ {year_text} 차트 수집 시작.")

                    # 2. 연도 라벨 재로딩 및 클릭
                    # 현재 모달 창 내에서 연도 라벨을 다시 찾습니다. (가장 안정적인 방법)
                    year_labels = wait.until(EC.presence_of_all_elements_located(SEL_YEAR_LABELS))
                    
                    # 텍스트 일치하는 라벨을 찾아 클릭합니다.
                    year_label_to_click = None
                    for label in year_labels:
                        if label.text == year_text:
                            year_label_to_click = label
                            break
                    
                    if year_label_to_click:
                        year_label_to_click.click() # 연도 선택
                    else:
                        print(f"  ❌ 경고: {year_text} 라벨을 찾을 수 없습니다. 건너뜁니다.")
                        continue


                    # 3. 차트 검색 및 데이터 파싱
                    if select_and_search_chart(driver, wait, year_label_to_click):
                        process_chart_data(driver, wait, year_text, YEARLY_CHARTS)

                    # 4. 다음 연도 선택을 위한 복귀 로직
                    print(f"  🔄 {year_text} 후 '차트선택' 화면 복귀 시작.")
                    
                    # '차트 파인더' 버튼 재클릭 
                    chart_finder_btn = wait.until(EC.element_to_be_clickable(SEL_CHART_FINDER_BTN))
                    ActionChains(driver).click(chart_finder_btn).perform()
                    
                    # '연도차트' 탭 재선택 (선택 상태 복구)
                    year_chart_tab = wait.until(EC.element_to_be_clickable(SEL_YEAR_CHART_TAB))
                    ActionChains(driver).click(year_chart_tab).perform()
                    
                    # 마지막으로, 연도 선택 창을 활성화하기 위해 현재 연대를 다시 클릭
                    # (이때는 모달이 열렸으므로 새롭게 요소를 찾아야 합니다.)
                    re_select_decade_label = wait.until(
                        EC.element_to_be_clickable((By.XPATH, f"//label[text()='{decade_text}']"))
                    )
                    re_select_decade_label.click()
                    print(f"  ✅ '차트선택' 화면 복귀 및 {decade_text} 재선택 완료.")
                    
            else:
                print(f"❌ 경고: {decade_text} 연대 라벨을 찾을 수 없습니다. 건너뜁니다.")


    except Exception as e:
        print(f"❌ 메인 크롤링 루프 중 오류 발생: {e}")

    finally:
        if driver:
            driver.quit()
            print("\n✅ WebDriver 종료.")
        return YEARLY_CHARTS

# 실행 (이하 동일)
if __name__ == '__main__':
    start_time = time.time()
    results = main_scraper_logic()
    # 스크래핑한 데이터 csv 저장
    write_data_to_csv("melon_yearly_top100.csv", results)
    end_time = time.time()

    print("\n" + "="*50)
    print(f"✨ 최종 수집된 데이터 개수: {len(results)}개")
    print(f"⏱️ 총 소요 시간: {end_time - start_time:.2f}초")
    print("="*50)