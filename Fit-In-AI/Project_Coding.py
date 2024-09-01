import re

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import time
from IPython.display import display
from datetime import datetime

date = str(datetime.now())
date = date[:date.rfind(':')].replace(' ', '_')
date = date.replace(':','시') + '분'

warnings.filterwarnings(action='ignore')

def get_url():
    keyword=input('검색어를 입력하세요 : ')
    news_num=int(input('총 필요한 뉴스기사 수를 입력하세요 : '))
    keyword=keyword.replace(' ','+')

    url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query={}'.format(keyword)
    driver = webdriver.Chrome(executable_path='C:/Users/김지완/Desktop/study/자바스터디/Fit-In-AI/chromedriver.exe')
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')

    n = 3
    while n > 0:
        print('웹페이지를 불러오는 중입니다..' + '..' * n)
        time.sleep(1)
        n -= 1

    i=0
    cur_page=1

    newsDict = {}
    while i<news_num:
        table=soup.find('ul',{'class' : 'list_news'})
        li_list= table.find_all('li',{'id' : re.compile('sp_nws.*')})
        area_list=[li.find('div',{'class' : 'news_area'}) for li in li_list]
        a_list=[area.find('a',{'class' : 'news_tit'}) for area in area_list]

        for n in a_list[:min(len(a_list),news_num-i)]:
            newsDict[i]={'제목' : n.get('title'),
                         '주소' : n.get('href')}
            i+=1
        cur_page+=1

        pages=soup.find('div',{'class' : 'sc_page_inner'})
        next_page_url=[p for p in pages.find_all('a') if p.text==str(cur_page)][0].get('href')

        req = webdriver.Chrome(executable_path='C:/Users/김지완/Desktop/study/자바스터디/Fit-In-AI/chromedriver.exe')
        req.get('https://search.naver.com/search.naver' +next_page_url)
        soup = bs(req.page_source, 'html.parser')



    newsDf = pd.DataFrame(newsDict).T
    file_name='네이버뉴스_{}_{}.csv'.format(keyword,date)
    newsDf.to_csv(file_name,encoding='utf-8-sig', index=False)
    driver.close()

    result = input('데이터프레임 저장이 완료되었습니다! 데이터프레임을 조회하시겠습니까? (y/n)')
    if result == 'y':
        display(newsDf)
        question = input('원하는 뉴스링크를 확인 하시겠습니까? (y/n)')
        if question == 'y':
            button = int(input('확인하고자 하는 뉴스의 번호(출력된 표 가장 왼쪽의 번호)를 입력해주세요.'))
            driver = webdriver.Chrome(executable_path='C:/Users/김지완/Desktop/study/자바스터디/Fit-In-AI/chromedriver.exe')
            driver.get(newsDf['주소'][button])
        else:
            return '프로그램을 종료합니다.'
    else:
        return '프로그램을 종료합니다.'

get_url()





