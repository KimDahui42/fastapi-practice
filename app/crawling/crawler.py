from cgitb import enable
import os
import json
from multiprocessing import Pool
import requests
import time
from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor
#import selenium
from selenium import webdriver as wd
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#import beautiful soup
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup


def set_chrome_driver():
    chrome_options = wd.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])
    chrome_options.headless = True
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = wd.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    return driver


def waitUntilGetSingle(driver,path):
    data = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH,path))
    )
    return data


def waitUntilGetMulti(driver,path):
    data = WebDriverWait(driver,20).until(
        EC.presence_of_all_elements_located((By.XPATH,path))
    )
    return data


def waitUntilClickSingle(act,driver,path):
    act.click(WebDriverWait(driver,20).until(
        EC.element_to_be_clickable((By.XPATH,path))
    )).perform()
    time.sleep(3)


def openInNewPage(element):
    element.send_keys(Keys.CONTROL+"\n")


def getData():
    date = dt.now().strftime('%Y-%m-%d')
    #url 목록
    urls = {
        'Kstartup':'https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do',#Kstartup
        '기업마당':'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do',#기업마당
        'SBA 서울산업진흥원':'https://www.sba.seoul.kr/Pages/ContentsMenu/Company_Support.aspx?C=6FA70790-6677-EC11-80E8-9418827691E2',#SBA 서울산업진흥원
        'SMtech':'https://www.smtech.go.kr/front/ifg/no/notice02_list.do',#SMtech
        'iitp':'https://www.iitp.kr/kr/1/business/businessApiList.it',#iitp
        '중소벤처24':'https://www.smes.go.kr/bizApply',#중소벤처24
        '중소벤처기업부':'https://www.mss.go.kr/site/smba/ex/bbs/List.do?cbIdx=310',#중소벤처기업부
        '이노비즈':'https://www.innobiz.net/company/company1_list.asp',#이노비즈
        '창조경제혁신센터':'https://ccei.creativekorea.or.kr/service/business_list.do',#창조경제혁신센터
        '중소기업기술정보진흥원':'https://www.tipa.or.kr/s0201',#중소기업기술정보진흥원
        '소상공인시장진흥공단':'https://www.semas.or.kr/index_main.html',#소상공인시장진흥공단
        '소상공인마당':'https://www.sbiz.or.kr/sup/custcenter/notice/notice.do',#소상공인마당
        '한국콘텐츠진흥원':'https://www.kocca.kr/kocca/pims/list.do?menuNo=204104',#한국콘텐츠진흥원
        '정보통신산업진흥원':'https://www.nipa.kr/',#정보통신산업진흥원
        '경기컨텐츠진흥원':'https://www.gcon.or.kr/busiNotice?menuId=MENU02369',#경기컨텐츠진흥원
        '경기테크노파크':'https://pms.gtp.or.kr/web/business/webBusinessList.do',#경기테크노파크
        '경기대진테크노파크':'https://gdtp.or.kr/sproject/index',#경기대진테크노파크
        '고려대학교 창업지원단':'https://piportal.korea.ac.kr/front/board/list.do?sep_cd=NOTICE',#고려대학교 창업지원단
        '서울대학교 창업지원단':'https://startup.snu.ac.kr/front/lounge/notice',#서울대학교 창업지원단
        '연세대학교 창업지원단':'https://venture.yonsei.ac.kr/notice',#연세대학교 창업지원단
    }
    crawled_data={}
    crawled_data['Kstartup']=KStartUp(date,urls)
    crawled_data['기업마당']=BizInfo(date,urls)
    crawled_data['SMtech']=SMtech(date,urls)
    crawled_data['iitp']=Iitp(date,urls)
    return toJson(crawled_data,date)


