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

from shop.adapters import CustomUserAccountAdapter
from shop.models import City, Banner

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_mobile_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
import re


def validate_mobile(mobile):
    if mobile:
        if not re.match('^09[\d]{9}$', mobile):
            raise ValidationError(u'شماره موبایل صحیح نمی باشد.')
        return mobile


class RegisterSerializerCustom(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    mobile = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = CustomUserAccountAdapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))

    def validate_password1(self, password):
        return CustomUserAccountAdapter().clean_password(password)

    def validate(self, data):
        if User.objects.filter(mobile=data['mobile']).exists():
            raise serializers.ValidationError(
                _("Mobile Number Exists."))
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        print(str(self.validated_data.get('password1', '')))
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'mobile': self.validated_data.get('address', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = CustomUserAccountAdapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


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
