from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from contact.models import Contact
from contact.serializers import ContactSerializer
from shop.renderers import CustomJSONRenderer


class ContactView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET', 'POST',)
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def get(self, request, format=None, *args, **kwargs):
        # return self.list(request, *args, **kwargs)
        return CustomJSONRenderer().render400()

    def post(self, request, format=None, *args, **kwargs):
        # print(str(self.is_valid()))
        # print(str(request))
        # if formData.is_valid():
        return self.create(request, *args, **kwargs)
        # return CustomJSONRenderer().renderData(formData.error_messages)
