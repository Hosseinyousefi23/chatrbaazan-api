from collections import OrderedDict

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from shop.models import City, Banner, Category, Product
from shop.renderers import CustomJSONRenderer
from shop.serializers import CitySerializer, BannerSerializer, CategorySerializer, ProductSerializer
from rest_auth.registration.views import RegisterView


def test(request):
    return render(request, 'index.html')


class TestAPi(APIView):
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        return Response("test")


def testr(request):
    return Response('test')


class GetCategory(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        categoryData = Category.objects.filter(available=True)
        categoryDataSerializer = CategorySerializer(categoryData, many=True).data
        # TODO Cache Data Category
        return CustomJSONRenderer().renderData(categoryDataSerializer)


class GetCity(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        print(str(City.objects.count()))
        dt = CitySerializer(City.objects.all(), many=True)
        return CustomJSONRenderer().renderData(dt.data)


class GetBanner(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        bannerData = Banner.objects.filter(available=True).order_by('-id')[:6]
        data = BannerSerializer(bannerData, many=True).data
        return CustomJSONRenderer().renderData(data)


class GetOffers(APIView, PageNumberPagination):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)
    page_size = 20
    max_page_size = 1000

    # renderer_classes = (JSONRenderer,)
    def get_queryset(self, request):
        limits = request.GET.get('limits', 10)
        try:
            limits = int(limits)
        except ValueError as e:
            limits = 5
        if limits >= 30:
            limits = 30
        ordering = request.GET.get('ordering', '-priority')
        order = ['priority', '-priority', 'created_at']
        if ordering not in order:
            ordering = '-ordering'

        cityId = request.GET.get('city', None)
        categoryId = request.GET.get('category', None)
        products = Product.objects.all().order_by(ordering, '-expiration_date')
        search = request.GET.get('search', None)

        if cityId is not None:
            city = City.objects.filter(id=cityId)
            if city.count() > 0:
                products = products.filter(city__id__in=city.values('id'))
        elif categoryId is not None:
            category = Category.objects.filter(id=categoryId)
            if category.count() > 0:
                products = products.filter(category__id__in=category.values('id'))
        if search is not None:
            products = products.filter(Q(name__contains=search) | Q(explanation__contains=search))
        return self.paginate_queryset(products, self.request)

    def get(self, request, format=None, ):
        products = self.get_queryset(request)
        if products is None:
            return CustomJSONRenderer().render400()
        return CustomJSONRenderer().renderData(
            OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', ProductSerializer(products, many=True, context={'request': request***REMOVED***).data)
            ])
        )


class GetOffer(APIView, PageNumberPagination):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    def get(self, request, slug, format=None, ):
        product = Product.objects.filter(slug=slug)
        if not product.exists():
            return CustomJSONRenderer().render400()
        return CustomJSONRenderer().renderData(
            ProductSerializer(product.first(), context={'request': request***REMOVED***, many=False).data)
