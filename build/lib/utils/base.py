# -*- coding: utf-8 -*-
import json
import time
import uuid

from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import QueryDict
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from flerken import configs
from modules.users.models import ChangeLog
from modules.users.models import Navigation, Menu, NavigationMenu, GroupMenu, DefaultGroup
from utils.base_exception import APIValidateException


class PublicView(TemplateView):

    # def dispatch(self, request, *args, **kwargs):
    #     url = request.get_full_path()
    #     if not request.user or not request.user.id:
    #         callback_url = "http://" + self.request.get_host() + "/user/ssologin/"
    #         basePath = BasePath.objects.filter().first()
    #         if basePath:
    #             login_url = "{0}/sso/login/".format(basePath.sso_url.rstrip("/")) + "?redirect_url=" + quote(callback_url + "?redirect_url=" + quote(url))
    #         return HttpResponseRedirect(login_url)
    #     return super(PublicView, self).dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super(PublicView, self).get_context_data(**kwargs)
    #     context['domain'] = self.request.user
    #     navigations, menus = self.get_menu()
    #     context['navigations'] = navigations[0:7]
    #     context['menus'] = menus
    #     context['system_name'] = u'flerken'
    #     context['system_version'] = '1.0.0'
    #     basePath = BasePath.objects.filter().first()
    #     if basePath:
    #         context['sso_base_domain'] = basePath.sso_url.rstrip("/") + "/"
    #     return context

    def get_menu(self):
        navid = 0
        if configs.SYSTEM_NAME:
            curNavs = Navigation.objects.filter(name=configs.SYSTEM_NAME)
            if len(curNavs) > 0:
                navid = curNavs[0].id
        if not navid:
            curNavs = Navigation.objects.filter(path__contains=self.request.get_host())
            if len(curNavs) > 0:
                navid = curNavs[0].id
        is_superuser = self.request.user.is_superuser
        data = []
        navs = Navigation.objects.all().order_by("-weight")
        all_menus = Menu.objects.all().order_by("-weight")
        if is_superuser != 1:
            ids = []
            current_user_set = self.request.user
            current_group_set = Group.objects.filter(Q(user=current_user_set))  # 获取当前用户所对应的所有组
            gids = []
            for group in current_group_set:
                gids.append(group.id)
            if len(gids) <= 0:
                gids = [dg.group_id for dg in DefaultGroup.objects.all()]
            group_menu_list = GroupMenu.objects.filter(group_id__in=gids)
            for menu in group_menu_list:
                ids.append(menu.menu_id)
            ids = list(set(ids))  # id 去重
            all_menus = all_menus.filter(id__in=ids)
            navids = [n.navigation_id for n in NavigationMenu.objects.filter(menu_id__in=ids)]
            navs = navs.filter(id__in=list(set(navids)))

        if not navid and len(navs) > 0:
            navid = navs[0].id
        if navid:
            self.request.session['navid'] = navid
        mids = [n.menu_id for n in NavigationMenu.objects.filter(navigation_id=navid)]
        navigations = []
        for n in navs:
            navmids = [nm.menu_id for nm in NavigationMenu.objects.filter(navigation_id=n.id)]
            t = model_to_dict(n)
            t['current'] = False
            for m in all_menus:
                if t['path']:
                    if len(str(t['path']).split("?")) == 1:
                        t['path'] = t['path'] + "?_navid=%s" % n.id
                    else:
                        t['path'] = t['path'] + "&_navid=%s" % n.id
                    break
                if not m.pid:
                    continue
                if m.id in navmids:
                    if is_superuser != 1 and m.id not in ids:
                        continue
                    if len(str(m.path).split("?")) == 1:
                        t['path'] = m.path + "?_navid=%s" % n.id
                    else:
                        t['path'] = m.path + "&_navid=%s" % n.id
                    break
            if str(t['id']) == str(navid):
                t['current'] = True
            navigations.append(t)
        all_menus = all_menus.filter(id__in=mids)
        for m in all_menus.filter(pid=0):
            m = model_to_dict(m)
            m['children'] = []
            m['has_children'] = False
            for me in all_menus.filter(pid=m['id']):
                me = model_to_dict(me)
                me['path'] = me['path']
                m['children'].append(me)
                m['has_children'] = True
            data.append(m)
        return navigations, data


