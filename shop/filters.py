from django_filters import rest_framework as filters

from shop.models import Product


class ProductFilter(filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'id': ['exact', 'lt', 'gt'],
            'name': ['exact', 'contains', 'icontains'],
            'english_name': ['exact', 'contains', 'icontains'],
            'company__id': ['exact'],
            'category__id': ['exact'],
            'company__name': ['exact', 'contains', 'icontains'],
            'category__name': ['exact', 'contains', 'icontains'],
            'company__english_name': ['exact', 'contains', 'icontains'],
            'category__english_name': ['exact', 'contains', 'icontains'],
        }


class CompanyFilter(filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'id': ['exact', 'lt', 'gt'],
            'name': ['exact', 'contains', 'icontains'],
            'english_name': ['exact', 'contains', 'icontains'],
            'category__id': ['exact'],
            'category__name': ['exact', 'contains', 'icontains'],
            'category__english_name': ['exact', 'contains', 'icontains'],
        }


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'id': ['exact', 'lt', 'gt'],
            'name': ['exact', 'contains', 'icontains'],
            'english_name': ['exact', 'contains', 'icontains'],
        }
