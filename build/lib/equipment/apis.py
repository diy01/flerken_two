# coding=utf-8
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from equipment.serializers import *
from utils.base import BaseListCreateAPIView


# class selectdata():
#    filter_backends = (filters.SearchFilter)
#    search_fields = ("devicename",)
# if request.method == 'GET':
#     devicename = request.GET.get('devicename', '')  # 得到搜索关键词'django'
#     print  devicename
#     course_list = Device.objects.filter(devicename=devicename)
#     print  course_list
#     return course_list
# return render({'devicename': course_list},'index.html')

class LicenseList(BaseListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = LicenseSerializer
    search_fields = ('devicename',)
    filter_backends = (DjangoFilterBackend, SearchFilter)