def content(fun):
    def reset(request, *args, **kwargs):
        response = fun(request, *args, **kwargs)
        # response.content_type = "text/json;charset=utf-8"
        return response

    return reset


class BaseBasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method.lower() == 'get':
            return True
        return request.user.is_superuser or request.user.is_staff


class BaseListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (BaseBasePermission,)

    validator_classes = None

    """
    Concrete view for listing a queryset or creating a model instance.
    """

    @content
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            id_list = request.data.getlist("pk[]", [])
        else:
            id_list = request.data.get("pk[]", [])
        id = request.data.get('pk', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数pk[]和pk不能都为空')
        key = ''
        if self.serializer_class:
            key = self.serializer_class.Meta.model._meta.app_label
        queryset = self.get_queryset()
        queryset = queryset.filter(pk__in=id_list)
        for q in queryset:
            self.changeLog(q.pk, key, json.dumps(model_to_dict(q)))
        queryset.delete()
        return Response({'success': True, 'msg': 'succ!'})

    @transaction.atomic()
    def perform_create(self, serializer):
        obj = serializer.save()
        if self.validator_classes:
            for validator in self.validator_classes:
                validator().validate(obj)
        json_obj = json.dumps(model_to_dict(obj))
        key = ''
        if self.serializer_class:
            key = self.serializer_class.Meta.model._meta.app_label
        self.changeLog(obj.pk, key, json_obj)

    def changeLog(self, res_id, index, message, **kwargs):
        uid = str(uuid.uuid1())
        if 'uid' in kwargs:
            uid = str(kwargs['uid'])
        action = None
        if 'action' in kwargs:
            action = kwargs['action']
        if self.serializer_class:
            resource = self.serializer_class.Meta.model._meta.db_table
        else:
            resource = ''
        if 'resource' in kwargs:
            resource = kwargs['resource']
        http_method = self.request.method.lower()
        if not action:
            if http_method == 'get':
                action = 'search'
            elif http_method == 'post':
                action = 'create'
            elif http_method == 'put' or http_method == 'patch':
                action = 'update'
            elif http_method == 'delete':
                action = 'delete'
        ChangeLog.objects.create(user_id=self.request.user.id, resource=resource, res_id=res_id, uuid=uid,
                                 action=action, index=index, message=message, change_time=int(time.time()),
                                 ctime=int(time.time()))


class BaseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (BaseBasePermission,)

    validator_classes = None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @transaction.atomic()
    def perform_update(self, serializer):
        obj = serializer.save()
        if self.validator_classes:
            for validator in self.validator_classes:
                validator().validate(obj)
        json_obj = json.dumps(model_to_dict(obj))
        key = ''
        if self.serializer_class:
            key = self.serializer_class.Meta.model._meta.app_label
        self.changeLog(obj.pk, key, json_obj)

    @transaction.atomic()
    def perform_destroy(self, instance):
        pk = instance.pk
        key = ''
        if self.serializer_class:
            key = self.serializer_class.Meta.model._meta.app_label
        json_obj = json.dumps(model_to_dict(instance))
        self.changeLog(pk, key, json_obj)
        instance.delete()

    def changeLog(self, res_id, index, message, **kwargs):
        uid = str(uuid.uuid1())
        if 'uid' in kwargs:
            uid = str(kwargs['uid'])
        action = None
        if 'action' in kwargs:
            action = kwargs['action']
        if self.serializer_class:
            resource = self.serializer_class.Meta.model._meta.db_table
        else:
            resource = ''
        if 'resource' in kwargs:
            resource = kwargs['resource']
        http_method = self.request.method.lower()
        if not action:
            if http_method == 'get':
                action = 'search'
            elif http_method == 'post':
                action = 'create'
            elif http_method == 'put' or http_method == 'patch':
                action = 'update'
            elif http_method == 'delete':
                action = 'delete'
        ChangeLog.objects.create(user_id=self.request.user.id, resource=resource, res_id=res_id, uuid=uid,
                                 action=action, index=index, message=message, change_time=int(time.time()),
                                 ctime=int(time.time()))
