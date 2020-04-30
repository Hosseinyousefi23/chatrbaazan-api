from django_filters import rest_framework as filters
from rest_framework.generics import GenericAPIView

from shop.models import Product
GenericAPIView


class ProductFilter(filters.FilterSet):
    expired = filters.BooleanFilter(method='filter_expired')
    tag = filters.CharFilter(method='filter_tags')

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

    def filter_tags(self, queryset, name, lst):
        items = [item.strip("'\" ") for item in lst.strip('[]').split(',')]
        return queryset.filter(label__name__in=items)

    def filter_expired(self, queryset, name, value):
        ids = [item.id for item in queryset if item.is_expired == value]
        return queryset.filter(id__in=ids)


class CompanyFilter(filters.FilterSet):
    active = filters.BooleanFilter(field_name='available')

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
    active = filters.BooleanFilter(field_name='available')

    class Meta:
        model = Product
        fields = {
            'id': ['exact', 'lt', 'gt'],
            'name': ['exact', 'contains', 'icontains'],
            'english_name': ['exact', 'contains', 'icontains'],
        }
