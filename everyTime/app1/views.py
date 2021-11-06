import re
import pandas as pd
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

#def f_login(request):
    #회원가입 db완성 후 로그인 시 id pw 받아와서 db랑 비교 후 일치 하면 다음 페이지로이동 아닐 시 예외 처리

@csrf_exempt
#------------------------------------시간표 crawling 부분(selenium)-------------------------------------------------

def index(request):
    return render(request,"index.html")

def login(request):
    if request.method=="POST":
        userid=request.POST["userid"]
        userpw=request.POST["userpw"]
        #해당 userid,userpw와 일치하는 user객체를 가져온다.
        user=auth.authenticate(request,username=userid,password=userpw)

        #해당 user 객체가 존재한다면
        if user is not None:
            request.session['Id']=userid
            auth.login(request,user)    #로그인한다
            print("로그인 성공")
            return redirect('select')

        #존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html화면으로 돌아감
            return render(request,'login.html'),{'error':'로그인 정보가 잘못되었습니다!'}

    # 처음 이 페이지로 왔을 때
    else:
        return render(request,'login.html')


def crawling(request): #추후 시간표 크롤링함수로 이름 변경
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
    userid=request.session.get('Id')
    if userid:
        ID=member.objects.get(ssgId=userid)
        print(ID)

        #Id.ssgId 하면 member DB의 ssgId(FG 아이디) 가 나오고, Id.ssgPw하면 DB의 FG비번이 나온다.
        #그냥 ID만 쓰면 제일 첫번째 값인 etaId가 나온다.
        return render(request,'select.html',{'ID':ID.ssgId})

    return render(request,"select.html")


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
            messages.error(request,'에브리타임 아이디와 비밀번호가 확인되었습니다!')
            print("4")
            return render(request,'signup.html',{'etaid': user_id,'etapw':user_pw})

        except:
            driver.quit()
            #return 'err'
            messages.error(request, '유효한 에브리타임 정보가 아닙니다!')
            return render(request, "check.html")
        driver.quit()

    # 에타 인증 후 FG 사이트 아이디, 비번 설정
    elif 'signup' in request.POST:
        etaid=request.POST["etaid"]
        etapw=request.POST["etapw"]
        ssgid = request.POST["ssgid"]
        ssgpw = request.POST["ssgpw"]
        ressgpw = request.POST["ressgpw"]
        if (ssgpw == ressgpw):
            print("비번이랑 재입력 비번이랑 일치함!")
            messages.error(request, '정상적으로 회원가입이 되었습니다!')

            #장고에서 제공하는 DB에 FD정보만 저장(로그인기능 편리함)
            user=User.objects.create_user(username=ssgid,password=ssgpw)
            #내가 만든 DB(에타정보, FD정보 둘다 저장)
            DB=member(etaId=etaid,etaPw=etapw,ssgId=ssgid,ssgPw=ssgpw)
            DB.save()

            auth.login(request,user)
            return redirect('/')

        else:
            messages.error(request, '비밀번호가 다릅니다!')
            return render(request, "signup.html")

    else:  # 맨 처음에 이 페이지로 들어올 때 -하연
        return render(request,"check.html")


@csrf_exempt
def authentic(request):
    if request.method=="POST":
        print("check")
    else:
        print("NO")