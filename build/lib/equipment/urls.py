# coding=utf-8
from django.urls import path

from equipment import views

urlpatterns = [

    path('', views.LihuiPage.as_view()),

]
