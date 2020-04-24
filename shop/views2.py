from collections import OrderedDict

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from shop.filters import ProductFilter, CompanyFilter
from shop.models import Product, Company, Category
from shop.renderers import CustomJSONRenderer
from shop.serializers2 import QuerySerializer, CouponSerializer, CompanySerializer, CategorySerializer


class CouponAPI(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST',)
    serializer_class = QuerySerializer

    def get_queryset(self):
        return Product.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, model=Product)
        serializer.is_valid(raise_exception=True)
        q = serializer.validated_data
        result = self.get_queryset()
        where = q.get('where', None)
        if where:
            f = ProductFilter(where, queryset=result)
            result = f.qs

        data = CouponSerializer(result, q=q, many=True,
                                context={'request': request}).data
        return CustomJSONRenderer().renderData(
            OrderedDict([
                # ('count', self.page.paginator.count),
                # ('code_count', self.code_count),
                # ('offer_count', self.offer_count),
                # ('next', self.get_next_link()),
                # ('previous', self.get_previous_link()),
                ('results', data),
                # ('dataCompany',
                #  CompanySerializer(dataCompany, many=False, context={'request': request},
                #                    pop=['available']).data if dataCompany else None),
                # ('category', category_frontend_name)
            ])
        )
        # except Exception as e:
        #     raise serializers.ValidationError(e)


class CompanyAPI(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST',)
    serializer_class = QuerySerializer

    def get_queryset(self):
        return Company.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, model=Company)
        serializer.is_valid(raise_exception=True)
        q = serializer.validated_data
        result = self.get_queryset()
        where = q.get('where', None)
        if where:
            f = CompanyFilter(where, queryset=result)
            result = f.qs
        data = CompanySerializer(result, q=q, many=True,
                                 context={'request': request}).data
        return CustomJSONRenderer().renderData(
            OrderedDict([
                # ('count', self.page.paginator.count),
                # ('code_count', self.code_count),
                # ('offer_count', self.offer_count),
                # ('next', self.get_next_link()),
                # ('previous', self.get_previous_link()),
                ('results', data),
                # ('dataCompany',
                #  CompanySerializer(dataCompany, many=False, context={'request': request},
                #                    pop=['available']).data if dataCompany else None),
                # ('category', category_frontend_name)
            ])
        )


class CategoryAPI(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST',)
    serializer_class = QuerySerializer

    def get_queryset(self):
        return Category.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, model=Category)
        serializer.is_valid(raise_exception=True)
        q = serializer.validated_data
        result = self.get_queryset()
        where = q.get('where', None)
        if where:
            f = CompanyFilter(where, queryset=result)
            result = f.qs
        data = CategorySerializer(result, q=q, many=True,
                                  context={'request': request}).data
        return CustomJSONRenderer().renderData(
            OrderedDict([
                # ('count', self.page.paginator.count),
                # ('code_count', self.code_count),
                # ('offer_count', self.offer_count),
                # ('next', self.get_next_link()),
                # ('previous', self.get_previous_link()),
                ('results', data),
                # ('dataCompany',
                #  CompanySerializer(dataCompany, many=False, context={'request': request},
                #                    pop=['available']).data if dataCompany else None),
                # ('category', category_frontend_name)
            ])
        )
