import re
import pandas as pd
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from selenium import webdriver
from django.views.decorators.csrf import csrf_exempt
from time import sleep

from django.contrib import messages
from .models import member

#def f_login(request):
    #회원가입 db완성 후 로그인 시 id pw 받아와서 db랑 비교 후 일치 하면 다음 페이지로이동 아닐 시 예외 처리

@csrf_exempt
#------------------------------------시간표 crawling 부분(selenium)-------------------------------------------------

def login(request): #추후 시간표 크롤링함수로 이름 변경
    if request.method == "POST":
        def start2time(start):
            base = 900
            off_set = int(((start - 450) / 25) * 50)
            base += off_set
            if base % 100 != 0:
                base -= 20
            return base

        def class_len2time(class_len):
            base = 100
            off_set = int(((class_len - 51) / 25) * 50)
            base += off_set
            if base % 100 != 0:
                base -= 20
            return base

        # 로그인 url
        url = 'https://everytime.kr/login'
        options = webdriver.ChromeOptions()

        # 크롤러 실행 시 로그노출 안되도록 option 설정
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        user_id = request.POST['userid']  # 개인 아이디 입력

        user_pw = request.POST['userpw']  # 비밀번호 입력

        driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)

        driver.get(url)
        driver.set_window_size(1024, 630)
        # id값으로 ID,Password 입력창을 찾아준 후 값 입력
        driver.find_element_by_xpath('//*[@id="container"]/form/p[1]/input').send_keys(user_id)

        sleep(1)

        driver.find_element_by_xpath('//*[@id="container"]/form/p[2]/input').send_keys(user_pw)

        sleep(2)

        # 로그인 버튼 클릭
        driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()

        sleep(2)

        # 로그인 성공여부 확인 및 예외처리
        try:
            driver.find_element_by_xpath('//*[@id="menu"]/li[2]/a').click()

        except:
            driver.quit()

        # 시간표 로딩 시간 부여
        sleep(3)

        # 현재 페이지(시간표) html불러오기
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        day = ["월", "화", "수", "목", "금", ]

        for i in range(2, 7):
            value = soup.select_one(
                '#container > div > div.tablebody > table > tbody > tr > td:nth-child(%d) > div.cols' % (i))
            value = value.select('div')
            print(day[i - 2])
            for i in value:

                start = str(start2time(int(re.sub(r'[^0-9]', '', i['style'][14:]))))
                class_len = "0" + str(class_len2time(int(re.sub(r'[^0-9]', '', i['style'][0:13]))))
                start = pd.to_datetime(start, format='%H%M')
                class_len = pd.to_datetime(class_len, format='%I%M')

                end_hour = start.hour + class_len.hour
                end_minute = start.minute + class_len.minute
                if end_minute >= 60:
                    end_minute -= 60
                    end_hour += 1

                print("%d:%02d - %d:%02d" % (start.hour, start.minute, end_hour, end_minute))
        driver.close()
        driver.quit()
        print("성공")
        return render(request, "select.html")
    else:
        return render(request, 'login.html')

@csrf_exempt
def select(request):
    return render(request,"select.html")

@csrf_exempt
def signup(request):
    if 'check' in request.POST:
        # 로그인 url
        url = 'https://everytime.kr/login'
        print("1")
        options = webdriver.ChromeOptions()

        # 크롤러 실행 시 로그노출 안되도록 option 설정
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # 개발용-코드

        user_id = request.POST.get('etaid')  # 개인 아이디 입력
        print("2")
        user_pw = request.POST.get('etapw')  # 비밀번호 입력

        driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)

        driver.get(url)

        # id값으로 ID,Password 입력창을 찾아준 후 값 입력
        driver.find_element_by_xpath('//*[@id="container"]/form/p[1]/input').send_keys(user_id)

        sleep(1)

        driver.find_element_by_xpath('//*[@id="container"]/form/p[2]/input').send_keys(user_pw)
        print("3")
        sleep(2)

        # 로그인 버튼 클릭
        driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()

        # 로그인 성공여부 확인 및 예외처리
        try:
            driver.find_element_by_xpath('//*[@id="menu"]/li[2]/a').click()
            messages.error(request,'에브리타임 아이디와 비밀번호가 확인되었습니다!')
            print("4")
        except:
            driver.quit()
            #return 'err'
            messages.error(request, '에브리타임에 로그인 할 수 없습니다!')
            return render(request, "signup.html")

        driver.quit()
        print("5")
        messages.error(request, '정상적으로 회원가입이 되었습니다!')
        return redirect('/signup')

    else:
        return render(request,"signup.html")


@csrf_exempt
def check(request):
    return render(request,"check.html")

@csrf_exempt
def authentic(request):
    if request.method=="POST":
        print("check")
    else:
        print("NO")