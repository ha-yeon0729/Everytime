import random
import re
import math
import pandas as pd
import openpyxl
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from selenium import webdriver
from django.views.decorators.csrf import csrf_exempt
from time import sleep
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import member
from django.http import HttpResponse


@csrf_exempt
def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        userid = request.POST["userid"]
        userpw = request.POST["userpw"]
        # 해당 userid,userpw와 일치하는 user객체를 가져온다.
        user = auth.authenticate(request, username=userid, password=userpw)

        # 해당 user 객체가 존재한다면
        if user is not None:
            request.session['Id'] = userid
            auth.login(request, user)  # 로그인한다
            print("로그인 성공")
            return redirect('select')

        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html화면으로 돌아감
            return render(request, 'login.html'), {'error': '로그인 정보가 잘못되었습니다!'}

    # 처음 이 페이지로 왔을 때
    else:
        return render(request, 'login.html')


# ------------------------------------시간표 crawling 부분(selenium)-------------------------------------------------
# 크롤링 시 서버에 봇이 아님을 인지 시키고 무리가 가지않도록 다음과 같은 방법 사용
# 1. User-Agent 설정  2.페이지가 전환 될 때 마다 sleep으로 쉬어주기
# 3. sleep은 random함수를 이용하여 쉬는 시간을 랜덤하게 해줌 4. 반복문 순환 시에도 sleep사용

def crawling(request):
    if request.method == "POST":

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

        # 로그인  url
        url = 'https://everytime.kr/login'
        options = webdriver.ChromeOptions()

        # 크롤러 실행 시 로그노출 안되도록 option 설정
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # UserAgent 설정
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        user_id = request.POST['userid']  # 개인 아이디 입력

        user_pw = request.POST['userpw']  # 비밀번호 입력

        driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)

        driver.get(url)
        # 창 크기 고정(px값 고정 위함)
        driver.set_window_size(1024, 630)

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

        # 시간표 로딩 시간 부여
        sleep(rand_value)

        # 현재 페이지(시간표) html불러오기
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        day = ["월", "화", "수", "목", "금", ]

        # ----------------------------사용자 시간표-------------------------------------
        print("나")

        print('')

        # 월~금 반복문 순회
        for i in range(2, 7):

            sleep(rand_value)

            value = soup.select_one(
                '#container > div > div.tablebody > table > tbody > tr > td:nth-child(%d) > div.cols' % (i))

            value = value.select('div')

            print(day[i - 2])

            # 요일 별 시간표 나타냄
            for i in value:
                # --------------top 과 height값 시간으로 변환--------------------
                top = int(re.sub(r'[^0-9]', '', i['style'][14:]))

                height = int(re.sub(r'[^0-9]', '', i['style'][0:13]))

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

        # ----------------------------친구 시간표-------------------------------------
        # 강의 시간, 이름 , 친구 수

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

            name = member.select_one('h3').text

            print('')

            print(name)

            print('')

            # 이름 클릭 후 시간표 페이지 진입
            driver.find_element_by_xpath('//*[@id="container"]/div[2]/a[%d]' % (num)).click()

            sleep(2)

            html = driver.page_source

            soup = BeautifulSoup(html, 'html.parser')

            # 월~금 반복문 순회
            for i in range(2, 7):

                sleep(rand_value)

                value = soup.select_one(
                    '#container > div > div.tablebody > table > tbody > tr > td:nth-child(%d) > div.cols' % (i))

                value = value.select('div')

                print(day[i - 2])

                # 요일 별 시간표 나타냄
                for i in value:

                    # --------------top 과 height값 시간으로 변환--------------------
                    top = int(re.sub(r'[^0-9]', '', i['style'][14:]))

                    height = int(re.sub(r'[^0-9]', '', i['style'][0:13]))

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

            sleep(rand_value)

            # 상단 친구 버튼 클릭
            driver.find_element_by_xpath('//*[@id="menu"]/li[5]/a').click()
        driver.close()
        driver.quit()
        print("성공")
        return render(request, "select.html")
    else:
        return render(request, 'login.html')


@csrf_exempt
def select(request):
    userid = request.session.get('Id')
    if userid:
        ID = member.objects.get(ssgId=userid)
        print(ID)

        # Id.ssgId 하면 member DB의 ssgId(FG 아이디) 가 나오고, Id.ssgPw하면 DB의 FG비번이 나온다.
        # 그냥 ID만 쓰면 제일 첫번째 값인 etaId가 나온다.
        return render(request, 'select.html', {'ID': ID.ssgId})

    return render(request, "select.html")


@csrf_exempt
def signup(request):
    # 입력한 아이디, 비번으로 진짜 에타에 접속이 되는지 확인 -하연
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
            messages.error(request, '에브리타임 아이디와 비밀번호가 확인되었습니다!')
            print("4")
            return render(request, 'signup.html', {'etaid': user_id, 'etapw': user_pw})

        except:
            driver.quit()
            # return 'err'
            messages.error(request, '유효한 에브리타임 정보가 아닙니다!')
            return render(request, "check.html")

        driver.quit()

    # 에타 인증 후 FG 사이트 아이디, 비번 설정
    elif 'signup' in request.POST:
        etaid = request.POST["etaid"]
        etapw = request.POST["etapw"]
        ssgid = request.POST["ssgid"]
        ssgpw = request.POST["ssgpw"]
        ressgpw = request.POST["ressgpw"]
        if (ssgpw == ressgpw):
            print("비번이랑 재입력 비번이랑 일치함!")
            messages.error(request, '정상적으로 회원가입이 되었습니다!')

            # 장고에서 제공하는 DB에 FD정보만 저장(로그인기능 편리함)
            user = User.objects.create_user(username=ssgid, password=ssgpw)
            # 내가 만든 DB(에타정보, FD정보 둘다 저장)
            DB = member(etaId=etaid, etaPw=etapw, ssgId=ssgid, ssgPw=ssgpw)
            DB.save()

            auth.login(request, user)
            return redirect('/')

        else:
            messages.error(request, '비밀번호가 다릅니다!')
            return render(request, "signup.html")

    else:  # 맨 처음에 이 페이지로 들어올 때 -하연
        return render(request, "check.html")


@csrf_exempt
def authentic(request):
    if request.method == "POST":
        print("check")
    else:
        print("NO")


def timetable_upload(request):
    def class_array(class_day, class_time):
        if class_day == '월':
            mon.append(class_time)
        if class_day == '화':
            tue.append(class_time)
        if class_day == '수':
            wed.append(class_time)
        if class_day == '목':
            thur.append(class_time)
        if class_day == '금':
            fri.append(class_time)

    excel = request.FILES['excel']

    if excel.name[-4:] != 'xlsx':
        print('err')
        return redirect('/login/')

    wb = openpyxl.load_workbook(excel)
    ws = wb.active
    # 불필요한 행 삭제
    ws.delete_rows(1, 3)
    ws.delete_cols(1, 11)

    ws.delete_cols(2)

    df = pd.DataFrame(ws.values)

    # 엑셀 값에서 value값만 저장
    class_list = list(df[0])

    # 강의 시간이 없는 부분 삭제
    class_list = list(filter(None, class_list))

    mon = []
    tue = []
    wed = []
    thur = []
    fri = []

    for i in class_list:
        tmp = i.index('(')

        class_ = i[0:tmp]

        class_time = class_[-11:]

        class_day = class_[0:-11]

        for i in class_day:
            class_array(i, class_time)

    print(mon)
    print(tue)
    print(wed)
    print(thur)
    print(fri)

    return redirect('/login/')
