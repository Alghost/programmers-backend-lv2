from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from fbuser.models import Fbuser
from fbuser.permissions import FbuserOwnerPermissionOrReadOnly
from comment.models import Comment
from comment.serializers import CommentSerializer, CommentSwaggerSchema
from like.models import Like
from like.serializers import LikeSerializer, LikeSwaggerSchema
from .models import Post
from .serializers import PostSerializer, PostSwaggerSchema

# Create your views here.


class PostList(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    schema = PostSwaggerSchema()

    def get_serializer(self, *args, **kwargs):
        # Generate POST data
        if self.request.method == 'POST':
            post_data = {}
            post_data.update(self.request.data)
            post_data.update({
                'writer': Fbuser.objects.get(pk=self.request.user.id).id
            })

            serializer = PostSerializer(data=post_data)
            serializer.is_valid(raise_exception=True)
            return serializer
        else:
            return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Post.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetail(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):

    serializer_class = PostSerializer
    permission_classes = (FbuserOwnerPermissionOrReadOnly, )
    schema = PostSwaggerSchema()

    def get_serializer(self, *args, **kwargs):
        # Generate POST data
        if self.request.method != 'GET':
            post_data = {}
            post_data.update(self.request.data)
            post_data.update({
                'writer': Fbuser.objects.get(pk=self.request.user.id).id
            })

            serializer = PostSerializer(data=post_data)
            serializer.is_valid(raise_exception=True)
            return serializer
        else:
            return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Post.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostCommentsList(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        generics.GenericAPIView):

    schema = CommentSwaggerSchema()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = CommentSerializer

    def get_serializer(self, *args, **kwargs):
        # For swagger
        if 'ppk' not in self.kwargs:
            res = CommentSerializer(data=self.request.data)
            res.is_valid(raise_exception=True)
            return res

        # Generate POST data
        if self.request.method == 'POST':
            comment_data = {}
            comment_data.update(self.request.data)
            comment_data.update({
                'object_id': self.kwargs['ppk'],
                'content_type': ContentType.objects.get_for_model(Post).id,
                'writer': Fbuser.objects.get(pk=self.request.user.id).id
            })

            serializer = CommentSerializer(data=comment_data)
            serializer.is_valid(raise_exception=True)
            return serializer

        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Comment.objects \
            .filter(content_type__model='post') \
            .filter(object_id=int(self.kwargs['ppk'])) \
            .order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostLikesList(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        generics.GenericAPIView):

    schema = LikeSwaggerSchema()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = LikeSerializer

    def get_serializer(self, *args, **kwargs):
        if 'ppk' not in self.kwargs:
            res = LikeSerializer(data=self.request.data)
            res.is_valid(raise_exception=True)
            return res

        # Generate POST data
        if self.request.method == 'POST':
            like_data = {}
            like_data.update(self.request.data)
            like_data.update({
                'object_id': self.kwargs['ppk'],
                'content_type': ContentType.objects.get_for_model(Post).id,
                'writer': Fbuser.objects.get(pk=self.request.user.id).id
            })

            serializer = LikeSerializer(data=like_data)
            serializer.is_valid(raise_exception=True)
            return serializer
        else:
            return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Like.objects \
            .filter(content_type__model='post') \
            .filter(object_id=int(self.kwargs['ppk'])) \
            .order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
