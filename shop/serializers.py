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

from shop.models import City, Banner, Category, Product, Discount, Company, ProductLabel
from accounts.models import User
import re


def validate_mobile(mobile):
    if mobile:
        if not re.match('^09[\d]{9}$', mobile):
            raise ValidationError(u'شماره موبایل صحیح نمی باشد.')
        return mobile


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'english_name', 'available')

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)
        for fd in pop:
            self.fields.pop(fd)


class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ('id', 'title', 'image', 'is_slider')

    def get_image(self, obj):
        if obj.image:
            return obj.image.url

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)

        for fd in pop:
            self.fields.pop(fd)


class CategorySerializer(serializers.ModelSerializer):
    open_chatrbazi = serializers.SerializerMethodField()
    all_chatrbazi = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'english_name', 'available', 'all_chatrbazi', 'open_chatrbazi')

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)

        for fd in pop:
            self.fields.pop(fd)

    def get_all_chatrbazi(self, obj):
        pass

    def get_open_chatrbazi(self, obj):
        pass


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'available')

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)

        for fd in pop:
            self.fields.pop(fd)


class ProductLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLabel
        fields = ('name', 'available')

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)

        for fd in pop:
            self.fields.pop(fd)


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'discount', 'available')

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)

        for fd in pop:
            self.fields.pop(fd)


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name', 'priority', 'explanation', 'expiration_date', 'price', 'chatrbazi', 'is_free', 'english_name',
            'image', 'category', 'label', 'city', 'company')

    def get_image(self, obj):
        if obj.image:
            return obj.image.url

    def get_city(self, obj):
        if obj.city:
            return CitySerializer(obj.city.all(), many=True, pop=['available']).data

    def get_company(self, obj):
        if obj.company:
            return CompanySerializer(obj.company.all(), many=True, pop=['available']).data

    def get_category(self, obj):
        if obj.category:
            return CategorySerializer(obj.category.all(), many=True, pop=['available']).data

    def get_label(self, obj):
        if obj.label:
            return ProductLabelSerializer(obj.label.all(), many=True, pop=['available']).data

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)

        for fd in pop:
            self.fields.pop(fd)
