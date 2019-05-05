import json
from urllib.parse import unquote

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from utils.base import PublicView
from ..users.auth.ssoapi import get_token


def index_view(request):
    return HttpResponseRedirect('/app/')


class LoginPageView(TemplateView):
    template_name = 'user/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        return context


class SysLoginPageView(TemplateView):
    template_name = 'user/sys_login.html'

    def get_context_data(self, **kwargs):
        context = super(SysLoginPageView, self).get_context_data(**kwargs)
        return context


@csrf_exempt
def doLogin(request):
    data = {'success': False, 'msg': 'fail!'}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            data['success'] = True
            data['msg'] = 'succ!'
    else:
        data['msg'] = 'request method must be POST'
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def doSysLogin(request):
    data = {'success': False, 'msg': 'fail!'}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            data['success'] = True
            data['msg'] = 'succ!'
    else:
        data['msg'] = 'request method must be POST'
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


@csrf_exempt
def sso_login(request):
    tokenKey = request.GET.get('tokenKey', '')
    redirect_url = request.GET.get('redirect_url', '/')
    status, userinfo = get_token(tokenKey)
    if status:
        users = User.objects.filter(username=userinfo.get('username', ''))
        if len(users) <= 0:
            return HttpResponseRedirect('/login/')
        user = users[0]

        if user and user.is_active:
            auth.login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return HttpResponseRedirect(unquote(redirect_url))
    return HttpResponseRedirect('/login/')


class MyInfoPageView(PublicView):
    template_name = 'user/my_info.html'

    def get_context_data(self, **kwargs):
        context = super(MyInfoPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'我的个人信息'
        context['path1'] = u'用户管理'
        context['path2'] = u'我的个人信息'
        return context
