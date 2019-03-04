from django.urls import re_path
from . import views

urlpatterns = [
    re_path('^/(?P<pk>[0-9]+)$',
            views.LikeDetail.as_view(),
            name="like-detail"),
]
