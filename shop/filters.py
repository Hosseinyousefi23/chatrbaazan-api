from django_filters import rest_framework as filters

from shop.models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    ideq = filters.NumberFilter(field_name='id')
    created_at = filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = Product
        fields = {
            'id': ['exact'],
        }


class CompanyFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    ideq = filters.NumberFilter(field_name='id')
    created_at = filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = Product
        fields = {
            'id': ['exact', 'lt', 'gt'],
        }


class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    ideq = filters.NumberFilter(field_name='id')
    created_at = filters.NumberFilter(lookup_expr='year')

    class Meta:
        model = Product
        fields = {
            'id': ['exact', 'lt', 'gt'],
        }
