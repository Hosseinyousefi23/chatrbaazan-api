from collections import OrderedDict
from django.db.models import Count, Max

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

from like.models import Like
from like.serializers import LikeSerializer
from shop.models import City, Banner, Category, Product, Company
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
        data = BannerSerializer(bannerData, many=True, context={'request': request***REMOVED***).data
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
        ordering = request.GET.get('ordering', 'created_at')
        order = ['favorites', 'topchatrbazi', 'created_at']
        if ordering not in order:
            ordering = '-created_at'

        cityId = request.GET.get('city', None)
        categoryId = request.GET.get('category', None)
        categorySlug = request.GET.get('category_slug', None)
        companyId = request.GET.get('company', None)
        companySlug = request.GET.get('company_slug', None)
        search = request.GET.get('search', None)

        if cityId is not None:
            city = City.objects.filter(id=convert_to_int(cityId))
            if city.count() > 0:
                products = products.filter(city__id__in=city.values('id'))
            else:
                return None
        if categoryId is not None or categorySlug:
            if categoryId is not None:
                category = Category.objects.filter(id=convert_to_int(categoryId))
            elif categorySlug is not None:
                category = Category.objects.filter(slug=categorySlug)
            if category.count() > 0:
                products = products.filter(category__id__in=category.values('id'))
            else:
                return None
        if companyId is not None or companySlug is not None:
            if companyId is not None:
                company = Company.objects.filter(id=convert_to_int(companyId))
            elif companySlug is not None:
                company = Company.objects.filter(slug=companySlug)

            if company.count() > 0:
                products = products.filter(company__id__in=company.values('id'))
            else:
                return None
        if search is not None:
            products = products.filter(Q(name__contains=search) | Q(explanation__contains=search) |
                                       Q(company__name=search) | Q(category__name=search))
        if products is not None or products.count() > 0:  # fix ordering products
            if ordering == 'created_at':
                products = products.order_by(ordering, '-expiration_date')
            else:
                if ordering == 'favorites':
                    like = Like.objects.values('product__id').filter(like=1).annotate(count=Count('like')).order_by(
                        '-count')
                    products = products.filter(id__in=like.values('product__id'))
                elif ordering == 'topchatrbazi':
                    products = products.all().order_by('-chatrbazi')
                else:
                    return None
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


def convert_to_int(number):
    try:
        cnumber = int(number)
        return cnumber
    except ValueError as verr:
        return 0
    except Exception as ex:
        return 0
