#!/usr/bin/env python
# coding: utf-8

# In[8]:


from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# In[9]:


def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(ChromeDriverManager().install())

    return driver


# In[10]:


def open_dr(driver, link):
    driver.get(link)
    return driver


def get_link():
    link = []
    for i in range(1):
        link.append(
            "https://recruit.navercorp.com/rcrt/list.do?annoId=&sw=&subJobCdArr=1010001%2C1010002%2C1010003%2C1010004%2C1010005%2C1010006%2C1010007%2C1010008%2C1010009&sysCompanyCdArr=&empTypeCdArr=&entTypeCdArr=&workAreaCdArr=".format(i))
        link.append(
            "https://recruit.navercorp.com/rcrt/list.do?annoId=&sw=&subJobCdArr=1020001%2C1030001%2C1030002%2C1040001%2C1050001%2C1050002%2C1060001&sysCompanyCdArr=&empTypeCdArr=&entTypeCdArr=&workAreaCdArr=".format(i))
    return link


def close_dr(driver):
    driver.close()


# In[11]:


def crawl():
    start_time = time.time()
    link = get_link()
    for i in range(len(link)):
        print(len(link))

        d = get_chrome_driver()
        driver = open_dr(d, link[i])
        now = datetime.datetime.now()
        print("test code- 현재 시간 출력하기")
        print(now)
        a_t = driver.find_elements(By.CSS_SELECTOR,
                                   '#__next > div.JobList_cn__t_THp > div > div > div.List_List_container__JnQMS > ul > li > div > a > div > div.job-card-company-name')
        num_per_page = len(a_t)

        title_links = []
        company_links = []
        date_links = []
        info_links = []
        url_links = []

        print(a_t[0].text)

        print(num_per_page)
        print("success")
        driver.close()
    print("--- %s seconds ---" % (time.time() - start_time))


def crawl2(link):
    d = get_chrome_driver()
    driver = open_dr(d, link)
    now = datetime.datetime.now()
    print("test code- 현재 시간 출력하기")
    print(now)

    com_name_list = [] # 회사이름
    job_name_list = [] #직무
    tag_list = [] #카테고리
    car_list = [] #경력유무
    cru_list = [] #정규직
    time_list = [] #모집기간
    # 회사이름
    com_name = driver.find_elements_by_css_selector(
        '#naver > div > section > div > div > div.sub_container > div.card_wrap > ul > li> div.company_logo > div')
    for com in com_name:
        com_name_list.append(com.text)
    print(com_name_list)

    #직무모집
    job_name = driver.find_elements_by_css_selector('#naver > div > section > div > div > div.sub_container > div.card_wrap > ul > li> a > h4')
    for j in job_name:
        job_name_list.append(j.text)
    print(job_name_list)

    #카테고리
    tag_name = driver.find_elements_by_xpath(
        '//*[@id="naver"]/div/section/div/div/div[2]/div[2]/ul/li/a/dl/dd[2]')
    for tag in tag_name:
        tag_list.append(tag.text)
    print(tag_list)

    #모집시기
    range_name = driver.find_elements_by_xpath('//*[@id="naver"]/div/section/div/div/div[2]/div[2]/ul/li/a/dl/dd[5]')
    for r in range_name:
        time_list.append(r.text)
    print(time_list)

    #경력유무
    car_name = driver.find_elements_by_xpath(
        '//*[@id="naver"]/div/section/div/div/div[2]/div[2]/ul/li/a/dl/dd[3]')
    for car in car_name:
        car_list.append(car.text)
    print(car_list)

    # 정규직유무
    cru_name = driver.find_elements_by_xpath(
        '//*[@id="naver"]/div/section/div/div/div[2]/div[2]/ul/li/a/dl/dd[4]')
    for cru in cru_name:
        cru_list.append(cru.text)
    print(cru_list)

    # url
    link_set = []
    link_url = []
    a_link = driver.find_elements(By.CSS_SELECTOR,
                                  '#naver > div > section > div > div > div.sub_container > div.card_wrap > ul > li > a')
    for m in a_link:
        link_set.append(m.get_attribute('onclick'))

    for i in range(len(link_set)):
        if "'" in link_set[i]:
            link_url.append(f'https://recruit.navercorp.com/rcrt/view.do?annoId={link_set[i][6:-2]}')
        else:
            link_url.append(f'https://recruit.navercorp.com/rcrt/view.do?annoId={link_set[i][5:-1]}')
    print(link_url)


    print("success")
    driver.close()
    return com_name_list,job_name_list,tag_list,car_list,cru_list,time_list,link_url,driver


def make_csv(com_name_list,job_name_list,tag_list,car_list,cru_list,time_list,link_url,driver):

    n = pd.DataFrame(index=range(0,10),columns=['회사이름','직무모집','카테고리','경력','정규직','모집기간','링크'])
    n['회사이름'] = com_name_list
    n['직무모집'] = job_name_list
    n['카테고리'] = tag_list
    n['경력'] = car_list
    n['정규직'] = cru_list
    n['모집기간'] = time_list
    n['링크'] = link_url
    with csv_writer_lock:
        with open('네이버_채용공고.csv', mode="a") as f1:
            review_writer = csv.writer(f1,delimiter=',')
            for i in range (0,10):
                review_writer.writerow(n.loc[i])
    f1.close()
    # FinalDf=NaverDf.append(n,ignore_index=True)
    # NaverDf.to_csv(file_name, encoding='utf-8-sig', index=False)


def crawlandcsv(link):
    com_name_list,job_name_list,tag_list,car_list,cru_list,time_list,link_url,driver=crawl2(link)
    make_csv(com_name_list,job_name_list,tag_list,car_list,cru_list,time_list,link_url,driver)




import time
import schedule
import datetime
from multiprocessing import Pool, freeze_support
import csv
from IPython.display import display
import re

from selenium import webdriver
import numpy as np
import pandas as pd

global NaverDf, FinalDf
import threading
csv_writer_lock = threading.Lock()

NaverDf = pd.DataFrame(columns=['회사이름','직무모집','카테고리','경력','정규직','모집기간','링크'])



def all():
    start_time = time.time()
    print(start_time)

    global file_name
    file_name = '네이버_채용공고.csv'
    NaverDf.to_csv(file_name, encoding='utf-8-sig', index=False)
    pool = Pool(processes=2)  # 4개의 프로세스를 사용합니다.
    link = get_link()
    pool.map(crawlandcsv, link)  # get_contetn 함수를 넣어줍시다.
    print("--- %s seconds ---" % (time.time() - start_time))


import sys

print("****************네이버 채용공고 크롤링*******************")
if __name__ == '__main__':
    freeze_support()

    # 스케쥴 모듈이 동작시킬 코드 : 현재 시간 출력
    schedule.every(60).seconds.do(all)
    #schedule.every().day.at("19:37").do(all)
    while True:
        schedule.run_pending()
        time.sleep(1)






