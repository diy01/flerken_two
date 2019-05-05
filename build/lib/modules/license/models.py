# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.


class License(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    company = models.CharField(null=False, max_length=100, verbose_name='公司')
    email = models.CharField(null=False, max_length=100, verbose_name='邮箱')
    full_name = models.CharField(null=False, max_length=100, verbose_name='联系人姓名')
    nodes = models.IntegerField(null=False, default=0, verbose_name='节点数量')
    license_type = models.CharField(null=False, max_length=30, verbose_name='License类型')
    hostname = models.CharField(null=False, max_length=32, verbose_name='主机名')
    start_date = models.CharField(null=False, max_length=30, verbose_name='生效时间')
    expiration_date = models.CharField(null=False, max_length=30, verbose_name='过期时间')

    class Meta:
        db_table = 'license'
