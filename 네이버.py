#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from enum import Enum
import pandas as pd

import chromedriver_autoinstaller
import calendar
import random
import math
import time


#크롬 드라이버로 url 주소 실행
def InitWeb(url = "", isMaximized = False) :
    if isMaximized :
        driver.maximize_window()
        
    driver.get(url)
    driver.implicitly_wait(10)

#return : soup
def GetSoup() :
    html = driver.page_source
    return BeautifulSoup(html, "html.parser")

#xPath 주소창에 key 검색 후 enter
def Search(xPath, key) :
    element = driver.find_element_by_xpath(xPath)
    element.click( )
    element.send_keys(key)
    element.send_keys("\n")
    driver.implicitly_wait(10)

#xPath 순차 클릭
def ClickXPath(xPathList) :
    for i in xPathList :
        try :
            driver.find_element_by_xpath(i).click()
        except :
            pass
        time.sleep(random.uniform(0.5, 1))
        
#txtList 순차 클릭
def ClickTxt(txtList) :
    for i in txtList :
        driver.find_element_by_link_text(i).click()
        time.sleep(random.uniform(0.5, 1))

#다 로딩될때까지 END 키
def PageDown() :
    while True : 
        prevCnt = len(GetSoup().find("ul", "lst_total").find_all("li"))
        element = driver.find_element_by_tag_name("body")
        element.send_keys(Keys.END)
        time.sleep(random.uniform(1, 1.2))
        if prevCnt == len(GetSoup().find("ul", "lst_total").find_all("li")) :
            break

#param1~2 리스트에 맞춰서 csv 형식으로 저장
#param1 첫행 리스트 / param2 나머지 데이터 리스트 리스트
def Save(param1, param2, csvPath) :
    df = pd.DataFrame()
    for i in range(0, len(param1)) :
        df[param1[i]]=pd.Series(param2[i])
        df.to_csv(csvPath,index=False, encoding="utf-8-sig")
        
#크롬 드라이버
chromedriver_autoinstaller.install(True)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


#===============================================================
#                     네이버 함수
#===============================================================

#네이버 날짜 검색
def SetNaverDate(yyyymmdd, naverType) :
    date = yyyymmdd.split("-")
    
    liNum = divNum = baseYear = 0
    
    if naverType == NaverType.Blog :
        liNum = 3
        divNum = 2
        baseYear = 2002
        
    elif naverType == NaverType.Cafe :
        liNum = 4
        divNum = 2
        baseYear = 1989
    
    elif naverType == NaverType.News :
        liNum = 2
        divNum = 3
        baseYear = 1989

    basePath = '//*[@id="snb"]/div[2]/ul/li[%s]/div/div[%s]/div[2]/div[YMD]/div/div/div/ul/li[NUM]/a' %(liNum, divNum)
    yearPath = basePath.replace("YMD", "1").replace("NUM", str(int(date[0])-baseYear))
    monthPath = basePath.replace("YMD", "2").replace("NUM", date[1])
    datePath = basePath.replace("YMD", "3").replace("NUM", date[2])
    
    xPathList.append(yearPath)
    xPathList.append(monthPath)
    xPathList.append(datePath)
    
#네이버 날짜 월별 1~말일 검색후 필요시 마지막 페이지까지
def SearchNaverByMonth(year, month, naverType) :
    startDate = "%s-%s-%s" %(year, month, "1")
    endDate = "%s-%s-%s" %(year, month, calendar.monthrange(year, month)[1])

    isView = False
    liNum = divNum = 0
    
    if naverType == NaverType.Blog :
        isView = True
        liNum = 3
        divNum = 2
        
    elif naverType == NaverType.Cafe :
        isView = True
        liNum = 4
        divNum = 2
    
    elif naverType == NaverType.News :
        isView = False
        liNum = 2
        divNum = 3
        
    path0 = '//*[@id="snb"]/div[2]/ul/li[%s]/div/div[1]/a[9]' %liNum
    path1 = '//*[@id="snb"]/div[2]/ul/li[%s]/div/div[%s]/div[1]/span[3]/a' %(liNum, divNum)
    path2 = '//*[@id="snb"]/div[2]/ul/li[%s]/div/div[%s]/div[3]/button' %(liNum, divNum)
    
    xPathList.clear()
    xPathList.append(path0)
    SetNaverDate(startDate, naverType)
    xPathList.append(path1)
    SetNaverDate(endDate, naverType)
    xPathList.append(path2)
    ClickXPath(xPathList)
    
    if isView :
        PageDown()      
            
