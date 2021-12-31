import re
import pandas as pd
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from selenium import webdriver
from django.views.decorators.csrf import csrf_exempt
from time import sleep
import random
import math
from .models import friend
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def crawling(request):
    # 계산 시 사용할 상수
    const = 0.8333333333333333333

    # top값을 시간으로 계산
    def start2time(top):
        minute = 0
        while True:
            minute += 1
            if math.floor(const * minute) == top:
                if minute % 5 == 0:
                    break

        f_hour = int(minute / 60) * 100

        f_minute = int(minute % 60)

        f_value = f_hour + f_minute

        return f_value

    # height값을 시간으로 계산
    def class_len2time(height):

        minute = 0

        while True:

            minute += 1

            tmp = const * minute
            # 반올림 중 사사오입을 무시하기 위해 끝이 0.5일경우 0.1을 더해주어 올림을 하도록 해줌
            if (tmp - math.floor(tmp)) == 0.5:
                tmp += 0.1

            if (height - 1) == round(tmp):

                if minute % 5 == 0:
                    break
        f_hour = int(minute / 60) * 100
        f_minute = int(minute % 60)

        if f_hour == 0:
            f_value = str(f_minute)
            return f_value

        f_value = f_hour + f_minute
        return str(f_value)

    # 친구 추가 될떄마다 2차원 배열 추가
    def add_friend(user_time_table):
        line = []
        user_time_table.append(line)

    # 2차원 배열안에 1차원 배열 추가해줌(월~금)
    def add_day(user_time_table, user_cnt):
        line = []

        user_time_table[user_cnt].append(line)

    # 로그인 url
    url = 'https://everytime.kr/login'

    options = webdriver.ChromeOptions()

    user_id = request.session['ETAID']

    user_pw = request.session['ETAPW']


    # 크롤러 실행 시 로그노출 안되도록 option 설정
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # UserAgent 설정
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)

    # 창 크기 고정(px값 고정 위함)
    driver.set_window_size(1024, 630)

    driver.get(url)

    # sleep에 사용 할 랜덤 값
    rand_value = random.uniform(2, 4)

    sleep(rand_value)

    # id값으로 ID,Password 입력창을 찾아준 후 값 입력
    driver.find_element_by_xpath('//*[@id="container"]/form/p[1]/input').send_keys(user_id)

    driver.find_element_by_xpath('//*[@id="container"]/form/p[2]/input').send_keys(user_pw)

    sleep(rand_value)

    # 로그인 버튼 클릭
    driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()

    sleep(rand_value)

    # 로그인 성공여부 확인 및 예외처리
    try:
        driver.find_element_by_xpath('//*[@id="menu"]/li[2]/a').click()

    except:
        driver.quit()
        return 'err'


    # ********************DB에 사용 될 변수(배열)*******************************
    user_name = ['사용자']  # 사용자 및 친구 이름 담을 배열

    user_cnt = 0

    user_time_table = [[]]

    # **************************************************************************

    # 시간표 로딩 시간 부여
    sleep(rand_value)

    # 현재 페이지(시간표) html불러오기
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    day = ["mon", "tue", "wed", "thu", "fri", ]

    # ----------------------------사용자 시간표-------------------------------------
    print("사용자")

    print('')

    # 월~금 반복문 순회
    for i in range(2, 7):

        sleep(rand_value)

        value = soup.select_one('#container > div > div.tablebody > table > tbody > tr > td:nth-child(%d) > div.cols' % (i))

        value = value.select('div')

        print(day[i - 2])

        # 반복문 순회할때 마다 2차원 배열 속에 1차원 배열 추가(1차원 배열은 각각 월~금 역할)
        add_day(user_time_table, user_cnt)

        # 요일 별 시간표 나타냄
        for j in value:
            # --------------top 과 height값 시간으로 변환--------------------
            top = int(re.sub(r'[^0-9]', '', j['style'][14:]))

            height = int(re.sub(r'[^0-9]', '', j['style'][0:13]))

            start = str(start2time(top))

            start = pd.to_datetime(start, format='%H%M')

            if height < 51:
                class_len = class_len2time(height)
                class_len = pd.to_datetime(class_len, format='%M')

            else:
                class_len = "0" + class_len2time(height)
                class_len = pd.to_datetime(class_len, format='%I%M')
    # ---------------------------------------------------------------
            # 강의 끝나는 시간 계산
            end_hour = start.hour + class_len.hour

            end_minute = start.minute + class_len.minute

            if end_minute >= 60:
                end_minute -= 60

                end_hour += 1

            print("%d:%02d - %d:%02d" % (start.hour, start.minute, end_hour, end_minute))

            # 구한 시간들을 문자로 변환하여 하나의 문장으로 합치는 작업
            start_hour = str(start.hour)
            start_minute = str(start.minute)
            end_hour = str(end_hour)
            end_minute = str(end_minute)

            if int(start_minute) < 10:
                start_minute = "0" + start_minute

            if int(end_minute) < 10:
                end_minute = "0" + end_minute

            f_val = str(start_hour) + str(start_minute) + '-' + str(end_hour) + str(end_minute)

            # 사용자(본인)의 요일별 시간 배열에 저장
            user_time_table[user_cnt][i - 2].append(f_val)

    #하연추가
    mon=user_time_table[user_cnt][0]
    tue=user_time_table[user_cnt][1]
    wed=user_time_table[user_cnt][2]
    thu=user_time_table[user_cnt][3]
    fri=user_time_table[user_cnt][4]

    DB = friend(my_name=request.session['name'], friend_name=user_name, mon=mon,tue=tue,wed=wed,thu=thu,fri=fri)
    DB.save()
    # ----------------------------친구 시간표-------------------------------------

    # 상단 친구 버튼 클릭
    driver.find_element_by_xpath('//*[@id="menu"]/li[5]/a').click()

    sleep(rand_value)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    # 친구 리스트 가져옴
    soup = soup.select('#container > div.friendlist>a.friend')

    num = 0

    for member in soup:

        sleep(rand_value)

        num += 1

        # 인원 1 증가 시켜줌
        user_cnt += 1

        # 배열에 새로운 2차원 배열 추가해줌(친구의 시간을 담기 위함)
        add_friend(user_time_table)

        friend_name = member.select_one('h3').text

        user_name.append(friend_name)

        print('')

        print(friend_name)

        print('')

        # 이름 클릭 후 시간표 페이지 진입
        driver.find_element_by_xpath('//*[@id="container"]/div[2]/a[%d]' % (num)).click()

        sleep(1)

        #가장 최근 학기 선택
        driver.find_element_by_xpath('//*[@id="container"]/aside/div[2]/ol/li[1]/a').click()

        sleep(rand_value)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        # 월~금 반복문 순회
        for i in range(2, 7):

            sleep(rand_value)

            value = soup.select_one(
                '#container > div > div.tablebody > table > tbody > tr > td:nth-child(%d) > div.cols' % (i))

            value = value.select('div')

            print(day[i - 2])

            # 반복문 순회할때 마다 2차원 배열 속에 1차원 배열 추가(1차원 배열은 각각 월~금 역할)
            add_day(user_time_table, user_cnt)

            # 요일 별 시간표 나타냄
            for j in value:

                # --------------top 과 height값 시간으로 변환--------------------
                top = int(re.sub(r'[^0-9]', '', j['style'][14:]))

                height = int(re.sub(r'[^0-9]', '', j['style'][0:13]))

                start = str(start2time(top))

                start = pd.to_datetime(start, format='%H%M')

                if height < 51:
                    class_len = class_len2time(height)
                    class_len = pd.to_datetime(class_len, format='%M')

                else:
                    class_len = "0" + class_len2time(height)
                    class_len = pd.to_datetime(class_len, format='%I%M')
                # ---------------------------------------------------------------
                # 강의 끝나는 시간 계산
                end_hour = start.hour + class_len.hour

                end_minute = start.minute + class_len.minute

                if end_minute >= 60:
                    end_minute -= 60

                    end_hour += 1

                print("%d:%02d - %d:%02d" % (start.hour, start.minute, end_hour, end_minute))

                # 구한 시간들을 문자로 변환하여 하나의 문장으로 합치는 작업
                start_hour = str(start.hour)
                start_minute = str(start.minute)
                end_hour = str(end_hour)
                end_minute = str(end_minute)

                if int(start_minute) < 10:
                    start_minute = "0" + start_minute

                if int(end_minute) < 10:
                    end_minute = "0" + end_minute

                f_val = str(start_hour) + str(start_minute) + '-' + str(end_hour) + str(end_minute)

                # 사용자(본인)의 요일별 시간 배열에 저장
                user_time_table[user_cnt][i - 2].append(f_val)

        # 하연추가
        mon = user_time_table[user_cnt][0]
        tue = user_time_table[user_cnt][1]
        wed = user_time_table[user_cnt][2]
        thu = user_time_table[user_cnt][3]
        fri = user_time_table[user_cnt][4]

        DB = friend(my_name=request.session['name'], friend_name=friend_name, mon=mon, tue=tue, wed=wed, thu=thu, fri=fri)
        DB.save()

        sleep(rand_value)

        # 상단 친구 버튼 클릭
        driver.find_element_by_xpath('//*[@id="menu"]/li[5]/a').click()

    driver.quit()

    user_cnt += 1

    return render(request, "select.html")