from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from accounts.models import UserSendCode
from accounts.serializers import UserSendCodeSerializer
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
