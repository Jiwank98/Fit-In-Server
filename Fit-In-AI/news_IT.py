
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
from copy import deepcopy

medianame_list = []  # 언론사이름
headline_list = []  # 뉴스제목
all_list = []  # 본문내용
category_list = []  # 카테고리
image_list = []  # 이미지url
link_list = []  # 뉴스url
time_list = []
    
def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    return driver
    
def open_dr(driver, link):
    driver.get(link)
    return driver
    
def close_dr(driver):
    driver.close()
    
def get_news(m,date):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    date = str(date)
    url_origin = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=%s&date=%s' % (m,date)
    dx = get_chrome_driver()
    driver = open_dr(dx, url_origin)
    driver.maximize_window()
    driver.get(url_origin)
    time.sleep(1)

    url_list = []

    page_r = driver.find_element(By.CLASS_NAME, "paging")
    page = page_r.find_elements(By.TAG_NAME,"a")
    url_list.append(url_origin)
    for url_page in page:
        url_list.append(url_page.get_attribute('href'))
    print(url_list)
    close_dr(driver)
    d = get_chrome_driver()
    if len(url_list)==1:
        k =1
    else:
        k = len(url_list)-1
    for i in range(0,k):
        p = str(i)
        url = url_list[i]
        driver= open_dr(d,url)
        driver.maximize_window()
        driver.get(url)
        time.sleep(1)
    
        for x in range(1, 5):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DOWN)
        time.sleep(1)

    # 언론사
        media_name = driver.find_elements(By.CLASS_NAME, "writing")
        for mdeia in media_name:
            medianame_list.append(mdeia.text)

        for k in range(1, 3):
            for j in range(1,11):
            # 뉴스클릭
                try:
                    news = '//*[@id="main_content"]/div[2]/ul[%d]/li[%d]/dl/dt[2]/a' % (k, j)
                    driver.find_element(By.XPATH, news).click()
                    time.sleep(1)
                except:
                    news2 = '//*[@id="main_content"]/div[2]/ul[%d]/li[%d]/dl/dt/a' % (k, j)
                    driver.find_element(By.XPATH, news2).click()
                    time.sleep(1)
    
    
    
    
                # 제목
                try:
                    news_name = driver.find_element(By.CLASS_NAME, 'media_end_head_headline')
                except:
                    news_name = driver.find_element(By.CLASS_NAME, 'end_tit')
                headline_list.append(news_name.text)
    
    
                try:
                    all_name = driver.find_elements(By.XPATH, '//*[@id="dic_area"]')
                    for all_n in all_name:
                        all_list.append(all_n.text)
                except:
                    all_name = driver.find_elements(By.XPATH, '//*[@id="articeBody"]')
                    for all_n in all_name:
                        all_list.append(all_n.text)
    
                if len(all_name) ==0:
                    all_list.append('No Article')

    
                try:
                    time_name = driver.find_element(By.XPATH, '//*[@id="ct"]/div[1]/div[3]/div[1]/div/span')
                    time_list.append(time_name.text)
                except:
                    time_name = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div[2]/span/em')
                    time_list.append(time_name.text)
    
    
            # 카테고리
                if (m == '230'):
                    category_list.append('IT 일반')
                if (m == '283'):
                    category_list.append('컴퓨터')
    
                # url
                try:
                    img = driver.find_element(By.CSS_SELECTOR, '#img1')
                    imgurl = img.get_attribute('src')
                    image_list.append(imgurl)
                except:
                    image_list.append('No image')
    
                    # link
                link_list.append(driver.current_url)
                driver.back()
    
            for y in range(1, 5):
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DOWN)
                time.sleep(1)
    close_dr(driver)
    

    
NewsDic = {
    '언론사': medianame_list,
    '뉴스제목': headline_list,
    '본문내용': all_list,
    '카테고리': category_list,
    '이미지url': image_list,
    'link': link_list,
    '시간': time_list
    }
    
for z in range(1, 3):
    if (z == 1):
        m = "{:03d}".format(230)  # IT 과학
    if (z == 2):
        m = "{:03d}".format(283)  # 컴퓨터
    date =20220930
    for i in range(1,21):
        get_news(m,date)
        date = date -1
    
print(len(medianame_list))
print(len(headline_list))
print(len(all_list))
print(len(image_list))
print(len(link_list))
print(len(category_list))
print(len(time_list))
    
NewsDf = pd.DataFrame(NewsDic)
    
NewsDf['언론사'] = medianame_list
NewsDf['뉴스제목'] = headline_list
NewsDf['본문내용'] = all_list
NewsDf['이미지url'] = image_list
NewsDf['link'] = link_list
NewsDf['카테고리'] = category_list
NewsDf['시간'] = time_list
file_name = 'newsdataIT1007.csv'
NewsDf.to_csv(file_name, encoding='utf-8-sig', index=True)