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
from django.urls import path, re_path
from django.conf.urls import url, include
from rest_auth.registration.views import VerifyEmailView, RegisterView
from rest_auth.views import LogoutView , PasswordResetView , PasswordResetConfirmView , LoginView
from django.conf.urls.static import static
from allauth.account.views import confirm_email as allauthemailconfirmation
from allauth.account.views import confirm_email

from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, ObtainJSONWebToken
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from accounts.views import UserDetailsView, account_login
from chatrbaazan import settings
from shop import serializers

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', account_login, name="account_login"),
    url(r'^', include('shop.urls')),
    path('auth/login/', LoginView.as_view()),
    path('auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^auth/account-confirm-email/', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', allauthemailconfirmation,
        name="account_confirm_email"),
    path('auth/refresh/', refresh_jwt_token),
    path('auth/verify/', verify_jwt_token),
    url(r'^auth/password/reset/$', PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^auth/user/$', UserDetailsView.as_view(), name='rest_user_details'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    url(r'^api/v1/contact/', include('contact.routers')),
    url(r'^api/v1/like/', include('like.routers')),
    url(r'^api/v1/cart/', include('carts.routers')),
    url(r'^api/v1/about/', include('about.routers')),
    url(r'^api/v1/user/', include('accounts.routers')),
    url(r'^api/v1/email/', include('emm.routers')),
    url(r'^api/v1/sms/', include('sms.routers')),
    url(r'^api/v1/', include('shop.routers')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
