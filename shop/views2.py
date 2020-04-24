from collections import OrderedDict

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from shop.models import Product, Company, Category
from shop.renderers import CustomJSONRenderer
from shop.serializers2 import QuerySerializer, DynamicQueryResponseSerializer


class FetchAPI(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST',)

    def get_queryset(self):
        return None

    def post_api(self, request, model):
        serializer = QuerySerializer(data=request.data, model=model)
        serializer.is_valid(raise_exception=True)
        q = serializer.validated_data
        response_serializer = DynamicQueryResponseSerializer(instance=self.get_queryset(), q=q, model=model,
                                                             many=True,
                                                             context={'request': request})
        data = response_serializer.data
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


class CouponAPI(FetchAPI):
    def get_queryset(self):
        return Product.objects.all()

    def post(self, request):
        return self.post_api(request, Product)


class CompanyAPI(FetchAPI):
    def get_queryset(self):
        return Company.objects.all()

    def post(self, request):
        return self.post_api(request, Company)


class CategoryAPI(FetchAPI):
    def get_queryset(self):
        return Category.objects.all()

    def post(self, request):
        return self.post_api(request, Category)
