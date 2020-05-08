from django_filters import rest_framework as filters

from shop.models import Product

CHOICES = {
    "product": 1,
    "app": 2,
    "offer": 3,
    "code": 4
}


class ProductFilter(filters.FilterSet):
    id = filters.CharFilter(method='filter_ids')
    expired = filters.BooleanFilter(method='filter_expired')
    tag = filters.CharFilter(method='filter_tags')
    type = filters.CharFilter(method='filter_type')

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains', 'icontains'],
            'english_name': ['exact', 'contains', 'icontains'],
            'company__id': ['exact'],
            'category__id': ['exact'],
            'company__name': ['exact', 'contains', 'icontains'],
            'category__name': ['exact', 'contains', 'icontains'],
            'company__english_name': ['exact', 'contains', 'icontains'],
            'category__english_name': ['exact', 'contains', 'icontains'],
            'slug': ['exact', 'contains', 'icontains'],

        }

    def filter_ids(self, queryset, name, value):
        items = [item.strip("'\" ") for item in value.strip('[]').split(',')]
        return queryset.filter(id__in=items)

    def filter_tags(self, queryset, name, lst):
        items = [item.strip("'\" ") for item in lst.strip('[]').split(',')]
        return queryset.filter(label__name__in=items)

    def filter_expired(self, queryset, name, value):
        ids = [item.id for item in queryset if item.is_expired == value]
        return queryset.filter(id__in=ids)

    def filter_type(self, queryset, name, lst):
        types = [item.strip("'\" ") for item in lst.strip('[]').split(',')]
        type_numbers = [CHOICES.get(typ, 0) for typ in types]
        return queryset.filter(type__in=type_numbers)


class CompanyFilter(filters.FilterSet):
    active = filters.BooleanFilter(field_name='available')
    id = filters.CharFilter(method='filter_ids')

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains', 'icontains'],
            'english_name': ['exact', 'contains', 'icontains'],
            'category__id': ['exact'],
            'category__name': ['exact', 'contains', 'icontains'],
            'category__english_name': ['exact', 'contains', 'icontains'],
            'slug': ['exact', 'contains', 'icontains'],
        }

    def filter_ids(self, queryset, name, value):
        items = [item.strip("'\" ") for item in value.strip('[]').split(',')]
        return queryset.filter(id__in=items)


class CategoryFilter(filters.FilterSet):
    active = filters.BooleanFilter(field_name='available')
    id = filters.CharFilter(method='filter_ids')

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains', 'icontains'],
            'english_name': ['exact', 'contains', 'icontains'],
            'slug': ['exact', 'contains', 'icontains'],
        }

    def filter_ids(self, queryset, name, value):
        items = [item.strip("'\" ") for item in value.strip('[]').split(',')]
        return queryset.filter(id__in=items)
