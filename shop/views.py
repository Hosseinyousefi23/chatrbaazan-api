from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from shop.renderers import CustomJSONRenderer


def test(request):
    return render(request, 'index.html')


def testr(request):
    return Response('test')


class HomeDetails(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        data = {
            'state': [
                {'id': '1', 'name': 'تهران', 'en_name': 'tehran'},
                {'id': '1', 'name': 'تهران', 'en_name': 'tehran'},
                {'id': '1', 'name': 'تهران', 'en_name': 'tehran'},
            ],
            'city': [
                {'id': '1', 'name': 'تهران', 'en_name': 'tehran', 'parent': '1'},
                {'id': '1', 'name': 'تهران', 'en_name': 'tehran', 'parent': '1'},
                {'id': '1', 'name': 'تهران', 'en_name': 'tehran', 'parent': '1'},
            ],
            'category': [
                {'id': '1', 'name': 'فست فود', 'slug': 'fastfood', 'sub': {}},
                {'id': '1', 'name': 'فست فود', 'slug': 'fastfood', 'sub': {}},
                {'id': '1', 'name': 'فست فود', 'slug': 'fastfood', 'sub': {}},
                {'id': '1', 'name': 'فست فود', 'slug': 'fastfood', 'sub': {}},
            ],
            'result': {
                'id': '1',
                'priority': '1',
                'resourcetype': 'Ticket',
                'title': 'Test Title',
                'tag': {},
                'link': 'http://google.com',
                'image': 'address image',
                'explanation': 'description',
                'expiration_date': 'expiration date',
                'company': [{}],
                'chatrbazi': 3001,
                'category': [
                    {'id': '1', 'name': 'فست فود', 'slug': 'fastfood', 'sub': {}},
                    {'id': '1', 'name': 'فست فود', 'slug': 'fastfood', 'sub': {}},
                ],
                'state': [
                    {'id': '1', 'name': 'تهران', 'en_name': 'tehran'},
                    {'id': '1', 'name': 'تهران', 'en_name': 'tehran'},
                ],
                'city': [
                    {'id': '1', 'name': 'تهران', 'en_name': 'tehran'},
                    {'id': '1', 'name': 'تهران', 'en_name': 'tehran'},
                ]
            },
        }
        return CustomJSONRenderer().render('ok', data)
