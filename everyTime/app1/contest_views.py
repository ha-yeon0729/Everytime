import urllib.request
from bs4 import BeautifulSoup
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import urllib.request
from urllib import parse
import json
from datetime import datetime

#공모전 기본 페이지
@csrf_exempt
def contest(request):
    return render(request,"contest.html")

# 위비티 버튼을 클릭했다면
@csrf_exempt
def wevity(request):
    if request.method=="POST":
        flag = 0
        #공모전 정보들을 배열로 저장(request 날릴 때 한번에 하기 위함.)-하연
        List=[]
        cnt=-1
        # 검색할 키워드 입력
        #search = input('검색어를 입력하세요: ')

        #입력받은 키워드 전달하기-하연
        search=request.POST.get("search")

        # 사이트 주소
        url = "https://www.wevity.com/"

        # 검색한 결과 주소 찾기위한 주소
        search_url = 'https://www.wevity.com/?c=srh&s=1&sw='

        # 검색한 키워드와 주소 연결
        search_url2 = search_url + parse.quote(search)

        # 결과창에서 more에 해당하는 주소 가져옴
        source = urllib.request.urlopen(search_url2).read()

        soup = BeautifulSoup(source, 'html.parser')

        more_link = \
        soup.select_one("#container > div.content-area > div.content-wrap > div.content > div > div:nth-child(2) > a")["href"]

        # 주소와 연결
        final_url = url + more_link

        source = urllib.request.urlopen(final_url).read()

        soup = BeautifulSoup(source, 'html.parser')

        # 기간 내 해당하는 대외활동 정보 가져온다.
        contest = soup.select("#container > div.content-area > div.content-wrap > div.content > div > ul > li")

        # 각각의 대회를 하나씩 훑는다.
        for i in contest:

            # 각 대회의 세부정보를 알기위해 해당 링크를 가져온다.
            link = url + i.select_one("div.tit > a")["href"]

            # 해당 페이지 정보 읽어온다.
            source = urllib.request.urlopen(link).read()

            soup = BeautifulSoup(source, 'html.parser')

            # 대회명
            name = soup.select_one(
                "#container > div.content-area > div.content-wrap > div.content > div > div.tit-area > h6").text

            if name[0:4] == '[삭제]':
                continue

            # 기간
            try:
                date = soup.select_one(
                    "#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li.dday-area").text
            except:
                date = ' '

            # 남은 일수(기한 지났는지 확인 용)
            D_day = soup.select_one(
                "#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li.dday-area > span.cil-dday").text
            try:
                # 대회 홈페이지 링크
                contest_link = soup.select_one(
                    "#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li:nth-child(8) > a")[
                    "href"]
            except:
                contest_link = ' '

            # 1등 상금
            try:
                first_prize = soup.select_one(
                    "#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li:nth-child(7)").text
                if first_prize=="\n1등 상금\n":
                    first_prize="없음"
            except:
                first_prize = ' '

            # 기간이 지난 경우 출력X
            if D_day[1] == '+':
                continue
            else:
                # 한 바퀴 돌때마다 추가-하연
                List.append([])
                cnt += 1
                flag+=1

            List[cnt].append(name)
            List[cnt].append(date)
            List[cnt].append(first_prize)
            List[cnt].append(contest_link)

        if flag == 0:
            messages.warning(request,"가능한 공모전이 없습니다!")
            return render(request, "wevity.html")

        return render(request, "wevity.html", {'List': List})
    return redirect('../')

