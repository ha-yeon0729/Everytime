# 대외활동 찾기(1)

import urllib.request
from urllib import parse
from bs4 import BeautifulSoup

def contest(request):
    # 검색할 키워드 입력
    search = input('검색어를 입력하세요: ')

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

        # 기간
        date = soup.select_one(
            "#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li.dday-area").text

        # 남은 일수(기한 지났는지 확인 용)
        D_day = soup.select_one(
            "#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li.dday-area > span.cil-dday").text

        # 대회 홈페이지 링크
        contest_link = soup.select_one(
            "#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li:nth-child(8) > a")[
            "href"]

        # 1등 상금
        first_prize = soup.select_one(
            "#container > div.content-area > div.content-wrap > div.content > div > div.cd-area > div.info > ul > li:nth-child(7)").text

        # 기간이 지난 경우 출력X
        if D_day[1] == '+':
            continue

        print(name)
        print(date[12:35])
        print(first_prize[13:].strip())
        print("자세한 내용: " + contest_link)
        print("---------------------------------------------------")
