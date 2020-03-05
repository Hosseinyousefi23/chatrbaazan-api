# Create your views here.
import operator
import random
import uuid
from collections import OrderedDict
from datetime import datetime, timedelta
# Create your views here.
from functools import reduce

from django.db.models import Q
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import City, Banner, Category, Product, Company, UserProduct, Failure, ShopSetting, \
    ProductLabel
from shop.renderers import CustomJSONRenderer
from shop.serializers import CitySerializer, BannerSerializer, ProductSerializer, \
    UserProductSerializer, CompanySerializer, ShopSettingSerializer, CategoryMenuSerializer, ProductLabelSerializer, \
    CompanyDetailSerializer


def test(request):
    return render(request, 'index.html')


class TestAPi(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)
    def get(self, request, format=None, ):
        return Response("I Love You Python :) * Hossein yousefi *")
        # return HttpResponse(uuid.uuid1(random.randint(0, 281474976710655)))


def testr(request):
    return Response('test')


class GetCategory(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        categoryData = Category.objects.filter(
            available=True).order_by('order', '-id')
        categoryDataSerializer = CategoryMenuSerializer(
            categoryData, many=True, context={'request': request}).data
        # TODO Cache Data Category
        # return CustomJSONRenderer().renderData(categoryDataSerializer)
        sumChatrbazi = Product.objects.filter(
            Q(expiration_date__gt=datetime.now()) | Q(expiration_date__isnull=True)).aggregate(Sum('chatrbazi'))
        # print('sql sum all chatrbaazi: ' , str(sumChatrbazi.query))
        # print('data sum all chatrbaazi', str(sumChatrbazi))
        # if sumChatrbazi.count() > 0:
        #     sumChatrbazi = sumChatrbazi[0]['sum']
        # else:
        #     sumChatrbazi = 0
        return CustomJSONRenderer().render({
            'data': categoryDataSerializer,
            'all_chatrbazi': sumChatrbazi['chatrbazi__sum']
        })


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
        bannerData = Banner.objects.filter(available=True).filter(
            Q(expiration_date__gt=datetime.now()) | Q(expiration_date__isnull=True)).order_by('-location')[:10]
        data = BannerSerializer(bannerData, many=True, context={
            'request': request}).data
        return CustomJSONRenderer().renderData(data)


class GetUserProduct(APIView, PageNumberPagination):
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET',)
    page_size = 20
    max_page_size = 1000

    # renderer_classes = (JSONRenderer,)
    def get_queryset(self, request):
        userData = UserProduct.objects.filter(
            user=request.user).order_by('-id')
        return self.paginate_queryset(userData, self.request)

    def get(self, request, format=None, ):
        userData = self.get_queryset(request)
        data = UserProductSerializer(userData, many=True, context={
            'request': request}).data
        return CustomJSONRenderer().renderData(
            OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data),
            ])
        )


