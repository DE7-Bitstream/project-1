import requests
from bs4 import BeautifulSoup
import csv
from dates import calculate_weeks
from __init__ import *
from selenium import webdriver

def get_cookies_with_selenium(url):
    # Selenium을 사용하여 쿠키를 가져오기
    driver = webdriver.Chrome()
    driver.get(url)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

def get_bs_from_days(cookies, start_day, end_day) -> BeautifulSoup:
    HEADER = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    }

    # 두 번째 요청 (세션 쿠키 활용)
    url = f"https://www.melon.com/chart/search/list.htm?chartType=WE&classCd=DP0000&startDay={start_day}&endDay={end_day}&moved=Y"
    response = requests.get(url, headers=HEADER, cookies={cookie['name']: cookie['value'] for cookie in cookies})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the chart URL: {url}, Status Code: {response.status_code}")
    
    # BeautifulSoup 객체 생성
    bs = BeautifulSoup(response.text, "html.parser")
    return bs



def parse_chart(bs) -> list:
    '''
    bs를 기반으로 차트 정보를 파싱하여 리스트로 반환
    '''
    songs = []
    for tr in bs.select("tr"):
        rank = tr.select_one(".rank")
        title = tr.select_one(".wrap_song_info .rank01 a")
        performer = tr.select_one(".wrap_song_info .rank02 a")
        
        if rank and title and performer:
            songs.append({
                "rank": rank.get_text(strip=True),
                "title": title.get_text(strip=True),
                "performer": performer.get_text(strip=True)
            })
    
    return songs

def crawl_data_by_days_url(cookies, start_day, end_day) -> list:
    bs = get_bs_from_days(cookies, start_day, end_day)
    chart = parse_chart(bs)
    return chart

def crawl_and_write_data_by_year(cookies, year) -> None:
    weeks = calculate_weeks(year)
    output_file = f"{CSV_DIR}/melon_chart_weekly_{year}.csv"

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["year", "month", "week_number_in_month", "rank", "song_name", "song_performer"])

        for week_year, week_month, week_number_in_month, week_start_day, week_end_day in weeks:
            chart = crawl_data_by_days_url(cookies, week_start_day, week_end_day)

            for item in chart:
                writer.writerow([
                    week_year,
                    week_month,
                    week_number_in_month,
                    item["rank"],
                    item["title"],
                    item["performer"]
                ])

if __name__ == "__main__":
    years = YEARS
    cookies = get_cookies_with_selenium("https://www.melon.com/chart/index.htm")
    for year in years:
        crawl_and_write_data_by_year(cookies, year)