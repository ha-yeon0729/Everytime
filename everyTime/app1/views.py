import platform
from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from django.views.decorators.csrf import csrf_exempt
from time import sleep

#def f_login(request):
    #회원가입 db완성 후 로그인 시 id pw 받아와서 db랑 비교 후 일치 하면 다음 페이지로이동 아닐 시 예외 처리

def home(request):
    return render(request, 'login.html')
@csrf_exempt

#------------------------------------시간표 crawling 부분(selenium)-------------------------------------------------

def login(request): #추후 시간표 크롤링함수로 이름 변경
    if request.method == "POST":
        # 로그인 url
        url = 'https://everytime.kr/login'

        options = webdriver.ChromeOptions()

        # 크롤러 실행 시 로그노출 안되도록 option 설정
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        #개발용-코드
        if platform.system() == 'Windows':
            user_id = request.POST.get('userid')  # 개인 아이디 입력

            user_pw = request.POST.get('userpw')  # 비밀번호 입력

            driver = webdriver.Chrome('C:\chromedriver.exe', options=options)

            driver.get(url)

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
                return 'err'

            driver.quit()

            return render(request, "select.html")



def select(request):
    return render(request, "select.html")
