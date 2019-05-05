from django.urls import path

from modules.users import views_api

urlpatterns = [

    # 用户token
    path('token/', views_api.UserToken.as_view(), name='api_token'),

    # 获取新的用户token
    path('newtoken/', views_api.UpdateUserToken.as_view(), name='api_newtoken'),

]
