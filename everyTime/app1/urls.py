from django.urls import path
from .import views
from .import crawl_views
urlpatterns=[
    path('',views.index),
    path('button/', views.button,name='button'),
    path('excelfile/', views.timetable_upload, name='excel'),
    path('login/', views.login,name='login'),
    path('crawl/',crawl_views.crawling,name='crawl'),
    path('select/', views.select, name='select'),
    path('signup/', views.signup, name='signup'),
    path('gongang/', views.gongang, name='gongang'),
    path('logout/', views.logout, name='logout'),
]