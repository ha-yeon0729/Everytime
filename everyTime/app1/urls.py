from django.urls import path
from .import views, contest_views
from .import crawl_views
from .import gongang_views

urlpatterns=[
    path('',views.index),
    path('button/', views.button,name='button'),
    path('excelfile/', views.timetable_upload, name='excel'),
    path('login/', views.login,name='login'),
    path('crawl/',crawl_views.crawling,name='crawl'),
    path('select/', views.select, name='select'),
    path('signup/', views.signup, name='signup'),
    path('findpw/',views.findpw,name='findpw'),
    path('gongang/', gongang_views.gongang, name='gongang'),
    path('logout/', views.logout, name='logout'),
    path('contest/', contest_views.contest, name='contest'),
    path('contest/wevity/', contest_views.wevity, name='wevity'),
    path('contest/thinkyou/', contest_views.thinkyou, name='thinkyou'),
    path('contest/spectory/', contest_views.spectory, name='spectory'),
]