#네이버 블로그 리스트 저장
def GetNaverBlog() :
    for i in range(1, 1001) :
        try :
            xPath = '//*[@id="sp_blog_%s"]/div/div/a' %i
            target = driver.find_element_by_xpath(xPath)
        except :
            break
            
        title = target.text.strip()
        target.send_keys(Keys.CONTROL + "\n")
        driver.switch_to.window(driver.window_handles[1])

        driver.implicitly_wait(10)

        try :
            driver.switch_to.frame("mainFrame")
        except :
            pass

        data = ""
        try :
            data = GetSoup().find("div", "se-main-container")
            len(data)
        except :
            try :
                data = GetSoup().find("div", id="postViewArea")
                len(data)
            except :
                try :
                    data = GetSoup().find("div", "se_component_wrap sect_dsc __se_component_area")
                    len(data)
                except :
                    titleList.append(title)
                    contentList.append(" ")
                    DebugLog()
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

        contents = ""
        for j in data :
            try :
                txt = j.get_text().strip()
                contents = contents + txt
            except :
                pass
                
        titleList.append(title)
        contentList.append(contents)
        DebugLog()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

#네이버 카페 검색
def SearchNaverCafe() :
    try :
        driver.switch_to.frame("cafe_main")
    except :
        pass

    time.sleep(random.uniform(1, 1.2))

    try :
        return GetSoup().find("div", "ContentRenderer").get_text().strip()
    except :
        return "Fail"

#네이버 카페 리스트 저장
def GetNaverCafe() :
    for i in range(1, 1001) :
        try :
            xPath = '//*[@id="_view_review_body_html"]/div/more-contents/div/ul/li[%i]/div/div/a' %i
            target = driver.find_element_by_xpath(xPath)
        except :
            break
            
        title = target.text.strip()
        target.send_keys(Keys.CONTROL + "\n")
        driver.switch_to.window(driver.window_handles[1])

        driver.implicitly_wait(10)
        
        contents = ""
        while True :
            contents = SearchNaverCafe()
            if contents != "Fail" :
                break

        titleList.append(title)
        contentList.append(contents)
        DebugLog()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
#네이버 뉴스 리스트 저장
def GetNaverNews() :
    while True :
        data = GetSoup().find("ul", "list_news").find_all("div", "news_area")

        for i in data :
            title = i.find("a", "news_tit").get_text().strip()
            contents = i.find("div", "dsc_wrap").get_text().strip()

            titleList.append(title)
            contentList.append(contents)
            DebugLog()

        prevUrl = driver.current_url

        driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div/a[2]').click()
        driver.implicitly_wait(10)

        if prevUrl == driver.current_url :
            break        
        
#네이버 타입에 따라 다른 본문리스트 저장
def SwitchNaver(naverType) :
    if naverType == NaverType.Blog :
        GetNaverBlog()
    elif naverType == NaverType.Cafe :
        GetNaverCafe()
    elif naverType == NaverType.News :    
        GetNaverNews()

#디버그 로그
def DebugLog() :
    idx = len(contentList) - 1
    print("번호 : %s" %(idx + 1))
    print("제목 : %s" %titleList[idx])
    print("내용 :\n%s" %contentList[idx])
    print("=" * 80)
    
#네이버 enum
class NaverType(Enum) :
    Blog = 1
    Cafe = 2
    News = 3


# In[ ]:


## ===============================================================
#                     네이버 블로그/카페/뉴스 검색
#===============================================================

#변수
xPathList = list()
txtList = list()
titleList = list()
contentList = list()
naverType = NaverType

#input
searchType = int(input("검색 할 타입[Blog = 1/Cafe = 2/News = 3] (ex.1) : "))
naverType = NaverType(searchType)

keyword = input("네이버 검색 단어 : ")
sYear = int(input("시작년도 (ex.2019) : "))
sMonth = int(input("시작월 (ex.3) : "))
eYear = int(input("끝년도 (ex.2020) : "))
eMonth = int(input("끝월 (ex.2) : "))
savePath = input("저장위치 (ex.C:/py_temp/test.csv) : ")


InitWeb("https://www.naver.com/")
Search('//*[@id="query"]', keyword)

if naverType == NaverType.Blog :
    txtList.append("VIEW")
    txtList.append("블로그")
    txtList.append("옵션")

elif naverType == NaverType.Cafe :
    txtList.append("VIEW")
    txtList.append("카페")
    txtList.append("옵션")
    
elif naverType == NaverType.News :
    txtList.append("뉴스")
    txtList.append("옵션")

ClickTxt(txtList)

for i in range(sYear, eYear + 1) :
    if sYear == eYear :
        for j in range(sMonth, eMonth + 1) :
            SearchNaverByMonth(i, j, naverType)
            SwitchNaver(naverType)
    else :
        if i != eYear :
            for j in range(sMonth, 13) :
                SearchNaverByMonth(i, j, naverType)
                SwitchNaver(naverType)
        else :
            for j in range(1, eMonth + 1) :
                SearchNaverByMonth(i, j, naverType)
                SwitchNaver(naverType)
                    
#csv 파일로 저장
param1 = ["번호", "제목", "내용"]
numList = list(range(1, len(titleList) + 1))
param2 = [numList, titleList, contentList]
Save(param1, param2, savePath)

