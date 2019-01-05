from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from accounts.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer, PasswordChangeSerializer
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from rest_framework import mixins, generics
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import UserSendCode, User
from accounts.serializers import UserSendCodeSerializer, CustomUserDetailsSerializer
from chatrbaazan import settings
from accounts.serializers import UserSendCodeSerializer, CustomUserDetailsSerializer, UserUpdateSerializer, \
    ChangePasswordSerializer
from chatrbaazan.env import ENV
from contact.models import Contact
from contact.serializers import ContactSerializer
from shop.models import validate_phone, validate_mobile
from shop.renderers import CustomJSONRenderer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class UserSendCodeView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'GET',)
    serializer_class = UserSendCodeSerializer

    # queryset = Contact.objects.all()

    def post(self, request, format=None, *args, **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.data.update(
            user=request.user.pk if not request.user.is_anonymous else None)
        request.data.update(status=2)
        request.POST._mutable = mutable
        return self.create(request, *args, **kwargs)

    def get(self, request, format=None, *args, **kwargs):
        if not request.user.is_anonymous:
            usercode = UserSendCode.objects.filter(user=request.user)
        else:
            usercode = None
        return CustomJSONRenderer().renderData(UserSendCodeSerializer(usercode, many=True).data)


class UserDetailsView(RetrieveUpdateAPIView):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """
    serializer_class = CustomUserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        https://github.com/Tivix/django-rest-auth/issues/275
        """
        return User().objects.none()


class UserViews(mixins.ListModelMixin, mixins.UpdateModelMixin,
                mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    allowed_method = ('PUT',)
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def get_object(self, request):
        return User.objects.get(pk=request.user.pk)

    def put(self, request, format=None, *args, **kwargs):
        mobile = request.POST.get('mobile', None)
        if mobile is not None:
            validate_mobile(mobile)
            if request.user.mobile != mobile:
                if User.objects.filter(mobile=mobile):
                    return CustomJSONRenderer().render({'message': 'تلفن همراه قبلا وارد شده است.'***REMOVED***, status=400)

        partial = kwargs.pop('partial', False)
        instance = self.get_object(request)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {***REMOVED***

        return Response(serializer.data)


class ChangePassword(mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    allowed_method = ('PUT',)
    serializer_class = ChangePasswordSerializer

    def put(self, request, format=None, *args, **kwargs):
        password_old = request.POST.get('password_old', None)
        password_1 = request.POST.get('password_1', None)
        password_2 = request.POST.get('password_2', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if password_1 != password_2:
            raise ValidationError({'message': 'password not contains '***REMOVED***)

        user = User.objects.get(pk=request.user.pk)

        if user.check_password(password_old):
            user.set_password(password_1)
            user.save()
            return CustomJSONRenderer().renderData(CustomUserDetailsSerializer(user, many=False).data)
        else:
            raise ValidationError({'password_old': 'password old not match'***REMOVED***)


def confirm_emil(request, key):
    print(str(vars(request)))
    return Response(key)


def account_login(request):
    return HttpResponseRedirect(ENV['URI_FRONT'] + 'login')


class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _(
                "لینک بازنشانی گذرواژه به ایمیل ثبت نامی شما ارسال گردید.")***REMOVED***,
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("گذرواژه شما با موفقیت بروز رسانی گردید.")***REMOVED***
        )


class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")***REMOVED***)
