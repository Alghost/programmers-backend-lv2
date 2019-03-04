import coreapi
from rest_framework import serializers
from rest_framework.schemas import AutoSchema
from .models import Post
from comment.models import Comment
from like.models import Like


class PostSerializer(serializers.ModelSerializer):
    """
    [Serializer] 게시글
    """

    tstamp = serializers.DateTimeField(
        read_only=True,
        format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Post
        fields = '__all__'


class PostSwaggerSchema(AutoSchema):

    def __init__(self):
        super().__init__([])

    def get_serializer_fields(self, path, method):
        fields = []
        if method == 'PUT' or method == 'POST':
            fields.append(
                coreapi.Field(
                    name="contents",
                    required=True,
                    location="form"),
            )
        return fields
