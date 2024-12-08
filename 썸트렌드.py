#!/usr/bin/env python
# coding: utf-8

# In[2]:


from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

import chromedriver_autoinstaller
import calendar
import random
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

#END 키
def PageDown() :
    element = driver.find_element_by_tag_name("body")
    element.send_keys(Keys.END)
    time.sleep(random.uniform(1, 1.2))
        
#param1~2 리스트에 맞춰서 csv 형식으로 저장
#param1 첫행 리스트 / param2 나머지 데이터 리스트 리스트
def Save(param1, param2, csvPath) :
    df = pd.DataFrame()
    for i in range(0, len(param2)) :
        df[param1[i]] = pd.Series(param2[i])
    df.to_csv(csvPath,index = False, encoding = "utf-8-sig")

#===============================================================
#                     썸트렌드 함수
#===============================================================
def NaverLogin() :
    xPathId = ["id", "pw"]
    idPw = ["twgh0195", "0p9o8i7u!!"]

    for i in range(2) :
        xPath = '//*[@id="%s"]' %xPathId[i]
        element = driver.find_element_by_xpath(xPath)
        element.click( )

        for j in idPw[i] :
            element.send_keys(j)
            time.sleep(random.uniform(0.1, 0.3))

    ClickXPath(['//*[@id="log.login"]'])

def SelectDate(year, month) :
    selectNum = [2, 1]
    yymm = [year, int(month) - 2]

    if yymm[1] == -1 :
        yymm = [yymm[0] - 1, 11]

    baseXPath = "/html/body/div[11]/div[3]/div[1]/table/tbody/tr[%s]/td[%s]"
    initDayXPath = baseXPath %(3, 3)
    
    time.sleep(random.uniform(1, 1.5))
    
    for i in range(len(yymm)) :
        baseXPath2 = "/html/body/div[11]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[%s]" %selectNum[i]
        Select(driver.find_element_by_xpath(baseXPath2)).select_by_value(str(yymm[i]))
        
    time.sleep(random.uniform(1, 1.5))
        
    driver.find_element_by_xpath(initDayXPath).click()
    driver.find_element_by_xpath(initDayXPath).click()

    ClickXPath(['//*[@id="searchDates"]'])

    leftCal = GetSoup().find("div", "drp-calendar right")

    offEnds = leftCal.find_all("td", "off ends available")
    available = leftCal.find_all("td", "available")

    startDay = startIdx = 0
    for i in available :
        startIdx += 1
        if i.get_text() == "1" :
            startDay = i
            break

    endDate = calendar.monthrange(year, month)[1]
    endIdx = endDate + startIdx - 2

    day = [startDay.get("data-title"), available[endIdx].get("data-title")]
    dayTr = list(range(2))
    dayTd = list(range(2))

    for i in range(2) :
        dayTr[i] = int(day[i][1]) + 1
        dayTd[i] = int(day[i][3]) + 1

    sDayXPath = baseXPath %(dayTr[0], dayTd[0])
    eDayXPath = baseXPath %(dayTr[1], dayTd[1])

    driver.find_element_by_xpath(sDayXPath).click()
    driver.find_element_by_xpath(eDayXPath).click()

def GetRankList() :
    keywordList = list()
    reputationList = list()
    countList = list()

    data = GetSoup().find("table", "table-associated-ranking table-associated-ranking-total analysis-without-top-card").find_all("tr")
    for i in data :
        keyword = i.find("td", "keyword").get_text()
        count = i.find("td", "count").get_text()
        keywordList.append(keyword)
        countList.append(count)
        
        if typeNum == 2 :
            reputation = i.find("td", "reputation").get_text()
            reputationList.append(reputation)
    
    if typeNum == 2:
        return [keywordList, reputationList, countList]
    else :
        return [keywordList, countList]

def SearchData(year, month) :
    ClickXPath(['//*[@id="searchDates"]'])

    time.sleep(random.uniform(1, 1.5))
    SelectDate(year, month)
    
    baseKey = "%s-%s" %(year, month)
    keywordKey = "%s_%s" %(baseKey, "keyword")
    repuKey = "%s_%s" %(baseKey, "reputation")
    countKey = "%s_%s" %(baseKey, "count")
    
    endDay = calendar.monthrange(year, month)[1]
    dataLists = list()

    num = 0
    while True :
        time.sleep(random.uniform(1, 1.5))
        headerDate = GetSoup().find("p", "layout-card-header-date").get_text()
        temp = headerDate.replace("~", ".")
        date = temp.split(".")
        
        try :
            if date[2] == "01" :
                if date[5] == str(endDay) :
                    dataLists = GetRankList()
                    break
        except :
            pass
        
        if num == 3 :
            emptyList = ["-"] * 15
            dataLists = [emptyList] * 3
            break
            
        num += 1
        
    dataDict[keywordKey] = dataLists[0]
    
    if typeNum == 2 :
        dataDict[repuKey] = dataLists[1]
        dataDict[countKey] = dataLists[2]
    else :
        dataDict[countKey] = dataLists[1]
        
    print("=" * 80)
    print(baseKey)
    print(dataDict[keywordKey])
    print(dataDict[countKey])
    
def SaveData(path, name) :
    dataCnt = len(dataDict)
    keyList = list(range(dataCnt))
    valueList = list(range(dataCnt))

    for i in dataDict.keys() :
        keyList.append(i)

    for i in dataDict.values() :
        valueList.append(i)

    del keyList[0 : len(dataDict)]
    del valueList[0 : len(dataDict)]

    Save(keyList, valueList, path + name + ".csv")
#=============================================================== 
    
#크롬 드라이버
chromedriver_autoinstaller.install(True)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

#시작
InitWeb("https://some.co.kr/")
ClickTxt(["로그인", "네이버 계정으로 로그인"])
time.sleep(random.uniform(0.5, 1))


# In[ ]:


#로그인 누르고 진행
#NaverLogin()
#아이디 : twgh0195
#비밀번호 : 0p9o8i7u!!
#검색단어 : 경사로, 목욕리프트, 수동침대, 수동휠체어, 욕창예방 매트리스, 이동욕조, 전동침대

typeNum = int(input("1 = 연관어 분석\n2 = 긍 · 부정 분석\n분석 타입 : (ex.1) : "))
keys = input("검색할 단어 (ex.가, 나, 다) : ")
sYear = int(input("시작년도 (ex.2019) : "))
sMonth = int(input("시작월 (ex.5) : "))
eYear = int(input("끝년도 (ex.2021) : "))
eMonth = int(input("끝월 (ex.4) : "))
savePath = input("저장위치 (ex.C:/py_temp/) : ")

keyList = keys.split(", ")

for i in keyList :  
    dataDict = dict(list())
    InitWeb("https://some.co.kr/", True)

    try :
        ClickTxt(["확인"])
    except :
        pass

    rType = "연관어 분석"
    if typeNum == 2 :
        rType = "긍 · 부정 분석"

    Search('//*[@id="mainSearchWrap"]/dl/dd/div[1]/div/input', i)
    
    try :
        ClickTxt(["다시보지않기", rType, "다시보지않기"])
    except :
        ClickTxt([rType])
    
    ClickXPath(['//*[@id="searchOptionInstaLabel"]/span[2]'])
    PageDown()

    for j in range(sYear, eYear + 1) :
        if sYear == eYear :
            for k in range(sMonth, eMonth + 1) :
                SearchData(j, k)
        else :
            if j != eYear :
                for k in range(sMonth, 13) :
                    SearchData(j, k)
            else :
                for k in range(1, eMonth + 1) :
                    SearchData(j, k)

    SaveData(savePath, i)

