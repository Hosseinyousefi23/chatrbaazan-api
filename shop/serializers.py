import operator
import os
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.aggregates import Sum
from django.template.defaultfilters import truncatechars
from django.urls.base import reverse
from django.utils.text import Truncator
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_auth.registration.serializers import RegisterSerializer

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers

from rest_framework_jwt.settings import api_settings

from like.models import Like
from shop.models import City, Banner, Category, Product, Discount, Company,ShopSetting, ProductLabel, ProductGallery, UserProduct
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
    link = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ('id', 'title', 'image', 'is_slider', 'link','location')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
            # return obj.image.url

    def get_link(self, obj):
        if obj.link:
            return obj.link
        elif obj.category:
            if obj.category.slug:
                return self.context['request'].build_absolute_uri(
                    reverse('getOffers') + '?category_slug={}'.format(obj.category.slug))
                return self.context['request'].build_absolute_uri(reverse('getOffer', args=[obj.category.slug]))
            pass
        elif obj.product:
            if obj.product.slug:
                return self.context['request'].build_absolute_uri(reverse('getOffer', args=[obj.product.slug]))
            pass
        else:
            pass

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)

        for fd in pop:
            self.fields.pop(fd)


class CategorySerializer(serializers.ModelSerializer):
    open_chatrbazi = serializers.SerializerMethodField()
    all_chatrbazi = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'english_name', 'available', 'all_chatrbazi', 'open_chatrbazi', 'slug')

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)
        for fd in pop:
            self.fields.pop(fd)

    def get_all_chatrbazi(self, obj):
        sum = Product.objects.values('category').annotate(sum=Sum('chatrbazi')).values('sum').filter(
            category__id=obj.pk)
        if sum.count() > 0:
            return sum[0]['sum']
        else:
            return 0

    def get_open_chatrbazi(self, obj):
        sum = Product.objects.values('category').annotate(sum=Sum('chatrbazi')).values('sum').filter(
            category__id=obj.pk).filter(priority=1)
        if sum.count() > 0:
            return sum[0]['sum']
        else:
            return 0


class CategoryMenuSerializer(serializers.ModelSerializer):
    open_chatrbazi = serializers.SerializerMethodField()
    all_chatrbazi = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'english_name', 'available',
                  'all_chatrbazi', 'open_chatrbazi', 'slug', 'company')

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)
        for fd in pop:
            self.fields.pop(fd)

    def get_all_chatrbazi(self, obj):
        sum = Product.objects.values('category').annotate(sum=Sum('chatrbazi')).values('sum').filter(
            category__id=obj.pk)
        if sum.count() > 0:
            return sum[0]['sum']
        else:
            return 0

    def get_open_chatrbazi(self, obj):
        sum = Product.objects.values('category').annotate(sum=Sum('chatrbazi')).values('sum').filter(
            category__id=obj.pk).filter(priority=1)
        if sum.count() > 0:
            return sum[0]['sum']
        else:
            return 0

    def get_company(self, obj):
        compnaies = Company.objects.filter(category__id=obj.id)
        if compnaies:
            return CompanySerializer(compnaies,many=True).data
        
class CompanySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('name', 'available', 'slug', 'description', 'image','link')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        else:
            pass

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


class ProductGallerySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductGallery
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        else:
            pass

    def get_title(self, obj):
        pass
        # return os.path.split(obj.image.url)[0]


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
    discount_code = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    explanation_short = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    # type = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id',
                  'name', 'priority','discount_code', 'explanation', 'explanation_short', 'expiration_date', 'price',
                  'chatrbazi', 'is_free', 'english_name',
                  'image', 'category', 'label', 'city', 'company', 'gallery', 'slug',
                  'like','link','file','type')

    def get_explanation_short(self, obj):
        return Truncator(obj.explanation).chars(300)

    # def get_type(self,obj):
        # return obj.get_type_display()

    def get_file(self, obj, *args, **kwargs):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)


    def get_image(self, obj, **kwargs):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)

    def get_city(self, obj):
        if obj.city:
            return CitySerializer(obj.city.all(), many=True, pop=['available']).data

    def get_company(self, obj):
        if obj.company:
            return CompanySerializer(obj.company.all().order_by('-priority'), many=True,
                                     context={'request': self.context['request']},
                                     pop=['available']).data

    def get_category(self, obj):
        if obj.category:
            return CategorySerializer(obj.category.all(), many=True, pop=['available']).data

    def get_label(self, obj):
        if obj.label:
            return ProductLabelSerializer(obj.label.all(), many=True, pop=['available']).data

    def get_discount_code(self, obj):
        if obj.discount_code:
            if obj.is_free:
                return obj.discount_code
            else:
                pass
        else:
            pass

    def get_gallery(self, obj):
        if obj.gallery:
            return ProductGallerySerializer(obj.gallery.all(), context=self.context, many=True).data
        else:
            pass

    def get_like(self, obj):
        return obj.click
        # like = Like.objects.filter(like=1).filter(product__id=obj.id)
        # if like.count() > 0:
        #     return int(like.count())
        # else:
        #     return 0

    # def get_dislike(self, obj):
    #     dislike = Like.objects.filter(like=2).filter(product__id=obj.id)
    #     if dislike.count() > 0:
    #         return int(dislike.count())
    #     else:
    #         return 0

    def __init__(self, instance, pop=[], *args, **kwargs):
        super().__init__(instance, **kwargs)
        for fd in pop:
            self.fields.pop(fd)


class UserProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = UserProduct
        fields = ('user', 'product', 'created_at', 'updated_at')

    def get_product(self, obj):
        if obj.product:
            return ProductSerializer(Product.objects.get(pk=obj.product.pk), many=False,
                                     context={'request': self.context['request']}).data
        else:
            return None


class ShopSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSetting
        fields = '__all__'
