#!/usr/bin/env python 
from django.conf.urls import url
from ..license import views

urlpatterns = [

    url(r'^license/$', views.LicensePageView.as_view(), name='view_license'),

]
