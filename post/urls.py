from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^$', views.PostList.as_view(),
            name='post-list'),
    re_path('^/(?P<pk>[0-9]+)$',
            views.PostDetail.as_view(),
            name="post-detail"),
    re_path('^/(?P<ppk>[0-9]+)/comments$',
            views.PostCommentsList.as_view(),
            name="post-comments-list"),
    re_path('^/(?P<ppk>[0-9]+)/likes$',
            views.PostLikesList.as_view(),
            name="post-likes-list"),
]
