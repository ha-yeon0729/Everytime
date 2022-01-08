import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import friend
import ast

# 한글 폰트 사용을 위해서 세팅(그래프에서 한글 깨짐을 방지)
from matplotlib import font_manager, rc
from django.contrib import messages

@csrf_exempt
def gongang(request):
    if request.user.is_authenticated and request.method == 'POST':
        #폰트 경로
        font_path = "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf"
        #폰트 적용
        font = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font)

        # 강의 늦게 끝나는 순서로 정렬해주는 함수
        def arrange_day_class(day):
            for i in range(len(day) - 1):
                for j in range(i + 1, len(day)):
                    if int(day[i][-4:]) < int(day[j][-4:]):
                        day[i], day[j] = day[j], day[i]

        # 강의 시작시간 종료시간 분리하는 함수
        def sep_classtime(day, start, end):
            for i in day:
                start.append(int(i[0:-5]))
                end.append(int(i[-4:]))

        # 강의시간에 해당하는 부분의 그래프 색상을 하얀색으로 변경
        def make_blank(x, start, prev_start, end, next_end):
            plt.bar(x, end, color='w')

            # 막대그래프의 값을 텍스트로 나타내주는 부분
            if prev_start > end:
                hour = str(int(end / 100))
                minute = str(end % 100)
                if minute == '0':
                    minute = '00'

                plt.text(x, end, hour + ':' + minute,
                         fontsize=6,
                         color='black',
                         horizontalalignment='center',
                         verticalalignment='bottom')

            plt.bar(x, start, color='lightslategrey')

            # 막대그래프의 값을 텍스트로 나타내주는 부분
            if start > next_end:
                hour = str(int(start / 100))
                minute = str(start % 100)
                if minute == '0':
                    minute = '00'

                plt.text(x, start, hour + ':' + minute,
                         fontsize=6,
                         color='black',
                         horizontalalignment='center',
                         verticalalignment='bottom')

        ##########################matplotlib관련 부분#######################
        ax = plt.axes()

        x = np.arange(5)

        # x축에 들어갈 내용
        years = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

        # 월~금에 기본적으로 생성할 막대의 크기
        values = [2200, 2200, 2200, 2200, 2200]

        # 라벨 가시화(색깔에 따른 의미 알려주기 위함)
        plt.bar(x, values, color='w', label='강의시간')

        plt.legend(fontsize=6,loc="upper right", bbox_to_anchor=(1.138, 1), facecolor='lavender')

        plt.bar(x, values, color='lightslategrey', label='공강시간')

        plt.legend(fontsize=6,loc="upper right", bbox_to_anchor=(1.138, 1), facecolor='lavender')


        # x축 생성
        plt.xticks(x, years)

        # y축 눈금 표시 범위
        plt.ylim([2200, 900])
        # y축 눈금 단위 지정
        plt.yticks([900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200],
                   ('9시', '10시', '11시', '12시', '13시', '14시', '15시', '16시', '17시', '18시', '19시', '20시', '21시', '22시'))

        #####################################################################

        # 선택된 친구의 시간을 요일별로 합쳐줄 배열
        mon=[]
        tue =[]
        wed =[]
        thu =[]
        fri =[]

        # 요일별 시작시간 끝나는 시간 담을 배열
        start_mon = []
        end_mon = []

        start_tue = []
        end_tue = []

        start_wed = []
        end_wed = []

        start_thu = []
        end_thu = []

        start_fri = []
        end_fri = []
        # 체크한 친구목록 불러오기
        try:
            selected = request.POST.getlist('selected')
            # 수,목,금을 의미하는 것이  wed, thu, fri가 아닐경우 수정 부탁드립니다!
            for i in selected:
                selectDB = friend.objects.filter(friend_name=i)
                for j in selectDB:
                    # 요일별 배열에 선택된 사용자의 요일별 배열의 원소들 넣어준다
                    mon.extend(ast.literal_eval(j.mon))
                    tue.extend(ast.literal_eval(j.tue))
                    wed.extend(ast.literal_eval(j.wed))
                    thu.extend(ast.literal_eval(j.thu))
                    fri.extend(ast.literal_eval(j.fri))

            # 요일별 배열 정렬
            arrange_day_class(mon)
            arrange_day_class(tue)
            arrange_day_class(wed)
            arrange_day_class(thu)
            arrange_day_class(fri)

            # 강의 시간 분리
            sep_classtime(mon, start_mon, end_mon)
            sep_classtime(tue, start_tue, end_tue)
            sep_classtime(wed, start_wed, end_wed)
            sep_classtime(thu, start_thu, end_thu)
            sep_classtime(fri, start_fri, end_fri)

            ### 공강시간-> 막대그래프  생성 파트
            print("mon!")
            print(start_mon, end_mon)
            print("tue!")
            print(start_tue, end_tue)
            print("wed!")
            print(start_wed, end_wed)
            print("thu!")
            print(start_thu, end_thu)
            print("fri!")
            print(start_fri, end_fri)

            # 월
            index = 0
            for s, e in zip(start_mon, end_mon):
                prev_start_index = index - 1

                prev_start = start_mon[prev_start_index]

                next_end_index = index + 1

                if prev_start_index < 0:
                    prev_start = 100000

                if next_end_index < len(end_mon):
                    next_end = end_mon[next_end_index]
                else:
                    next_end = 0


                make_blank(x[0], s, prev_start, e, next_end)

                index += 1

            # 화
            index = 0
            for s, e in zip(start_tue, end_tue):
                prev_start_index = index - 1

                prev_start = start_tue[prev_start_index]

                next_end_index = index + 1

                if prev_start_index < 0:
                    prev_start = 100000

                if next_end_index < len(end_tue):
                    next_end = end_tue[next_end_index]
                else:
                    next_end = 0

                make_blank(x[1], s, prev_start, e, next_end)

                index += 1

            # 수
            index = 0
            for s, e in zip(start_wed, end_wed):
                prev_start_index = index - 1

                prev_start = start_wed[prev_start_index]

                next_end_index = index + 1

                if prev_start_index < 0:
                    prev_start = 2400

                if next_end_index < len(end_wed):
                    next_end = end_wed[next_end_index]
                else:
                    next_end = 0

                make_blank(x[2], s, prev_start, e, next_end)

                index += 1

            # 목
            index = 0
            for s, e in zip(start_thu, end_thu):
                prev_start_index = index - 1

                prev_start = start_thu[prev_start_index]

                next_end_index = index + 1

                if prev_start_index < 0:
                    prev_start = 2400

                if next_end_index < len(end_thu):
                    next_end = end_thu[next_end_index]
                else:
                    next_end = 0

                make_blank(x[3], s, prev_start, e, next_end)

                index += 1

            # 금
            index = 0
            for s, e in zip(start_fri, end_fri):
                prev_start_index = index - 1

                prev_start = start_fri[prev_start_index]

                next_end_index = index + 1

                if prev_start_index < 0:
                    prev_start = 2400

                if next_end_index < len(end_fri):
                    next_end = end_fri[next_end_index]
                else:
                    next_end = 0

                make_blank(x[4], s, prev_start, e, next_end)

                index += 1

            # 생성된 그래프 imgae file로 저장(출력위함)
            plt.savefig('/home/hayeon/Everytime/everyTime/static/example.png', facecolor='#eeeeee', dpi=140, pad_inches=0.3)  # 예시) 'C:/example.png' )
            return render(request,"gongang.html",{'select':selected})
        except:
            messages.warning(request,"오류가 발생했습니다! 친구를 1명 이상 선택해주세요")
            return render(request,"select.html")
    return render(request, "fail.html")
#####################출력하는법########################
# 이후 그래프를 출력할 템플릿 html에
# <img src="{% static 'graph/example.png' %}" alt="공강시간 막대그래프">
# 상단 코드 추가하여 출력에 주면 된다.