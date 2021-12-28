import urllib.request
from urllib import parse
from bs4 import BeautifulSoup
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from time import sleep

@csrf_exempt
def contest_wevity(request):
    if request.method=="POST":
        flag = 0
        #공모전 정보들을 배열로 저장(request 날릴 때 한번에 하기 위함.)-하연
        List=[[]]
        cnt=0
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
            except:
                first_prize = ' '
            # 기간이 지난 경우 출력X
            if D_day[1] == '+':
                continue
            else:
                flag+=1
            #print(name)
            #print(date[12:35])
            #print(first_prize[13:].strip())
            #print("자세한 내용: " + contest_link)
            #print("---------------------------------------------------")
            List[cnt].append(name)
            List[cnt].append(date)
            List[cnt].append(first_prize)
            List[cnt].append(contest_link)

            print(List)
            print(List[cnt])
            # 한 바퀴 돌때마다 추가-하연
            List.append([])
            print(List)
            cnt+=1
            print(cnt)

        if flag == 0:
            print('가능한 공모전이 없습니다.')
            messages.warning(request,"가능한 공모전이 없습니다!")
            return render(request, "contest.html")

        return render(request, "contest.html", {'List': List})
    else:
        return render(request, "contest.html")


def contest_thinkyou(request):
    if request.method=="POST":
        flag = 0

        # 공모전 정보들을 배열로 저장(request 날릴 때 한번에 하기 위함.)-하연
        List = [[]]
        cnt = 0
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

                flag += 1

        print(name)
        print(date)
        print(contest_link)
        List[cnt].append(name)
        List[cnt].append(date)
        List[cnt].append(contest_link)

        print(List)
        print(List[cnt])
        # 한 바퀴 돌때마다 추가-하연
        List.append([])
        cnt += 1

        if flag == 0:
            messages.warning(request, "가능한 공모전이 없습니다.")
            return render(request, "contest.html")
        return render(request, "contest.html", {'List': List})
    else:
        return render(request, "contest.html")