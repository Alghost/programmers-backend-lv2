from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status


from .models import Fbuser
from .serializers import FbuserSerializer
from .permissions import FbuserPermissionOrReadOnly

# Create your views here.


class UserList(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):

    serializer_class = FbuserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Fbuser.objects.all().order_by('id')

        return Fbuser.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetail(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        generics.GenericAPIView):

    serializer_class = FbuserSerializer
    permission_classes = (FbuserPermissionOrReadOnly, )

    def get_queryset(self):
        return Fbuser.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ChkID(APIView):
    def get(self, request, *args, **kwargs):
        try:
            Fbuser.objects.get(username=request.query_params['t'])
        except:
            return Response()

        return Response(status=status.HTTP_400_BAD_REQUEST)
