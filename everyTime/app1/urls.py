from django.urls import path
from .import views

urlpatterns=[
    path('',views.index),
    path('login/', views.login),
    path('select/', views.select, name='select'),
    path('signup/', views.signup, name='signup'),
]