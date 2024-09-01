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

NewsDf = pd.read_csv('newsdataIT1003.csv', encoding='utf-8-sig')
naver = []
kakao = []

medianame_list = []  # 언론사이름
headline_list = []  # 뉴스제목
all_list = []  # 본문내용
category_list = []  # 카테고리
image_list = []  # 이미지url
link_list = []  # 뉴스url
time_list = []

medianame_list2 = []  # 언론사이름
headline_list2 = []  # 뉴스제목
all_list2 = []  # 본문내용
category_list2 = []  # 카테고리
image_list2 = []  # 이미지url
link_list2 = []  # 뉴스url
time_list2 = []


for i in range(400):
    if '네이버' in NewsDf['뉴스제목'][i]:
        medianame_list.append(NewsDf['언론사'][i])  # 언론사이름
        headline_list.append(NewsDf['뉴스제목'][i]) # 뉴스제목
        all_list.append(NewsDf['본문내용'][i])  # 본문내용
        category_list.append(NewsDf['카테고리'][i])  # 카테고리
        image_list.append(NewsDf['이미지url'][i]) # 이미지url
        link_list.append(NewsDf['link'][i])  # 뉴스url
        time_list.append(NewsDf['시간'][i])

    elif '카카오' in NewsDf['뉴스제목'][i]:
        medianame_list2.append(NewsDf['언론사'][i])  # 언론사이름
        headline_list2.append(NewsDf['뉴스제목'][i])  # 뉴스제목
        all_list2.append(NewsDf['본문내용'][i])  # 본문내용
        category_list2.append(NewsDf['카테고리'][i])  # 카테고리
        image_list2.append(NewsDf['이미지url'][i])  # 이미지url
        link_list2.append(NewsDf['link'][i])  # 뉴스url
        time_list2.append(NewsDf['시간'][i])



NaverDic = {
    '언론사': medianame_list,
    '뉴스제목': headline_list,
    '본문내용': all_list,
    '카테고리': category_list,
    '이미지url': image_list,
    'link': link_list,
    '시간': time_list
}
KakaoDic = {
    '언론사': medianame_list2,
    '뉴스제목': headline_list2,
    '본문내용': all_list2,
    '카테고리': category_list2,
    '이미지url': image_list2,
    'link': link_list2,
    '시간': time_list2
}
NaverDf = pd.DataFrame(NaverDic)
KakaoDf = pd.DataFrame(KakaoDic)
file_name1 = 'Naver1003.csv'
file_name2 = 'Kakao1003.csv'
NaverDf.to_csv(file_name1, encoding='utf-8-sig', index=True)
KakaoDf.to_csv(file_name2, encoding='utf-8-sig', index=True)

