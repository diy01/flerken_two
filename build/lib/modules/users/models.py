# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class ChangeLog(models.Model):
    ACTION = (
        ('create', u'新增'),
        ('update', u'修改'),
        ('delete', u'删除'),
    )

    id = models.AutoField(primary_key=True)
    uuid = models.CharField(db_column='uuid', max_length=128, null=True, default='')
    user_id = models.IntegerField(db_column='user_id', null=False, default=0)
    resource = models.CharField(db_column='resource', max_length=60, null=True, default='')
    res_id = models.CharField(db_column='res_id', max_length=64, null=True, default='')
    action = models.CharField(db_column='action', choices=ACTION, max_length=30, null=True, default='')
    index = models.CharField(max_length=100, null=True, default='', db_index=True)
    message = models.TextField(blank=True, default='')
    change_time = models.BigIntegerField(db_column='change_time', null=True, default=None, db_index=True)
    ctime = models.BigIntegerField(db_column='ctime', null=True, default=None)

    class Meta:
        index_together = ('resource', 'res_id')
        db_table = 'changelog'


class Menu(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    pid = models.IntegerField(db_column='pid', null=False, default=0)
    name = models.CharField(db_column='name', max_length=120, null=True, default='')
    path = models.CharField(max_length=360, null=True, default='')
    tag = models.CharField(max_length=120, null=True, default='')  # 标签
    weight = models.IntegerField(db_column='weight', null=True, default=0)  # 权重

    def has_child(self):  # 供菜单选择是生成树状菜单时使用
        return Menu.objects.filter(pid=self.id).count()

    def children(self):
        return Menu.objects.filter(pid=self.id)

    def superPermission(self):
        list = [u"系统管理"]
        return list

    def staffPermission(self):
        list = [u"查看业务线", u"授权审批", u"授权查询", u"任务查询"]
        return list

    class Meta:
        db_table = 'auth_menu'


class GroupMenu(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    group_id = models.IntegerField(db_column='group_id', null=False, default=0)
    menu_id = models.IntegerField(null=True, default=0)

    class Meta:
        db_table = 'auth_group_menus'


class DefaultGroup(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    group_id = models.IntegerField(null=False, default=0, verbose_name=u'组ID')

    class Meta:
        db_table = 'auth_default_group'


class Navigation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False, default='', verbose_name=u'子系统名称')
    icon = models.CharField(max_length=30, null=True, default='', blank=True, verbose_name=u'icon')
    path = models.CharField(max_length=255, null=True, default='', blank=True, verbose_name=u'路径')
    weight = models.IntegerField(null=False, default=0, blank=True, verbose_name=u'权重')
    comment = models.CharField(max_length=60, null=False, default='', blank=True, verbose_name=u'系统描述')

    class Meta:
        db_table = 'auth_navigation'


class NavigationMenu(models.Model):
    id = models.AutoField(primary_key=True)
    navigation_id = models.IntegerField(null=False, default=0, verbose_name=u'子系统ID')
    menu_id = models.IntegerField(null=False, default=0, verbose_name=u'菜单ID')

    class Meta:
        db_table = 'auth_navigation_menu'


class Structure(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    pid = models.IntegerField(null=False, default=0, verbose_name=u'上级ID')
    name = models.CharField(max_length=100, null=False, default='', verbose_name=u'部门名称')
    full_name = models.CharField(max_length=100, unique=True, null=False, default='', verbose_name=u'部门全称')
    leader_id = models.IntegerField(null=False, default=0, blank=True, verbose_name=u'部门负责人ID')
    comment = models.CharField(max_length=255, null=False, default='', blank=True, verbose_name=u'描述')

    class Meta:
        db_table = 'structure'


class StructureUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    dept_id = models.IntegerField(null=False, default=0, verbose_name=u'部门ID')
    user_id = models.IntegerField(null=False, default=0, verbose_name=u'员工ID')

    class Meta:
        db_table = 'structure_user'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cell_phone = models.CharField(null=False, default='', max_length=60, blank=True, verbose_name=u'手机号')
    extend_user_id = models.CharField(null=False, default='', max_length=100, blank=True, verbose_name=u'第三方账号ID')

    class Meta:
        db_table = 'user_profile'


class LDAP(models.Model):
    STATUS = (
        (0, u'启用'),
        (1, u'禁用'),
    )

    id = models.AutoField(primary_key=True)
    server_uri = models.CharField(null=False, max_length=255, verbose_name=u'LDAP地址')
    bind_dn = models.CharField(null=False, max_length=255, verbose_name=u'绑定DN')
    password = models.CharField(null=False, max_length=255, verbose_name=u'密码')
    user_ou = models.TextField(null=False, verbose_name=u'用户OU')
    user_filter = models.CharField(null=False, max_length=255, default='', verbose_name=u'用户过滤器')
    status = models.IntegerField(null=False, default=0, choices=STATUS, verbose_name=u'状态')

    class Meta:
        db_table = 'sso_ldap'


class BasePath(models.Model):
    id = models.AutoField(primary_key=True)
    sso_url = models.CharField(max_length=255, null=False, default='', verbose_name=u'SSO')
    cmdb_url = models.CharField(max_length=255, null=False, default='', blank=True, verbose_name=u'CMDB')
    ticket_url = models.CharField(max_length=255, null=False, default='', blank=True, verbose_name=u'工单')
    monitor_url = models.CharField(null=False, max_length=255, default='', blank=True, verbose_name=u'监控系统')
    release_url = models.CharField(max_length=255, null=False, default='', blank=True, verbose_name=u'发布系统')

    class Meta:
        db_table = 'base_path'