class GetOffers(APIView, PageNumberPagination):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)
    page_size = 20
    max_page_size = 1000

    # renderer_classes = (JSONRenderer,)
    def get_queryset(self, request):
        print("query part")
        limits = request.GET.get('limits', 100)
        try:
            limits = int(limits)
        except ValueError as e:
            limits = 100
        if limits >= 30:
            limits = 30

        self.page_size = limits  # fix limit query
        ordering = request.GET.get('ordering', 'created_at')
        order = ['favorites', 'topchatrbazi', 'created_at', 'expired', ]
        if ordering not in order:
            ordering = 'created_at'

        cityId = request.GET.get('city', None)
        categoryId = request.GET.get('category', None)
        categorySlug = request.GET.get('category_slug', None)
        companyId = request.GET.get('company', None)
        companySlug = request.GET.get('company_slug', None)
        search = request.GET.get('search', None)
        type_product = request.GET.get('type', None)
        expire = request.GET.get('expire', False)
        products = Product.objects.all()
        if cityId is not None:
            city = City.objects.filter(id=convert_to_int(cityId))
            print('count city in filter', str(city.count()))
            if city.count() > 0:
                products = products.filter(
                    Q(city__id__in=city.values('id')) | Q(city__id__isnull=True))
                print('sql filter product by city', str(products.query))
            else:
                return None
        if categoryId is not None or categorySlug:
            if categoryId is not None:
                category = Category.objects.filter(
                    id=convert_to_int(categoryId))
            elif categorySlug is not None:
                category = Category.objects.filter(slug=categorySlug)
            if category.count() > 0:
                products = products.filter(
                    category__id__in=category.values('id'))
            else:
                return None
        if companyId is not None or companySlug is not None:
            if companyId is not None:
                company = Company.objects.filter(id=convert_to_int(companyId))
            elif companySlug is not None:
                company = Company.objects.filter(slug=companySlug)

            if company.count() > 0:
                products = products.filter(
                    company__id__in=company.values('id'))
            else:
                return None
        if search is not None:
            products = products.filter(Q(label__name__contains=search) |
                                       Q(company__name__contains=search)).distinct()
        if products.count() > 0:  # fix ordering products
            if ordering == 'created_at':
                products = products.order_by('-created_at', '-expiration_date')
            else:
                if ordering == 'favorites':
                    # like = Like.objects.values('product__id').filter(like=1).annotate(count=Count('like')) \
                    #     .filter(product__id__in=products.values('id')).order_by(
                    #     '-count')
                    # if like.count() > 0:
                    #     margesort = marge_sort(
                    #         [id[0] for id in like.values_list('product__id')],
                    #         [id[0] for id in products.values_list('id')])
                    #     products = products.filter(id__in=margesort)
                    # else:
                    products = products.order_by('-click')

                elif ordering == 'topchatrbazi':
                    products = products.order_by('-chatrbazi', '-click')
                elif ordering == 'expired':
                    print("expired part")
                    products = products.order_by('-expiration_date', '-created_at').filter(
                        (Q(expiration_date__isnull=False) & Q(expiration_date__lt=datetime.now())) | (Q(
                            expiration_date__isnull=True) & Q(
                            created_at__lt=datetime.now() - timedelta(6 * 365 / 12))))  # 6 month ago
                else:
                    return None
            if type_product is not None:
                products = products.filter(type=type_product)
        if not expire:
            products = products.filter(
                Q(expiration_date__gt=datetime.now()) | Q(expiration_date__isnull=True))
        print("return part")
        return self.paginate_queryset(products, self.request)

    def get(self, request, format=None, ):
        category_frontend_name = ""
        categoryId = request.GET.get('category', None)
        categorySlug = request.GET.get('category_slug', None)
        category = None
        if categoryId is not None:
            category = Category.objects.filter(
                id=convert_to_int(categoryId))
        elif categorySlug is not None:
            category = Category.objects.filter(slug=categorySlug)
        if category is not None:
            category_name = [i for i in category.values_list("name")]
            print("category name:")
            print(category_name)
            if len(category_name) > 0:
                category_frontend_name = category_name[0][0]

        products = self.get_queryset(request)
        if products is None:
            return CustomJSONRenderer().render404('product', '')
        companySlug = request.GET.get('company_slug', None)
        dataCompany = None
        if companySlug:
            company = Company.objects.filter(slug=companySlug)
            if company.count() > 0:
                dataCompany = company.first()
        data = ProductSerializer(products, many=True, pop=['explanation_short', 'file', 'gallery', 'like'], context={
            'request': request}).data
        return CustomJSONRenderer().renderData(
            OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data),
                ('dataCompany',
                 CompanySerializer(dataCompany, many=False, context={'request': request},
                                   pop=['available']).data if dataCompany else None),
                ('category', category_frontend_name)
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
            ProductSerializer(product.first(), context={'request': request}, many=False).data)


