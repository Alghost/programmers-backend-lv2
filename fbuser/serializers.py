import re
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Fbuser


class FbuserSerializer(serializers.ModelSerializer):
    """
    [Serializer] 사용자
    """

    password = serializers.CharField(
        write_only=True)

    registered_dttm = serializers.DateTimeField(
        read_only=True,
        format='%Y-%m-%d %H:%M:%S')

    def validate_password(self, value):
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$^+=!*()@%&]).{8,}$"
        if len(value) < 8:
            raise serializers.ValidationError(
                "비밀번호는 8자리 이상이어야 합니다")
        elif not re.match(regex, value):
            raise serializers.ValidationError(
                "비밀번호는 대/소문자, 숫자, 특수기호를 포함해야합니다")

        return make_password(value)

    class Meta:
        model = Fbuser
        fields = '__all__'
