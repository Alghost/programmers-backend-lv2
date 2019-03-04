from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^$', views.UserList.as_view(),
            name='user-list'),
    re_path('^/chkid$', views.ChkID.as_view(),
            name='user-chkid'),
    re_path('^/(?P<pk>[0-9]+)$',
            views.UserDetail.as_view(),
            name="user-detail"),
]
