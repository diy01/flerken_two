from django.urls import path

from equipment import apis

urlpatterns = [
    # path(r'^$', apis.selectdata.as_view(), name="api_select"),
    path('', apis.LicenseList.as_view(), name="views_select"),

]
