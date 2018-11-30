"""chatrbaazan URL Configuration

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
from django.urls import path
from django.conf.urls import url, include
from rest_auth.views import LogoutView
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, ObtainJSONWebToken
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from chatrbaazan import settings
from shop import serializers

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('shop.urls')),
    path('auth/login/', ObtainJSONWebToken.as_view()),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('auth/refresh/', refresh_jwt_token),
    path('auth/verify/', verify_jwt_token),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    url(r'^api/v1/contact/', include('contact.routers')),
    url(r'^api/v1/like/', include('like.routers')),
    url(r'^api/v1/cart/', include('carts.routers')),
    url(r'^api/v1/', include('shop.routers')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
