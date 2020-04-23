from collections import OrderedDict

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from shop.models import Product, Company, Category
from shop.renderers import CustomJSONRenderer
from shop.serializers2 import QuerySerializer, CouponSerializer, CompanySerializer, CategorySerializer


class CouponAPI(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST',)
    serializer_class = QuerySerializer

    def get_queryset(self, request, serializer):
        result = Product.objects.filter(pk=1000)
        return result

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.get_queryset(request, serializer)
        fields = serializer.validated_data.get('attributes', None)
        include = serializer.validated_data.get('include', None)

        data = CouponSerializer(result, fields=fields,
                                include=include, many=True,
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


class CompanyAPI(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST',)
    serializer_class = QuerySerializer

    def get_queryset(self, request, serializer):
        result = Company.objects.filter(pk__lt=1000)
        return result

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.get_queryset(request, serializer)
        fields = serializer.validated_data.get('attributes', None)
        include = serializer.validated_data.get('include', None)

        data = CompanySerializer(result, fields=fields,
                                 include=include, many=True,
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

    def get_queryset(self, request, serializer):
        result = Category.objects.filter(pk=5)
        return result

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.get_queryset(request, serializer)
        fields = serializer.validated_data.get('attributes', None)
        include = serializer.validated_data.get('include', None)

        data = CategorySerializer(result, fields=fields,
                                  include=include, many=True,
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
