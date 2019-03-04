from rest_framework import permissions
from django.contrib.auth.hashers import check_password, make_password

from .models import Fbuser, FbuserAuth


class FbuserOwnerPermissionOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        # for ReadOnly
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # for Swagger
        if not request.data:
            return True

        data = view.get_serializer().data
        if 'writer' not in data:
            return False

        if request.user.id == data['writer']:
            return True

        return False


class FbuserPermissionOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    사용자 수정을 본인만 가능하도록 권한 설정
    """

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        # for ReadOnly
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # for Swagger
        if not request.data:
            return True

        if request.path[:13] != '/api/fbusers/':
            return False

        data = request.data
        if 'password' not in data:
            return False

        user_id = ''.join(list(filter(str.isdigit, request.path)))

        if int(user_id) != request.user.id:
            return False

        auth = FbuserAuth()
        fbuser = auth.authenticate(request)

        if not check_password(data['password'], fbuser.password):
            return False

        return True