# kstartup 크롤링 함수
def KStartUp(date,urls):
    print("start KStartUP crawling")
    kstartup_break_flag=False
    url=urls['Kstartup']
    #Selenium_webdriver 위치
    driver=set_chrome_driver()
    driver.get(url)
    act=ActionChains(driver)
    
    #사업 내용 딕셔너리 리스트 생성
    kstartup_list=[]

    list_xpath="//li[@class='notice']"
    #다음 페이지가 없음()
    waitUntilClickSingle(act,driver,"//div[@class='paginate']/a[last()]")
    max_idx=int(waitUntilGetSingle(driver,"//div[@class='paginate']/a[last()-2]").text)
    print(max_idx)
    waitUntilClickSingle(act,driver,"//div[@class='paginate']/a[1]")
    
    for idx in range(1,max_idx+1):
        if kstartup_break_flag:
            break
        # paginator 개수 구하기
        page_cnt=len(waitUntilGetMulti(driver,"//div[@class='paginate']/a"))-4
        # 다음페이지로 화면 전환
        temp_idx=idx%page_cnt
        next_page=f"//div[@class='paginate']/a[{temp_idx+2}]" 
        if temp_idx==0:
            next_page=f"//div[@class='paginate']/a[last()-2]"
            waitUntilClickSingle(act,driver,next_page)
            kstartup_list,kstartup_break_flag=KStartUpData(driver,date,kstartup_list,list_xpath)
            if idx!=max_idx:
                waitUntilClickSingle(act,driver,"//div[@class='paginate']/a[last()-1]")
        else:
            waitUntilClickSingle(act,driver,next_page)
            return_list=KStartUpData(driver,date,kstartup_list,list_xpath)
            kstartup_list=return_list[0]
            kstartup_break_flag=return_list[1]
    return kstartup_list


def KStartUpData(driver,date,kstartup_list,list_xpath):
    kstartup_break_flag=False
    temp_list_boxes=waitUntilGetMulti(driver,list_xpath)
    for list_box in temp_list_boxes:
        list_box_soup=BeautifulSoup(list_box.get_attribute('innerHTML'),"lxml")
        # 날짜가 date 일자에 올라온 공고라면
        list_day=list_box_soup.select('span.list')[2].text.strip()[5:]
        print(f'{list_day} and {date} is {list_day==date}')
        if list_day==date:
            openInNewPage(list_box.find_elements(By.TAG_NAME,"button")[1])
            driver.switch_to.window(driver.window_handles[1])
            temp_soup=BeautifulSoup(driver.page_source,"lxml")
            #데이터 저장
            title=temp_soup.select_one("#scrTitle").text
            agency=temp_soup.select_one("div.bg_box>ul.dot_list-wrap:nth-child(1)>li:nth-child(3) p.txt").text
            contact=temp_soup.select_one("div.bg_box>ul.dot_list-wrap:nth-child(1)>li:nth-child(4) p.txt").text
            event_date=temp_soup.select_one("#rcptPeriod").text.replace('\t','').replace('\n','').replace('\xa0',' ')
            kstartup_list_data={
                'title': title,
                'agency': agency,
                'contact': contact,
                'event_date': event_date,
                'upload_date': date,
            }
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            kstartup_list.append(kstartup_list_data)
        else:
            kstartup_break_flag=True
            break
    return kstartup_list,kstartup_break_flag


# 기업마당 크롤링 함수
def BizInfo(date,urls):
    print("start Bizinfo crawling")
    bizinfo_break_flag=False
    url=urls['기업마당']
    #Selenium_webdriver 위치
    driver=set_chrome_driver()
    driver.get(url)
    act=ActionChains(driver)
    
    #사업 내용 딕셔너리 리스트 생성
    bizinfo_list=[]
    # 1페이지 데이터 가져오기
    list_xpath="//div[@class='table_Type_1']/table/tbody/tr"

    #다음 페이지가 없음
    # 최대 이동 페이지는 10으로 설정됨   
    max_idx=10 
    for idx in range(1,max_idx+1):
        if bizinfo_break_flag:
            break
        # 다음페이지로 화면 전환-
        next_page=f"//div[@class='page_wrap']/a[last()-{12-idx}]"
        waitUntilClickSingle(act,driver,next_page)
        bizinfo_list,bizinfo_break_flag=BizInfoData(driver,date,bizinfo_list,list_xpath)
        break
    return bizinfo_list


