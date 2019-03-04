from django.urls import path, re_path
from . import views

urlpatterns = [
    #     re_path('^$', views.CommentList.as_view(),
    #             name='comment-list'),
    re_path('^/(?P<pk>[0-9]+)$',
            views.CommentDetail.as_view(),
            name="comment-detail"),
    re_path('^/(?P<ppk>[0-9]+)/comments$',
            views.CommentCommentsList.as_view(),
            name="comment-comments-list"),
    re_path('^/(?P<ppk>[0-9]+)/likes$',
            views.CommentLikesList.as_view(),
            name="comment-likes-list"),
]