# 씽유 버튼을 클릭했다면
@csrf_exempt
def thinkyou(request):
    if request.method=='POST':
        flag = 0

        # 공모전 정보들을 배열로 저장(request 날릴 때 한번에 하기 위함.)-하연
        List = []
        cnt = -1
        # 검색할 키워드 입력
        # search = input('검색어를 입력하세요: ')

        # 입력받은 키워드 전달하기-하연
        search = request.POST.get("search")

        # 사이트 주소
        url = "https://thinkyou.co.kr"

        # 검색한 결과 주소 찾기위한 주소
        search_url = 'https://thinkyou.co.kr/contest/search.asp?serstr='

        # 검색한 키워드와 주소 연결
        final_url = search_url + parse.quote(search)

        source = urllib.request.urlopen(final_url).read()

        soup = BeautifulSoup(source, 'html.parser')

        # 기간 내 해당하는 대외활동 정보 가져온다.
        contest = soup.select("#contents > div > div.result-group > dl")

        # 각각의 대회를 하나씩 훑는다.
        for i in contest:

            # 각 대회의 세부정보를 알기위해 해당 링크를 가져온다.
            link = url + i.select_one("dt > a")["href"]

            # 해당 페이지 정보 읽어온다.
            source = urllib.request.urlopen(link).read()

            soup = BeautifulSoup(source, 'html.parser')

            # 공모전 이름
            name = soup.select_one("#printArea > div.contest_view > dl > dt > h1").text

            # 마감 여부
            D_day = soup.select_one("#printArea > div.contest_view > dl > dt > span").text

            # 공모전 세부 정보
            contest_info = soup.select("#printArea > div.contest_view > div > div.rightArea > table > tbody>tr")

            for j in contest_info:
                # 정보의 종류
                kind = j.select_one("tr> th").text
                # 정보
                info = j.select_one("tr> td").text

                if kind == "접수기간":
                    # 접수 기간
                    date = info

                if kind == "홈페이지":
                    # 대회 홈페이지 링크
                    contest_link = j.select_one("tr>td>a")["href"]

            # 기간이 지난 경우 출력X
            if D_day == '마감':
                continue

            # 한 바퀴 돌때마다 추가-하연
            List.append([])
            cnt += 1
            flag += 1

            List[cnt].append(name)
            List[cnt].append(date)
            List[cnt].append(contest_link)

        if flag == 0:
            messages.warning(request, "가능한 공모전이 없습니다.")
            return render(request, "thinkyou.html")
        return render(request, "thinkyou.html", {'List': List})
    return redirect('../')

#스펙토리 버튼을 클릭했다면
@csrf_exempt
def spectory(request):
    if request.method=='POST':
        flag = 0
        # 공모전 정보들을 배열로 저장(request 날릴 때 한번에 하기 위함.)-하연
        List = []
        cnt = -1
        # 현재 날짜
        now = datetime.today()

        # 검색할 키워드 입력
        # search = input('검색어를 입력하세요: ')

        # 입력받은 키워드 전달하기-하연
        search = request.POST.get("search")

        # 대회 정보를 가지고 있는 api주소
        search_url = 'http://spectory.net/api/portal/contest?__n=1640420919237&siteType=%EA%B3%B5%EB%AA%A8%EC%A0%84&categoryPrefix=info-category&searchType=all&searchTxt='

        # 검색한 키워드와 주소 연결
        final_url = search_url + parse.quote(search) + '&page=1&rows=10'

        source = urllib.request.urlopen(final_url).read()

        # json데이터로 분리 후 key값이 data인 값만 추출
        contest = json.loads(source)['data']

        # 각각의 대회를 하나씩 훑는다.
        for i in contest:
            # json데이터 중 접수 마감기간의 정보를 가지고 있는 것의 key값이 'endDate'이다. 이 시간과 현재 날짜를 비교하여 접수기간이 유효한지를 판단
            end_date = datetime.strptime(i['endDate'], '%Y-%m-%d %H:%M')

            # 접수기간이 유효할 경우
            if now < end_date:

                # 한 바퀴 돌때마다 추가-하연
                List.append([])
                cnt += 1
                flag+=1

                date = i['startDate'][0:11] + '~ ' + i['endDate'][0:11]

                print(i['name'].strip())

                print('접수기간:', date.strip())

                print('-----------------------------------------------')

                List[cnt].append(i['name'].strip())
                List[cnt].append(date.strip())
        if flag == 0:
            messages.warning(request,"가능한 공모전이 없습니다!")
            return render(request, "spectory.html")

        return render(request, "spectory.html", {'List': List})

    return redirect('../')