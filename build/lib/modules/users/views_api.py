from django.contrib import auth
from django.contrib.auth.models import User
from django.db import transaction
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters
from rest_framework import parsers, renderers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.users.serializers import UserSerializer
from utils.base import BaseListCreateAPIView, content
from utils.base_exception import APIValidateException


class UserToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.username:
            return Response({'detail': u'用户未认证'}, status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key})


class UpdateUserToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    @transaction.atomic()
    @content
    def post(self, request, *args, **kwargs):
        if not request.user.username:
            return Response({'detail': u'用户未认证'}, status.HTTP_401_UNAUTHORIZED)
        Token.objects.filter(user_id=request.user.id).delete()
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key})


class ChangeUserPwd(BaseListCreateAPIView):
    """
    用户修改密码.

    输入参数：

    * old_password              ——   旧密码(必输)
    * password                  ——   新密码(必输)

    """

    paginate_by = None
    queryset = User.objects.all()

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['PATCH', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    @content
    def patch(self, request, *args, **kwargs):
        data = {'success': True, 'msg': u'新增成功'}
        username = request.user.username
        password = request.data.get('password')
        old_password = request.data.get('old_password')

        if not password:
            raise APIValidateException(u'password 不能为空')
        user = auth.authenticate(username=username, password=old_password)
        if not user:
            raise APIValidateException(u'旧密码不正确')
        user.set_password(password)
        user.save()
        self.changeLog(user.id, user.username, u'修改密码')
        return Response(data)
