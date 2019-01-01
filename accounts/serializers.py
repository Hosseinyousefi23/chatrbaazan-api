from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_auth.registration.serializers import RegisterSerializer

from django.contrib.auth import authenticate , get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers

from rest_framework_jwt.settings import api_settings

from accounts.adapters import CustomUserAccountAdapter
from accounts.models import UserSendCode
from shop.models import City , Banner , Category , Product , Discount , Company , ProductLabel , validate_phone
from .models import User
import re


class RegisterSerializerCustom(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True , write_only=True)
    last_name = serializers.CharField(required=True , write_only=True)
    mobile = serializers.CharField(required=True , write_only=True)
    password1 = serializers.CharField(required=True , write_only=True)
    password2 = serializers.CharField(required=True , write_only=True)

    def validate_email(self , email):
        email = CustomUserAccountAdapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))

    def validate_password1(self , password):
        return CustomUserAccountAdapter().clean_password(password)

    def validate(self , data):
        if User.objects.filter(mobile=data['mobile']).exists():
            raise serializers.ValidationError(
                _("Mobile Number Exists."))
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        print(str(self.validated_data.get('password1' , '')))
        return {
            'first_name': self.validated_data.get('first_name' , '') ,
            'last_name': self.validated_data.get('last_name' , '') ,
            'mobile': self.validated_data.get('address' , '') ,
            'password1': self.validated_data.get('password1' , '') ,
            'email': self.validated_data.get('email' , '') ,
        }

    def save(self , request):
        adapter = CustomUserAccountAdapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request , user , self)
        setup_user_email(request , user , [])
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name' , 'last_name' , 'email' , 'mobile' , 'address')
        read_only_fields = ('email' ,)


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    mobile = serializers.CharField(required=True , validators=[validate_phone])
    address = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name' , 'last_name' , 'email' , 'mobile' , 'address')
        read_only_fields = ('email' ,)


class UserSendCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSendCode
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True} ,
            'status': {'write_only': True}
        }


class ChangePasswordSerializer(serializers.ModelSerializer):
    password_old = serializers.CharField(required=True)
    password_1 = serializers.CharField(required=True)
    password_2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('password_old' , 'password_1' , 'password_2')
        extra_kwargs = {
            'password': {'write_only': True}
        }
