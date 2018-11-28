from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_auth.registration.serializers import RegisterSerializer

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers

from rest_framework_jwt.settings import api_settings

from shop.models import City, Banner, Category, Product, Discount
from accounts.models import User
import re


def validate_mobile(mobile):
    if mobile:
        if not re.match('^09[\d]{9***REMOVED***$', mobile):
            raise ValidationError(u'شماره موبایل صحیح نمی باشد.')
        return mobile


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'english_name')


class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ('id', 'title', 'image', 'is_slider')

    def get_image(self, obj):
        if obj.image:
            return obj.image.url


class CategorySerializer(serializers.ModelSerializer):
    open_chatrbazi = serializers.SerializerMethodField()
    all_chatrbazi = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'english_name', 'available')


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'discount', 'available')


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name', 'priority', 'explanation', 'expiration_date', 'price', 'chatrbazi', 'is_free', 'english_name',
            'image')

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
