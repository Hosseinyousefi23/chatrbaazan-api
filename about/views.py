from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from about.models import About
from about.serializers import AboutSerializer
from contact.models import Contact
from contact.serializers import ContactSerializer
from shop.renderers import CustomJSONRenderer


class AboutView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AboutSerializer

    # queryset = Contact.objects.all()

    def get(self, request, format=None, *args, **kwargs):
        about = About.objects.filter(status=1).first()
        if about:
            return CustomJSONRenderer().renderData(
                AboutSerializer(about, many=False, context={'request': request***REMOVED***).data)
        else:
            return CustomJSONRenderer().renderData([])
