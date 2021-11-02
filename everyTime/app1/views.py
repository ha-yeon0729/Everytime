from django.shortcuts import render
from bs4 import BeautifulSoup
import requests as req
from django.views.decorators.csrf import csrf_exempt
from fake_useragent import UserAgent
from time import sleep

@csrf_exempt
def login(request):
    if request.method == "POST":
        # 로그인 정보(개발자 도구)
        login_info = {
            'userid': request.POST['userid'],  # 개인 아이디 입력
            'password': request.POST['userpw'],  # 비밀번호 입력
            'redirect': '/'
        }

        # 헤더 정보
        headers = {
            'User-agent': UserAgent().chrome,
            'Referer': 'https://everytime.kr/'
        }

        # 로그인 URL
        baseUrl = 'https://everytime.kr/user/login'

        with req.session() as s:
            # Request(로그인 시도)
            res = s.post(baseUrl, login_info, headers=headers)
            sleep(3)

            # 로그인 시도 실패시 예외
            if res.status_code != 200:
                raise Exception("Login failed.")

            # 로그인 성공 후 세션 정보를 가지고 페이지 이동
            res = s.get('https://everytime.kr/', headers=headers)
            sleep(3)

            # 페이지 이동 후 수신 데이터 확인
            # print(res.text)

            # bs4 초기화
            soup = BeautifulSoup(res.text, "html.parser")
            sleep(2)
        try:
            # 로그인 성공 여부 체크
            name = soup.find('p', class_='school').string
            print('success')  ##성공시 success출력
        except:
            print('try again')  # 실패 시 try again출력

    return render(request, "login.html")

def select(request):
    return render(request,"select.html")

def signup(request):
    return render(request,"signup.html")