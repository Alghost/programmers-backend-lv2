from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.schemas import AutoSchema
from .models import Like
from post.models import Post
from comment.models import Comment


class LikeSerializer(serializers.ModelSerializer):
    """
    [Serializer] 좋아요
    """

    def validate(self, attrs):
        """
        Parent instance가 있는지 확인하기 위한 validator
        """
        data = super().validate(attrs)

        if data['content_type'] == ContentType.objects.get_for_model(Comment):
            try:
                Comment.objects.get(id=data['object_id'])
            except Comment.DoesNotExist:
                raise serializers.ValidationError(
                    'No comment for id;{}'.format(data['object_id']))
        elif data['content_type'] == ContentType.objects.get_for_model(Post):
            try:
                Post.objects.get(id=data['object_id'])
            except Post.DoesNotExist:
                raise serializers.ValidationError(
                    'No post for id;{}'.format(data['object_id']))

        else:
            raise ValueError('No supported content type')

        return data

    registered_dttm = serializers.DateTimeField(
        read_only=True,
        format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Like
        fields = '__all__'


class LikeSwaggerSchema(AutoSchema):

    def __init__(self):
        super().__init__([])

    def get_serializer_fields(self, path, method):
        return []
