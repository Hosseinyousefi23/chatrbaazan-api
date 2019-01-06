from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from rest_framework import serializers, exceptions
from sms.models import SmsUser
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers
from rest_auth.models import TokenModel
from rest_auth.utils import import_callable
from rest_framework_jwt.settings import api_settings

from accounts.adapters import CustomUserAccountAdapter
from accounts.models import UserSendCode
from shop.models import City, Banner, Category, Product, Discount, Company, ProductLabel, validate_phone
from .models import User
import re
from allauth.account import app_settings
UserModel = get_user_model()


class RegisterSerializerCustom(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={
                                   'blank': 'لطفا ایمیل خود را وارد نمایید.'***REMOVED***)
    first_name = serializers.CharField(required=True, write_only=True, error_messages={
                                       'blank': 'لطفا نام خود را وارد نمایید.'***REMOVED***)
    last_name = serializers.CharField(required=True, write_only=True, error_messages={
                                      'blank': '‌لطفا نام خانوادگی خود را وارد نمایید.'***REMOVED***)
    mobile = serializers.CharField(required=True, write_only=True,error_messages={
                                      'blank': '‌لطفا تلفن همراه خود را وارد نمایید.'***REMOVED***)
    password1 = serializers.CharField(required=True, write_only=True,error_messages={
                                      'blank': 'لطفا گذرواژه خود را وارد نمایید'***REMOVED***)
    password2 = serializers.CharField(required=True, write_only=True,error_messages={
                                      'blank': '‌لطفا تکرار گذرواژه خود را وارد نمایید.'***REMOVED***)

    def validate_email(self, email):
        email = CustomUserAccountAdapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(
                _("این ایمیل قبلا ثبت نام شده است."))
        else:
            raise serializers.ValidationError(
               _("ایمیل معتبر نمی‌باشد."))

    def validate_password1(self, password):
        return CustomUserAccountAdapter().clean_password(password)

    def validate(self, data):
        if User.objects.filter(mobile=data['mobile']).exists():
            raise serializers.ValidationError(
                _("شماره الزامی است.."))
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("رمز عبور یکسان نمی باشد"))
        return data

    def get_cleaned_data(self):
        print(str(self.validated_data.get('password1', '')))
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'mobile': self.validated_data.get('address', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        ***REMOVED***

    def save(self, request):
        adapter = CustomUserAccountAdapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    mobile_active = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'mobile', 'address', 'mobile_active', 'postal_code')
        read_only_fields = ('email',)

    def get_mobile_active(self, obj):
        sms_user = SmsUser.objects.filter(user__id=obj.pk)
        if sms_user:
            if sms_user.first().status == 1:
                return True
            else:
                return False
        else:
            pass


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    mobile = serializers.CharField(required=False, validators=[validate_phone])
    address = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'mobile', 'address', 'postal_code')
        read_only_fields = ('email',)


class UserSendCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSendCode
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True***REMOVED***,
            'status': {'write_only': True***REMOVED***
        ***REMOVED***


class ChangePasswordSerializer(serializers.ModelSerializer):
    password_old = serializers.CharField(required=True)
    password_1 = serializers.CharField(required=True)
    password_2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('password_old', 'password_1', 'password_2')
        extra_kwargs = {
            'password': {'write_only': True***REMOVED***
        ***REMOVED***


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(error_messages={
                                   'blank': 'لطفا ایمیل خود را وارد نمایید'***REMOVED***, required=False, allow_blank=True)
    password = serializers.CharField(error_messages={
                                     'blank': 'لطفا گذرواژه خود را وارد نمایید'***REMOVED***, style={'input_type': 'password'***REMOVED***)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = _('لطفا ایمیل و گذرواژه خود را وارد نمایید')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('لطفا نام کاربری و گذرواژه خود را وارد نمایید')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        elif username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('لطفا نام کاربری و گذرواژه خود را وارد نمایید')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(
                        email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('اکانت شما غیرفعال شده است')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('اطلاعات کاربری اشتباه می باشد')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(
                        _('ایمیل تایید نشده است.'))

        attrs['user'] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField(error_messages={
        'blank': 'لطفا ایمیل خود را وارد نمایید.'
    ***REMOVED***)

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {***REMOVED***

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        ***REMOVED***

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(
        error_messages={'blank': 'لطفا گذرواژه خود را وارد نمایید'***REMOVED***, max_length=128)
    new_password2 = serializers.CharField(
        error_messages={'blank': 'لطفا گذرواژه خود را مجددا وارد نمایید'***REMOVED***, max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    set_password_form_class.error_messages['password_mismatch'] = _(
        "گذرواژه ها یکسان نمی باشند."),

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {***REMOVED***
        password1 = attrs['new_password1']
        password2 = attrs['new_password2']
        print('password1', password1)
        print('password2', password2)
        if password1 != password2:
            print('ey joon')
            raise ValidationError(
                {'new_password2': ['گذرواژه ها یکسان نمی باشند.']***REMOVED***)
        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']***REMOVED***)

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']***REMOVED***)

        return attrs

    def save(self):
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)
