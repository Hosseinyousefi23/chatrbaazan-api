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
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^category/$', views.GetCategory.as_view()),
    url(r'^city/$', views.GetCity.as_view()),
    url(r'^banner/$', views.GetBanner.as_view()),
    url(r'^company/$', views.GetCompanies.as_view()),
    url(r'^label/(?P<slug>.*)$', views.LabelViews.as_view()),
    url(r'^user/product/$', views.GetUserProduct.as_view()),
    url(r'^offer/$', views.GetOffers.as_view(), name="getOffers"),
    url(r'^offer/(?P<slug>.*)/$', views.GetOffer.as_view(), name="getOffer"),
    url(r'^extension/$', views.Extension.as_view(), name='extension'),
    url(r'^bestcompanies/$', views.BestCompanies.as_view()),
    url(r'^failure/(?P<slug>.*)/$',
        views.FailureOffer.as_view(), name="reportFailure"),
    url(r'^setting/$', views.SettingView.as_view(), name="setting"),
    url(r'^route/', include(router.urls)),
]
