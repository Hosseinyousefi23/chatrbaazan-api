from django.shortcuts import render

# Create your views here.
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from rest_framework import mixins, generics
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from accounts.models import UserSendCode, User
from accounts.serializers import UserSendCodeSerializer, CustomUserDetailsSerializer, UserUpdateSerializer
from contact.models import Contact
from contact.serializers import ContactSerializer
from shop.renderers import CustomJSONRenderer


class UserSendCodeView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('POST', 'GET',)
    serializer_class = UserSendCodeSerializer

    # queryset = Contact.objects.all()

    def post(self, request, format=None, *args, **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.data.update(user=request.user.pk)
        request.data.update(status=2)
        request.POST._mutable = mutable
        return self.create(request, *args, **kwargs)

    def get(self, request, format=None, *args, **kwargs):
        usercode = UserSendCode.objects.filter(user=request.user)
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

    def put(self, request, format=None, *args, **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True
