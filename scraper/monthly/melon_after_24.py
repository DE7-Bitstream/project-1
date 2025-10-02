from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time



def scraping_genre(driver):
    info_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn.button_icons.type03.song_info')))

    genres = []
    for i in range(len(info_buttons)):
        ActionChains(driver).click(info_buttons[i]).perform()
        genre = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]')))
        genres.append(genre.text)
        driver.back()

    return genres



def scraping_all(driver, year, month):
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'button_icons.etc.arrow_d')))
    ActionChains(driver).click(button).perform()

    if year == 2024:
        prev_year_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn_round.small.pre')))
        ActionChains(driver).click(prev_year_btn).perform()

    month_calender = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'month_calendar')))
    month_buttons = month_calender.find_elements(By.CLASS_NAME, 'btn')

    ActionChains(driver).click(month_buttons[month]).perform()
    time.sleep(3)

    titles, singers, albums = [], [], []
    data = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'wrap_song_info')))
    for i in range(len(data)):
        if i % 2 == 0:
            title, singer = data[i].text.split('\n')
            titles.append(title)
            singers.append(singer)

        else:
            album = data[i].text
            albums.append(album)

    genres = scraping_genre(driver)

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



driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
URL = 'https://www.melon.com/chart/month/index.htm'
driver.get(URL)

titles, singers, albums, genres = scraping_all(driver, 2025, 2)
make_df(titles, singers, albums, genres, 2025, 3)

#for i in range(12):
#    titles, singers, albums, genres = scraping_all(driver, 2024, i)
#    make_df(titles, singers, albums, genres)