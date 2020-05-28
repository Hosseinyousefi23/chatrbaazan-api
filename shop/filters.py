from django.db.models import Q
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
    company__id = filters.CharFilter(method='filter_company_ids')
    category__id = filters.CharFilter(method='filter_category_ids')

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains', 'icontains'],
            'english_name': ['exact', 'contains', 'icontains'],
            'company__name': ['exact', 'contains', 'icontains'],
            'category__name': ['exact', 'contains', 'icontains'],
            'company__english_name': ['exact', 'contains', 'icontains'],
            'category__english_name': ['exact', 'contains', 'icontains'],
            'slug': ['exact', 'contains', 'icontains'],

        }

    def filter_ids(self, queryset, name, value):
        items = [item.strip("'\" ") for item in value.strip('[]').split(',')]
        excludes = [i[1:] for i in items if i.startswith("-")]
        if len(excludes) > 0:
            return queryset.filter(~Q(id__in=excludes))
        elif len(items) > 0:
            return queryset.filter(id__in=items)
        else:
            return queryset

    def filter_tags(self, queryset, name, lst):
        items = [item.strip("'\" ") for item in lst.strip('[]').split(',')]
        excludes = [i[1:] for i in items if i.startswith("-")]
        if len(excludes) > 0:
            return queryset.filter(~Q(label__name__in=excludes))
        elif len(items) > 0:
            return queryset.filter(label__name__in=items)
        else:
            return queryset

    def filter_expired(self, queryset, name, value):
        ids = [item.id for item in queryset if item.is_expired == value]
        return queryset.filter(id__in=ids)

    def filter_type(self, queryset, name, lst):
        types = [item.strip("'\" ") for item in lst.strip('[]').split(',')]
        type_numbers = [CHOICES.get(typ, 0) for typ in types]
        return queryset.filter(type__in=type_numbers)

    def filter_company_ids(self, queryset, name, value):
        items = [item.strip("'\" ") for item in value.strip('[]').split(',')]
        excludes = [i[1:] for i in items if i.startswith("-")]
        if len(excludes) > 0:
            return queryset.filter(~Q(company__id__in=excludes))
        elif len(items) > 0:
            return queryset.filter(company__id__in=items)
        else:
            return queryset

    def filter_category_ids(self, queryset, name, value):
        items = [item.strip("'\" ") for item in value.strip('[]').split(',')]
        excludes = [i[1:] for i in items if i.startswith("-")]
        if len(excludes) > 0:
            return queryset.filter(~Q(category__id__in=excludes))
        elif len(items) > 0:
            return queryset.filter(category__id__in=items)
        else:
            return queryset


class CompanyFilter(filters.FilterSet):
    active = filters.BooleanFilter(field_name='available')
    id = filters.CharFilter(method='filter_ids')
    category__id = filters.CharFilter(method='filter_category_ids')

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'contains', 'icontains'],
            'english_name': ['exact', 'contains', 'icontains'],
            'category__name': ['exact', 'contains', 'icontains'],
            'category__english_name': ['exact', 'contains', 'icontains'],
            'slug': ['exact', 'contains', 'icontains'],
        }

    def filter_ids(self, queryset, name, value):
        items = [item.strip("'\" ") for item in value.strip('[]').split(',')]
        excludes = [i[1:] for i in items if i.startswith("-")]
        if len(excludes) > 0:
            return queryset.filter(~Q(id__in=excludes))
        elif len(items) > 0:
            return queryset.filter(id__in=items)
        else:
            return queryset

    def filter_category_ids(self, queryset, name, value):
        items = [item.strip("'\" ") for item in value.strip('[]').split(',')]
        excludes = [i[1:] for i in items if i.startswith("-")]
        if len(excludes) > 0:
            return queryset.filter(~Q(category__id__in=excludes))
        elif len(items) > 0:
            return queryset.filter(category__id__in=items)
        else:
            return queryset


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
        excludes = [i[1:] for i in items if i.startswith("-")]
        if len(excludes) > 0:
            return queryset.filter(~Q(id__in=excludes))
        elif len(items) > 0:
            return queryset.filter(id__in=items)
        else:
            return queryset
