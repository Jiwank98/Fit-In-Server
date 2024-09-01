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

warnings.filterwarnings(action='ignore')

def get_url():
    keyword=input('검색어를 입력하시오 : ')
    url = 'https://www.youtube.com/results?search_query={}'.format(keyword)
    driver = webdriver.Chrome(executable_path='C:/Users/김지완/Desktop/study/자바스터디/Fit-In-AI/chromedriver97.exe')
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')

    n = 3
    while n > 0:
        print('웹페이지를 불러오는 중입니다..' + '..' * n)
        time.sleep(1)
        n -= 1

    name_list = []
    url_list = []
    view_list = []

    youtubeDic = {
        '제목': name_list,
        '주소': url_list,
        '조회수': view_list
    }

    name = soup.select('a#video-title')
    video_url = soup.select('a#video-title')
    view = soup.select('a#video-title')

    for i in range(len(name)):
        name_list.append(name[i].text.strip())
        view_list.append(view[i].get('aria-label').split()[-1])
    for i in video_url:
        url_list.append('{}{}'.format('https://www.youtube.com', i.get('href')))

    youtubeDf = pd.DataFrame(youtubeDic)
    youtubeDf['제목']=name_list
    youtubeDf['주소'] = url_list
    youtubeDf['조회수'] = view_list
    youtubeDf.to_csv('kk.csv', encoding='utf-8-sig', index=False)
    driver.close()

    result = input('데이터프레임 저장이 완료되었습니다! 데이터프레임을 조회하시겠습니까? (y/n)')
    if result == 'y':
        display(youtubeDf)
        question = input('승여니가 원하는 영상이 뭐양? (y/n)')
        if question == 'y':
            button = int(input('재생하고자 하는 영상의 번호(출력된 표 가장 왼쪽의 번호)를 입력해주세요.'))
            driver = webdriver.Chrome(executable_path='C:/Users/김지완/Desktop/study/자바스터디/Fit-In-AI/chromedriver97.exe')
            driver.get(youtubeDf['주소'][button])
        else:
            return '프로그램을 종료합니다.'
    else:
        return '프로그램을 종료합니다.'

get_url()





