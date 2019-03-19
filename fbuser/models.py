from django.db import models
from django.contrib.auth.hashers import check_password


# Create your models here.


class Fbuser(models.Model):
    """
    Fbusers
    """

    username = models.CharField(max_length=32,
                                verbose_name='이름')
    password = models.CharField(max_length=64,
                                verbose_name='비밀번호')
    email = models.EmailField(max_length=256,
                              unique=True,
                              verbose_name='이메일주소')
    is_active = models.BooleanField(default=False,
                                    verbose_name='활성화 여부')
    is_staff = models.BooleanField(default=False,
                                   verbose_name='관리자 여부')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')

    def __repr__(self):
        return 'Fbuser()'

    def __str__(self):
        return '({}) {}'.format(self.username, self.email)

    class Meta:
        db_table = 'programmers_fbuser'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'


class FbuserAuth(object):
    def authenticate(self, request, username=None, password=None):
        if username and password:
            try:
                user = Fbuser.objects.get(email=username)
                if check_password(password, user.password) \
                        and self.user_can_authenticate(user):
                    return user

            except Fbuser.DoesNotExist:
                return None
        else:
            if request.user.is_authenticated:
                return Fbuser.objects.get(pk=request.user.id)

        return None

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', False)
        return is_active

    def get_user(self, user_id):
        try:
            user = Fbuser.objects.get(pk=user_id)
        except Fbuser.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
