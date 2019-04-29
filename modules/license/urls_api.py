#!/usr/bin/env python 
from django.urls import path, re_path
from ..models import apis

urlpatterns = [

    path('license/', apis.LicenseList.as_view(), name='api_license'),
    re_path(r'license/(?P<pk>[0-9]+)/$', apis.LicenseDetail.as_view()),

    ]