class FailureOffer(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    def get(self, request, slug, format=None, ):
        product = Product.objects.filter(slug=slug)
        if not product.exists():
            return CustomJSONRenderer().render404('product', '')

        print(str(vars(request.session)))
        if 'uuid_failure' in request.session:
            return CustomJSONRenderer().render({'message': 'گزارش توسط شما قبلا ارسال شده است'}, status=400)
        if not request.user.is_anonymous:
            user = request.user
        else:
            user = None
        request.session['uuid_failure'] = str(
            uuid.uuid1(random.randint(0, 281474976710655)))
        uuid_failure = request.session['uuid_failure']
        Failure.objects.create(product=product.first(),
                               user=user,
                               uuid=uuid_failure)
        product.update(failure=F('failure') + 1)
        return CustomJSONRenderer().render({'success': True}, 200)


class SettingView(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    def get(self, request, format=None):
        setting = ShopSetting.objects.filter(enable=True)
        return CustomJSONRenderer().renderData(ShopSettingSerializer(setting.first(), many=False).data)


class GetCompanies(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    def get(self, request, format=None):
        search = request.GET.get('search', None)
        if search is not None:
            Companies = Company.objects.filter(
                Q(name__contains=search)).distinct()
        else:
            Companies = None
        return CustomJSONRenderer().renderData(
            CompanySerializer(Companies, many=True, context={'request': request}).data)


def convert_to_int(number):
    try:
        cnumber = int(number)
        return cnumber
    except ValueError as verr:
        return 0
    except Exception as ex:
        return 0


def marge_sort(first_list, second_list):
    # if type(first_list) is dict:
    #     first_list = first_list.items()
    # if type(second_list) is dict:
    #     second_list = second_list.items()
    return first_list + list(set(second_list) - set(first_list))


class LabelViews(APIView, PageNumberPagination):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)
    page_size = 20
    max_page_size = 1000

    def get_queryset(self, request, slug):
        limits = request.GET.get('limits', 100)
        search = request.GET.get('search', None)
        ordering = request.GET.get('ordering', 'created_at')
        order = ['favorites', 'topchatrbazi', 'created_at']
        company = request.GET.get('company_slug', None)
        if company == 'ندارد':
            company = None
        category = request.GET.get('category_slug', None)
        if category == 'ندارد':
            category = None
        type_product = request.GET.get('type', None)
        expire = request.GET.get('expire', False)
        exclude = request.GET.get('exclude', None)
        smart = request.GET.get('smart', False)
        keywords = slug.split('$')

        if ordering not in order:
            ordering = 'created_at'

        try:
            limits = int(limits)
        except ValueError as e:
            limits = 100
        if limits >= 30:
            limits = 30

        self.page_size = limits  # fix limit query
        # ordering = request.GET.get('ordering', 'created_at')
        # order = ['favorites', 'topchatrbazi', 'created_at']
        # if ordering not in order:
        #     ordering = 'created_at'
        if smart:
            products = Product.objects.all()
            ids = [product.id for product in products if not product.is_expired]
            products = Product.objects.filter(id__in=ids).filter(
                reduce(operator.or_, (Q(label__name=x) for x in keywords))).distinct()
            if exclude:
                products = products.filter(~Q(id=exclude))
            if len(products) < limits:
                if category:
                    support = Product.objects.filter(id__in=ids).filter(~Q(id=exclude) &
                                                                        (Q(category__name__contains=category) | Q(
                                                                            category__slug__contains=category) | Q(
                                                                            category__english_name__contains=category)))
                    # support = support.order_by('-created_at')
                    products = products.union(support)
            # products = products.order_by('-created_at')
            products = products[:limits]
        else:
            products = Product.objects.filter(Q(label__name__contains=slug))
            if search is not None:
                products = products.filter(
                    Q(category__name__contains=search) | Q(company__name__contains=search))
            if company is not None:
                products = products.filter(
                    Q(company__name__contains=company) | Q(company__slug__contains=company))
            if category is not None:
                products = products.filter(
                    Q(category__name__contains=category) | Q(
                        category__slug__contains=category)
                    | Q(category__english_name__contains=category))
            if products.count() > 0:  # fix ordering products
                if ordering == 'created_at':
                    products = products.order_by('-created_at', '-expiration_date')
                else:
                    if ordering == 'favorites':
                        products = products.order_by('-click')
                    elif ordering == 'topchatrbazi':
                        products = products.order_by('-chatrbazi', '-click')
                    else:
                        return None
            if type_product is not None:
                products = products.filter(type=type_product)

            if not expire:
                products = products.filter(
                    Q(expiration_date__gt=datetime.now()) | Q(expiration_date__isnull=True))

        return self.paginate_queryset(products, self.request)

    def get(self, request, slug=None, format=None):
        search = request.GET.get('search', None)
        if slug:
            slug = str(slug).replace('/', '')
            products = self.get_queryset(request, slug)
            if products is None:
                return CustomJSONRenderer().render404('product', '')
            companySlug = request.GET.get('company_slug', None)
            dataCompany = None
            if companySlug:
                company = Company.objects.filter(slug=companySlug)
                if company.count() > 0:
                    dataCompany = company.first()
            return CustomJSONRenderer().renderData(
                OrderedDict([
                    ('count', self.page.paginator.count),
                    ('next', self.get_next_link()),
                    ('previous', self.get_previous_link()),
                    ('results', ProductSerializer(products,
                                                  context={'request': request}, many=True).data),
                    ('dataCompany',
                     CompanySerializer(dataCompany, many=False, context={'request': request},
                                       pop=['available']).data if dataCompany else None)
                ])
            )
            # return CustomJSONRenderer().renderData(
            # ProductSerializer(products , context={'request': request} , many=True).data)
        else:
            print('None slug LabelViews ')
            PLable = None
            if search is not None:
                PLable = ProductLabel.objects.filter(Q(name__contains=search))
            return CustomJSONRenderer().renderData(ProductLabelSerializer(PLable, many=True, pop=['available']).data)


class Extension(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)
    serializer_class = CompanyDetailSerializer

    def get(self, request):
        url = request.GET['url']
        company_list = Company.objects.filter(link__contains=url)
        if len(company_list) > 0:
            company = company_list[0]
            ser = self.serializer_class(company, context={'request': request})
            json_data = JSONRenderer().render(ser.data)
            return HttpResponse(json_data)
        else:
            return HttpResponseNotFound('not found')


class BestCompanies(APIView, PageNumberPagination):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)
    page_size = 20
    max_page_size = 1000

    # renderer_classes = (JSONRenderer,)
    def get_queryset(self, request):
        size = request.GET.get('size', 36)
        try:
            size = int(size)
        except ValueError as e:
            size = 100
        if size > 36:
            size = 36

        companies = Company.objects.filter(priority__gt=3).order_by('-priority')[:size]

        return companies

    def get(self, request, format=None, ):

        companies = self.get_queryset(request)
        if companies is None:
            return CustomJSONRenderer().render404('company', '')

        data = CompanySerializer(companies, many=True, pop=['id', 'available', 'description', ], context={
            'request': request}).data
        return CustomJSONRenderer().renderData(
            OrderedDict([
                ('results', data),
            ])
        )
