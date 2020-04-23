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
from django.conf.urls import url, include
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
from shop import views2
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^v1/category/$', views.GetCategory.as_view()),
    url(r'^v1/city/$', views.GetCity.as_view()),
    url(r'^v1/banner/$', views.GetBanner.as_view()),
    url(r'^v1/company/$', views.GetCompanies.as_view()),
    url(r'^v1/label/(?P<slug>.*)$', views.LabelViews.as_view()),
    url(r'^v1/user/product/$', views.GetUserProduct.as_view()),
    url(r'^v1/offer/$', views.GetOffers.as_view(), name="getOffers"),
    url(r'^v1/offer/(?P<slug>.*)/$', views.GetOffer.as_view(), name="getOffer"),
    url(r'^v1/extension/$', views.Extension.as_view(), name='extension'),
    url(r'^v1/bestcompanies/$', views.BestCompanies.as_view()),
    url(r'^v1/search/$', views.Search.as_view()),
    url(r'^v1/companies/$', views.Companies.as_view()),
    url(r'^v1/score/$', views.Score.as_view()),
    url(r'^v1/failure/(?P<slug>.*)/$',
        views.FailureOffer.as_view(), name="reportFailure"),
    url(r'^v1/setting/$', views.SettingView.as_view(), name="setting"),
    url(r'^v1/route/', include(router.urls)),
]

v2patterns = [
    url(r'^v2/coupon/$', views2.CouponAPI.as_view()),
    url(r'^v2/company/$', views2.CompanyAPI.as_view()),
    url(r'^v2/category/$', views2.CategoryAPI.as_view()),
]

urlpatterns += v2patterns
