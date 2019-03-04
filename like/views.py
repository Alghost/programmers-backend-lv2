from rest_framework import mixins
from rest_framework import generics

from fbuser.permissions import FbuserOwnerPermissionOrReadOnly
from fbuser.models import Fbuser

from .models import Like
from .serializers import LikeSerializer

# Create your views here.


class LikeDetail(
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):

    serializer_class = LikeSerializer
    permission_classes = (FbuserOwnerPermissionOrReadOnly, )

    def get_serializer(self, *args, **kwargs):
        # for Authentication
        if self.request.method != 'GET':
            like_data = {}
            like_data.update(self.request.data)
            like_data.update({
                'writer': Fbuser.objects.get(pk=self.request.user.id).id
            })

            serializer = LikeSerializer(data=like_data)
            serializer.is_valid(raise_exception=True)
            return serializer
        else:
            return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Like.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
