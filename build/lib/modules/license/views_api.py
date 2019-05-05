#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from modules.license.serializers import *
from utils.base import BaseListCreateAPIView, BaseRetrieveUpdateDestroyAPIView


class LicenseList(BaseListCreateAPIView):
    """
    ###License管理表

    ###输入/输出参数

    * id                               —— pk
    * company                          —— 公司
    * email                            —— 邮箱
    * full_name                        —— 联系人姓名
    * nodes                            —— 节点数量
    * license_type                     —— License类型
    * hostname                         —— 主机名
    * start_date                       —— 生效时间
    * expiration_date                  —— 过期时间
    * ctime                            —— 创建时间
    * cuser                            —— 创建用户

    """

    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)


class LicenseDetail(BaseRetrieveUpdateDestroyAPIView):
    """
    ###License管理详情页

    ###输入/输出参数

    * id                               —— pk
    * company                          —— 公司
    * email                            —— 邮箱
    * full_name                        —— 联系人姓名
    * nodes                            —— 节点数量
    * license_type                     —— License类型
    * hostname                         —— 主机名
    * start_date                       —— 生效时间
    * expiration_date                  —— 过期时间
    * ctime                            —— 创建时间
    * cuser                            —— 创建用户

    """

    queryset = License.objects.all()
    serializer_class = LicenseSerializer
