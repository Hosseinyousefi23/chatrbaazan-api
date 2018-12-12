from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import random
from sms.serializers import SmsUserSerializer


class SmsView(mixins.CreateModelMixin,
              generics.GenericAPIView):
    serializer_class = SmsUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None, *args, **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.data.update('status', 2)
        request.data.update('user', request.user if request.user else None)
        request.data.update('phone', request.POST.get('phone', None))
        request.data.update('code_verify', random.randint(1, 30) * 10)
        request.POST._mutable = mutable

    def get(self, request, format=None, *args, **kwargs):
        pass
