from django.urls import path

from modules.users import views

urlpatterns = [

    path('login/', views.LoginPageView.as_view(), name='login'),

    path('syslogin/', views.SysLoginPageView.as_view(), name='syslogin'),

    path('dologin/', views.doLogin, name='dologin'),

    path('dosyslogin/', views.doSysLogin, name='dosyslogin'),

    path('ssologin/', views.sso_login),

    path(r'logout/', views.logout, name='logout'),

    # 我的个人信息
    path('myinfo/', views.MyInfoPageView.as_view(), name='view_myinfo'),

]
