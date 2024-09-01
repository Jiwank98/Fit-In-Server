from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import pandas as pd
from flask import Flask, render_template, send_file
import os
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(ChromeDriverManager().install())

    return driver

def open_dr(driver, link):
    driver.get(link)
    return driver

def close_dr(driver):
    driver.close()

def get_news():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    url = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=%s' % (m)
    print(m)
    d = get_chrome_driver()
    driver = open_dr(d, url)
    driver.maximize_window()
    driver.get(url)
    time.sleep(1)

    for x in range(0, 4):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DOWN)
    time.sleep(1)

    for j in range(2, 8):
        for a in range(1, 4):

            # 뉴스클릭
            news = '//*[@id="ct"]/div[2]/div[%d]/ul/li[%d]/a' % (j, a)
            driver.find_element(By.XPATH, news).click()
            time.sleep(1)

            # 언론사
            media_name = driver.find_element(By.CLASS_NAME, "writing")
            medianame_list.append(media_name.text)

            # 제목
            news_name = driver.find_element(By.CLASS_NAME, "media_end_head_headline")
            headline_list.append(news_name.text)

            # 전체내용
            all_name = driver.find_elements(By.XPATH, '//*[@id="dic_area"]')
            for all_n in all_name:
                all_list.append(all_n.text)

            # 카테고리

            if (z == 1 and j == 2):
                category_list.append('0')
            if (z == 1 and j == 3):
                category_list.append('1')
            if (z == 1 and j == 4):
                category_list.append('2')
            if (z == 1 and j == 5):
                category_list.append('3')
            if (z == 1 and j == 6):
                category_list.append('4')
            if (z == 1 and j == 7):
                category_list.append('5')

            if (z == 2 and j == 2):
                category_list.append('6')
            if (z == 2 and j == 3):
                category_list.append('7')
            if (z == 2 and j == 4):
                category_list.append('8')
            if (z == 2 and j == 5):
                category_list.append('9')
            if (z == 2 and j == 6):
                category_list.append('10')
            if (z == 2 and j == 7):
                category_list.append('11')

            if (z == 3 and j == 2):
                category_list.append('12')
            if (z == 3 and j == 3):
                category_list.append('13')
            if (z == 3 and j == 4):
                category_list.append('14')
            if (z == 3 and j == 5):
                category_list.append('15')
            if (z == 3 and j == 6):
                category_list.append('16')
            if (z == 3 and j == 7):
                category_list.append('17')

            # url
            try:
                img = driver.find_element(By.CSS_SELECTOR, '#img1')
                imgurl = img.get_attribute('src')
                image_list.append(imgurl)
            except:
                image_list.append('No image')

                # link
            link_list.append(driver.current_url)

            # category2
            if (j == 2):
                category2_list.append('정치')
            if (j == 3):
                category2_list.append('경제')
            if (j == 4):
                category2_list.append('사회')
            if (j == 5):
                category2_list.append('생활')
            if (j == 6):
                category2_list.append('세계')
            if (j == 7):
                category2_list.append('IT')

            driver.back()

        for y in range(0, 5):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DOWN)
        time.sleep(1)

    driver.quit()


medianame_list = []  # 언론사이름
headline_list = []  # 뉴스제목
all_list = []  # 본문내용
category_list = []  # 카테고리
image_list = []  # 이미지url
link_list = []  # 뉴스url
category2_list = []  # 카테고리2

NewsDic = {
    '언론사': medianame_list,
    '뉴스제목': headline_list,
    '본문내용': all_list,
    '핵심키워드': category_list,
    '이미지url': image_list,
    'link': link_list,
    '카테고리': category2_list
}

for z in range(1, 4):
    if (z == 1):
        m = "{:03d}".format(230)  # IT 과학
    if (z == 2):
        m = "{:03d}".format(226)  # 인터넷/sns
    if (z == 3):
        m = "{:03d}".format(283)  # 컴퓨터
    get_news()

NewsDf = pd.DataFrame(NewsDic)

NewsDf['언론사'] = medianame_list
NewsDf['뉴스제목'] = headline_list
NewsDf['본문내용'] = all_list
NewsDf['핵심키워드'] = category_list
NewsDf['이미지url'] = image_list
NewsDf['link'] = link_list
NewsDf['카테고리'] = category2_list

file_name = 'newsdata.csv'
NewsDf.to_csv(file_name, encoding='utf-8-sig', index=True)