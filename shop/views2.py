from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Product, Company, Category, ProductLabel
from shop.renderers import CustomJSONRenderer
from shop.serializers import CategoryMenuSerializer, CompanyDetailSerializer, ProductLabelSerializer
from shop.serializers2 import QuerySerializer, DynamicQueryResponseSerializer


class FetchAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST',)

    def post_api(self, request, model):
        serializer = QuerySerializer(data=request.data, model=model)
        serializer.is_valid(raise_exception=True)
        q = serializer.validated_data
        response_serializer = DynamicQueryResponseSerializer(instance=self.get_queryset(), q=q, model=model,
                                                             many=True,
                                                             context={'request': request})
        data = response_serializer.data
        return Response({'result': data})


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


class Search(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    def get(self, request):
        rank_min = 0.0
        query = request.GET.get('q', None)
        half_space = '‌'
        query = query.replace(half_space, ' ')
        vector = SearchVector('name') + SearchVector('english_name')
        # vector = SearchVector('name','english_name')
        vector2 = SearchVector('name')
        search_query = SearchQuery(query, search_type='phrase')
        # categories = Category.objects.annotate(rank=SearchRank(vector, search_query)).filter(
        #     rank__gt=rank_min).order_by('-rank')
        categories = Category.objects.annotate(similarity=TrigramSimilarity('name', query)).filter(
            similarity__gt=rank_min).order_by('-similarity')
        companies = Company.objects.annotate(rank=SearchRank(vector, search_query)).filter(rank__gt=rank_min).order_by(
            '-rank')
        labels = ProductLabel.objects.annotate(rank=SearchRank(vector2, search_query)).filter(
            rank__gt=rank_min).order_by('-rank')
        return CustomJSONRenderer().render({
            'categories': CategoryMenuSerializer(categories, pop=['all_chatrbazi', 'open_chatrbazi', 'company'],
                                                 many=True, context={'request': request}).data,
            'companies': CompanyDetailSerializer(companies, many=True, pop=['description', 'product_company'],
                                                 context={'request': request}).data,
            'tags': ProductLabelSerializer(labels, many=True, context={'request': request}).data,
        })
