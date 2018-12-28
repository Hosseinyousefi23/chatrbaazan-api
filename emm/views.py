from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from emm.serializers import EmailRegisterSerializer


class EmailRegisterView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_method = ('POST',)
    serializer_class = EmailRegisterSerializer

    def post(self, request, format=None, *args, **kwargs):
        return self.create(request, *args, **kwargs)

