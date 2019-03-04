"""programmers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


schema_view = get_swagger_view(title='프로그래머스 APIs')

urlpatterns = [
    path('docs/', schema_view),
    path('api/admin/', admin.site.urls),
    path('api/fbusers', include('fbuser.urls')),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token-refresh',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('api/posts', include('post.urls')),
    path('api/comments', include('comment.urls')),
    path('api/likes', include('like.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