def BizInfoData(driver,date,bizinfo_list,list_xpath):
    bizinfo_break_flag=False
    temp_list_boxes=waitUntilGetMulti(driver,list_xpath)
    for list_box in temp_list_boxes:
        list_box_soup=BeautifulSoup(list_box.get_attribute('innerHTML'),"lxml")
        # 날짜가 date 일자에 올라온 공고라면
        list_day=list_box_soup.select_one('td:nth-child(6)').text
        if list_day==date:
            driver.execute_script(f"window.open('https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/{list_box_soup.find('a')['href']}');")
            driver.switch_to.window(driver.window_handles[1])
            temp_soup=BeautifulSoup(driver.page_source,"lxml")
            #데이터 저장
            title=temp_soup.select_one("h2.title").text
            agency=temp_soup.select_one("div.view_cont>ul>li:nth-child(2)>div.txt").text.replace('\t','').replace('\n','').replace(' ','')
            contact="정보없음"
            event_date=temp_soup.select_one("div.view_cont>ul>li:nth-child(3)>div.txt").text.replace('\t','').replace('\n','').replace(' ','')
            bizinfo_list_data={
                'title': title,
                'agency': agency,
                'contact': contact,
                'event_date': event_date,
                'upload_date': date,
            }
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            bizinfo_list.append(bizinfo_list_data)
        else:
            bizinfo_break_flag=True
            break
    return bizinfo_list,bizinfo_break_flag


#smtech 크롤링 함수
def SMtech(date,urls):
    print("start SMtech crawling")
    smtech_break_flag=False
    url=urls['SMtech']
    #Selenium_webdriver 위치
    driver=set_chrome_driver()
    driver.get(url)
    act=ActionChains(driver)
    
    #사업 내용 딕셔너리 리스트 생성
    smtech_list=[]

    list_xpath='//*[@id="subcontent"]/div[2]/div[2]/table/tbody/tr'
    #공고 수가 적어 최대 두 페이지만 체크합니다.
    # 1페이지 데이터 가져오기
    smtech_list,smtech_break_flag=SMtechData(driver,date,smtech_list,list_xpath)
    if smtech_break_flag:
        return smtech_list
    # 2페이지 데이터 가져오기
    waitUntilClickSingle(act,driver,"//*[@id='paging']/a[4]")
    smtech_list,smtech_break_flag=SMtechData(driver,date,smtech_list,list_xpath)

    return smtech_list


def SMtechData(driver,date,smtech_list,list_xpath):
    smtech_break_flag=False
    temp_list_boxes=waitUntilGetMulti(driver,list_xpath)

    for list_box in temp_list_boxes:
        list_box_soup=BeautifulSoup(list_box.get_attribute('innerHTML'),"lxml")
        # 현재 접수중인 공고라면
        status=list_box_soup.find('img')['alt']
        if status=='접수중':
            driver.execute_script(f"window.open('https://www.smtech.go.kr{list_box_soup.find('a')['href']}');")
            driver.switch_to.window(driver.window_handles[1])
            temp_soup=BeautifulSoup(driver.page_source,"lxml")
            #데이터 저장
            title=temp_soup.select_one('div.l15 > table > tbody > tr:nth-child(2) > td').text.replace('\xa0',' ')
            agency=temp_soup.select_one('div.l15 > table > tbody > tr:nth-child(3) > td:nth-child(2)').text.replace('\xa0',' ')
            contact=temp_soup.select_one('div.l15 > table > tbody > tr:nth-child(3) > td.ll').text.replace('\xa0','').replace('\t','').replace('\n','').replace(' ','')
            event_date=temp_soup.select_one("div.l15 > table > tbody > tr:nth-child(4) > td:nth-child(2)").text.replace('\xa0','')+' ~ '+temp_soup.select_one('div.l15 > table > tbody > tr:nth-child(4) > td.ll').text.replace('\xa0','')
            smtech_list_data={
                'title': title,
                'agency': agency,
                'contact': contact,
                'event_date': event_date,
                'upload_date': date,
            }
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            smtech_list.append(smtech_list_data)
        else:
            smtech_break_flag=True
            break
    return smtech_list,smtech_break_flag


