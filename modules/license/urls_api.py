#!/usr/bin/env python 
from django.urls import path, re_path
from modules.license import views_api


urlpatterns = [

    path('license/', views_api.LicenseList.as_view(), name='api_license'),
    re_path(r'license/(?P<pk>[0-9]+)/$', views_api.LicenseDetail.as_view()),

    ]