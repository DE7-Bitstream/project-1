from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time

YEAR_ID = {
    2023 : 3,
    2022 : 4,
    2021 : 5,
    2020 : 6
}
TOP_50 = True
TOP_100 = False

def scraping_genre(driver, top_50):
    time.sleep(2)
    info_buttons = driver.find_elements(By.CLASS_NAME, 'btn.btn_icon_detail')
    if top_50:
        info_buttons = info_buttons[:50]
    else:
        info_buttons = info_buttons[50:]

    genres = []
    for i in range(len(info_buttons)):
        ActionChains(driver).click(info_buttons[i]).perform()
        genre = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]')))
        genres.append(genre.text)
        driver.back()

    return genres



def scraping_all(driver, year, month, top_50):
    # 연도 선택
    year_id = YEAR_ID[year]
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f'year_{year_id}')))
    driver.execute_script('arguments[0].click()', button)

    # 월 선택
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f'month_{month}')))
    driver.execute_script('arguments[0].click()', button)

    # 장르 선택 (종합)
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'gnr_1')))
    driver.execute_script('arguments[0].click()', button)

    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn_b26')))
    ActionChains(driver).click(button).perform()

    if not top_50:
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="frm"]/div[2]/span/a')))
        ActionChains(driver).click(button).perform()

    time.sleep(2)
    titles, singers, albums = [], [], []
    data = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'wrap_song_info')))
    if top_50:
        data = data[:50]
    else:
        data = data[50:]

    for i in range(len(data)):
        if '아티스트 더보기' in data[i].text:
            index = data[i].text.index('아티스트 더보기')
            temp = data[i].text
            temp = temp[:index] + temp[index + 9:]
            temp = temp.split('\n')
        else:
            temp = data[i].text.split('\n')
            
        if len(temp) == 2:
            title, singer = temp
            singer, album = singer.split('|')
        else:
            title, singer, album = temp
            _, album = album.split('|')
            
        singer = singer.strip()
        album = album.strip()

        titles.append(title)
        singers.append(singer)
        albums.append(album)

    genres = scraping_genre(driver, top_50)

    return titles, singers, albums, genres



def make_df(titles, singers, albums, genres, year, month):
    df = pd.DataFrame(
        {'순위' : [i for i in range(1, 101)],
         '곡명' : titles,
         '가수' : singers,
         '앨범' : albums,
         '장르' : genres}
    )

    if month < 10:
        month = f'0{month}'
    df.to_csv(f'{year}_{month}_월간차트', index = False)



def scraping(driver, year):
    if year == 2020:
        month = [i for i in range(9, 13)]
    else:
        month = [i for i in range(1, 13)]

    for i in month:
        titles_1, singers_1, albums_1, genres_1 = scraping_all(driver, year, i, TOP_50)
        titles_2, singers_2, albums_2, genres_2 = scraping_all(driver, year, i, TOP_100)

        titles = titles_1 + titles_2
        singers = singers_1 + singers_2
        albums = albums_1 + albums_2
        genres = genres_1 + genres_2
        make_df(titles, singers, albums, genres, year, i)



driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
URL = 'https://www.melon.com/chart/month/index.htm'
driver.get(URL)

# 2024년 이전 데이터 페이지로 이동
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'button_icons.etc.arrow_d')))
ActionChains(driver).click(button).perform()
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'button_icons.arrow_link')))
ActionChains(driver).click(button).perform()

# 연대, 연도, 월, 장르 선택
# 연대 선택은 공통
# 연도가 바뀔때마다 연도 선택, 월/장르 선택은 매번 반복
time.sleep(2)
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tab02')))
ActionChains(driver).click(button).perform()
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'decade_1')))
driver.execute_script('arguments[0].click()', button)

scraping(driver, 2023)
scraping(driver, 2022)
scraping(driver, 2021)
scraping(driver, 2020)