#smtech 크롤링 함수
def Iitp(date,urls):
    print("start iitp crawling")
    iitp_break_flag=False
    url=urls['iitp']
    #Selenium_webdriver 위치
    driver=set_chrome_driver()
    driver.get(url)
    act=ActionChains(driver)
    
    #사업 내용 딕셔너리 리스트 생성
    iitp_list=[]

    list_xpath='//*[@id="conArea"]/div[2]/table/tbody/tr'
    #공고 수가 적어 최대 두 페이지만 체크합니다.
    # 1페이지 데이터 가져오기
    iitp_list,iitp_break_flag=IitpData(driver,date,iitp_list,list_xpath)
    if iitp_break_flag:
        return iitp_list
    # 2페이지 데이터 가져오기
    waitUntilClickSingle(act,driver,'//ul[@class="pagination"]/li[4]/a')
    iitp_list,iitp_break_flag=IitpData(driver,date,iitp_list,list_xpath)

    return iitp_list


def IitpData(driver,date,iitp_list,list_xpath):
    iitp_break_flag=False
    temp_list_boxes=waitUntilGetMulti(driver,list_xpath)

    for list_box in temp_list_boxes:
        list_box_soup=BeautifulSoup(list_box.get_attribute('innerHTML'),"lxml")
        # 현재 접수중인 공고라면
        expired_date=dt.strptime(list_box_soup.select_one('td:nth-child(3)').text[11:],'%Y.%m.%d')
        current_date=dt.strptime(date,'%Y-%m-%d')
        print(expired_date-current_date)
        if expired_date>current_date:
            driver.execute_script(f"window.open('{list_box_soup.find('a')['href']}');")
            driver.switch_to.window(driver.window_handles[1])
            temp_soup=BeautifulSoup(driver.page_source,"lxml")
            #데이터 저장
            print(temp_soup.select_one('div.bbs_view_tit > strong'))
            title=temp_soup.select_one('div.bbs_view_tit > strong').text.replace('\xa0',' ').replace('\t','').replace('\n','')
            agency=temp_soup.select_one('div.bbs_view_info > span:nth-child(2)').text.replace('\xa0',' ').replace('\t','').replace('\n','')
            contact="정보없음"
            event_date=temp_soup.select_one('div.bbs_view_info > span:nth-child(1)').text.replace('\xa0',' ').replace('\t','').replace('\n','')
            iitp_list_data={
                'title': title,
                'agency': agency,
                'contact': contact,
                'event_date': event_date,
                'upload_date': date,
            }
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            iitp_list.append(iitp_list_data)
        else:
            iitp_break_flag=True
            break
    return iitp_list,iitp_break_flag



#딕셔너리 데이터 json 파일 저장 crawled data 폴더 "오늘일자".json
def toJson(data_list,date):
    try:
        os.makedirs(f'./crawled data')
    except:
        pass
    with open(f"./crawled data/{date}.json", 'w', encoding="UTF-8") as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)


def validateDate(date):
    try:
        dt.strptime(date,"%Y-%m-%d")
        return True
    except ValueError:
        print("잘못된 형식입니다.")

def tempMain():
    print("="*30)
    print("다음 중 선택해 주세요\n1. 오늘 날짜\n2. 다른 날짜")
    print("="*30)
    select_menu=input(">>> ")
    if select_menu=='1':
        today=dt.now().strftime('%Y-%m-%d')
        print("\n크롤링을 시작합니다....")
        getData(today)
        print("\n종료되었습니다.")
    else:
        while True:
            print("정보를 확인할 날짜를 입력해주세요.")
            date=input("입력 형식:yyyy-mm-dd >>> ").strip()
            if validateDate(date)==True:
                print("입력 데이터 : %s 크롤링을 시작합니다...." % date)
                getData(date)
                print("종료되었습니다.")
            else:
                print("입력 형식 오류")
                continue


if __name__=="__main__":
    print("\n크롤링을 시작합니다....")
    getData()
    print("\n종료되었습니다.")