# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Device(models.Model):
    devicename = models.CharField(db_column='Devicename', max_length=50)  # Field name made lowercase.
    deviceip = models.CharField(db_column='Deviceip', max_length=50)  # Field name made lowercase.
    cpucorecount = models.IntegerField(db_column='CPUcorecount')  # Field name made lowercase.
    memorysize = models.IntegerField()
    operatingsystem = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'
