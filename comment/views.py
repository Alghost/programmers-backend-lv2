from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, PermissionDenied
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from fbuser.models import Fbuser
from fbuser.permissions import FbuserOwnerPermissionOrReadOnly
from like.models import Like
from like.serializers import LikeSerializer, LikeSwaggerSchema
from .models import Comment
from .serializers import CommentSerializer, CommentSwaggerSchema

# Create your views here.


class CommentDetail(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):

    schema = CommentSwaggerSchema()
    serializer_class = CommentSerializer
    permission_classes = (FbuserOwnerPermissionOrReadOnly, )

    def get_queryset(self):
        return Comment.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentCommentsList(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        generics.GenericAPIView):

    schema = CommentSwaggerSchema()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer(self, *args, **kwargs):
        if 'ppk' not in self.kwargs:
            return CommentSerializer(data=self.request.data)

        # Generate POST data
        if self.request.method == 'POST':
            comment_data = {}
            comment_data.update(self.request.data)
            comment_data.update({
                'object_id': self.kwargs['ppk'],
                'content_type': ContentType.objects.get_for_model(Comment).id,
                'writer': Fbuser.objects.get(pk=self.request.user.id).id
            })
            serializer = CommentSerializer(data=comment_data)
            serializer.is_valid(raise_exception=True)
            return serializer

        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Comment.objects \
            .filter(content_type__model='comment') \
            .filter(object_id=int(self.kwargs['ppk'])) \
            .order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentLikesList(
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
                'content_type': ContentType.objects.get_for_model(Comment).id,
                'writer': Fbuser.objects.get(pk=self.request.user.id).id
            })
            serializer = LikeSerializer(data=like_data)
            serializer.is_valid(raise_exception=True)
            return serializer

        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Comment.objects \
            .filter(content_type__model='comment') \
            .filter(object_id=int(self.kwargs['ppk'])) \
            .order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
