from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('select/', views.select, name='select'),
    path('signup/', views.signup, name='signup'),
    path('timetable_upload/', views.timetable_upload),
]
