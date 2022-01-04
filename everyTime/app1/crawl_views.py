import rsa,re
import pandas as pd
from bs4 import BeautifulSoup
from django.contrib import messages
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
    if request.session['name']:
        print(request.session['name'])
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
        from .models import member
        user = member.objects.get(etaId=user_id)
        user_pw=user.etaPw

        # 크롤러 실행 시 로그노출 안되도록 option 설정
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # UserAgent 설정
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)

        # 창 크기 고정(p
        # x값 고정 위함)
        driver.set_window_size(1024, 630)
        driver.get(url)

        # sleep에 사용 할 랜덤 값
        rand_value = random.uniform(2, 4)
        print(3)
        sleep(rand_value)

        # id값으로 ID,Password 입력창을 찾아준 후 값 입력
        driver.find_element_by_xpath('//*[@id="container"]/form/p[1]/input').send_keys(user_id)

        driver.find_element_by_xpath('//*[@id="container"]/form/p[2]/input').send_keys(user_pw)
        print(4)
        sleep(rand_value)
        print(5)
        # 로그인 버튼 클릭
        driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()
        print(6)
        sleep(rand_value)
        print(7)
        # 로그인 성공여부 확인 및 예외처리
        try:
            print(8)
            driver.find_element_by_xpath('//*[@id="menu"]/li[2]/a').click()

        except:
            print(9)
            driver.quit()
            return 'err'

        print(10)
        # ********************DB에 사용 될 변수(배열)*******************************
        user_name = []  # 사용자 및 친구 이름 담을 배열

        user_cnt = 0

        user_time_table = [[]]

        # **************************************************************************

        # 시간표 로딩 시간 부여
        sleep(rand_value)

        # 현재 페이지(시간표) html불러오기
        html = driver.page_source
        print(11)
        soup = BeautifulSoup(html, 'html.parser')

        day = ["mon", "tue", "wed", "thu", "fri", ]

        # ----------------------------사용자 시간표-------------------------------------
        # 이미 사용자 시간을 크롤링하여 DB에 저장했다면 바로 친구 시간표 크롤링으로 건너뛰기
        try:
            user=friend.objects.get(friend_name=request.session['name'])

        # 사용자 시간이 존재하지 않는다면 except문 실행
        except:
            user_name=request.session['name']
            print(request.session['name'])

            print('')
            print(12)
            # 월~금 반복문 순회
            for i in range(2, 7):

                sleep(rand_value)

                value = soup.select_one('#container > div > div.tablebody > table > tbody > tr > td:nth-child(%d) > div.cols' % (i))

                value = value.select('div')

                print(day[i - 2])

                # 반복문 순회할때 마다 2차원 배열 속에 1차원 배열 추가(1차원 배열은 각각 월~금 역할)
                if i is not 7:      # 하연 추가
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
            print(10)
            #하연추가
            mon=user_time_table[user_cnt][0]
            tue=user_time_table[user_cnt][1]
            wed=user_time_table[user_cnt][2]
            thu=user_time_table[user_cnt][3]
            fri=user_time_table[user_cnt][4]

            DB = friend(my_name=request.session['name'], friend_name=user_name, mon=mon,tue=tue,wed=wed,thu=thu,fri=fri)
            DB.save()

        # 사용자 크롤링 여부에 상관없이 친구 시간표 일단 체크하기(finally문)
        finally:
            # ----------------------------친구 시간표-------------------------------------
            print("a")
            # 상단 친구 버튼 클릭
            driver.find_element_by_xpath('//*[@id="menu"]/li[5]/a').click()

            sleep(rand_value)

            html = driver.page_source

            soup = BeautifulSoup(html, 'html.parser')
            print("b")
            # 친구 리스트 가져옴
            soup = soup.select('#container > div.friendlist>a.friend')

            num = 0
            for member in soup:
                # 이미 크롤링된 친구라면 제외하기 위해서 친구 이름이 DB에 있는지 먼저 체크한다.
                friend_name = member.select_one('h3').text
                print(friend_name)

                try:
                    print("c")
                    exist=friend.objects.get(friend_name=friend_name) # DB에 있는지 확인하는 코드. 있다면 다시 for문으로 돌아가고 없다면 except로 간다.
                    print("이미 존재")
                    continue

                except:
                    sleep(rand_value)

                    num += 1

                    # 인원 1 증가 시켜줌
                    user_cnt += 1

                    # 배열에 새로운 2차원 배열 추가해줌(친구의 시간을 담기 위함)
                    add_friend(user_time_table)
                    print("d")
                    #friend_name = member.select_one('h3').text

                    user_name.append(friend_name)

                    print('')

                    print(friend_name)

                    print('')

                    # 이름 클릭 후 시간표 페이지 진입
                    driver.find_element_by_xpath('//*[@id="container"]/div[2]/a[%d]' % (num)).click()

                    sleep(1)

                    # 가장 최근 학기 선택
                    driver.find_element_by_xpath('//*[@id="container"]/aside/div[2]/ol/li[1]/a').click()

                    sleep(rand_value)
                    html = driver.page_source

                    soup = BeautifulSoup(html, 'html.parser')
                    print("e")
                    # 월~금 반복문 순회
                    for i in range(2, 7):
                        print("f")
                        sleep(rand_value)
                        print("g")
                        value = soup.select_one(
                            '#container > div > div.tablebody > table > tbody > tr > td:nth-child(%d) > div.cols' % (i)
                        )
                        print("h")
                        value = value.select('div')

                        print(day[i - 2])
                        print("i")
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

            messages.error(request, '에브리타임에서 시간표를 자동으로 불러왔습니다!')
            return render(request, "button.html")
    else:
        messages.error(request, '로그인을 해주세요!')
        return render(request, "login.html")