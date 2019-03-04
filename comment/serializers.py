import coreapi
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.schemas import AutoSchema
from .models import Comment
from post.models import Post


class CommentSerializer(serializers.ModelSerializer):
    """
    [Serializer] 댓글
    """

    def validate(self, data):
        """
        Parent instance가 있는지 확인하기 위한 validator
        """
        data = super().validate(data)

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
            raise serializers.ValidationError('No supported content type')

        return data

    tstamp = serializers.DateTimeField(
        read_only=True,
        format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSwaggerSchema(AutoSchema):

    def __init__(self):
        super().__init__([])

    def get_serializer_fields(self, path, method):
        fields = []
        if path == '/api/comments/{id}':
            if method == 'PUT':
                fields.append(
                    coreapi.Field(
                        name="contents",
                        required=True,
                        location="form"),
                )
        elif '{ppk}' in path:
            if method == 'PUT' or method == 'POST':
                fields.append(
                    coreapi.Field(
                        name="contents",
                        required=True,
                        location="form"),
                )

        return fields
