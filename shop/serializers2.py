from collections import OrderedDict

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Avg
from django.db.models.functions import Coalesce
from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from shop.models import Product, Category, Company
from shop.static import FIELD_NAMES, FILTERS


class FilteredListSerializer(ListSerializer):
    def __init__(self, *args, **kwargs):
        self.q = kwargs['child'].q
        self.model_name = kwargs['child'].model_name
        super().__init__(*args, **kwargs)

    def to_representation(self, data):
        data = data.all()
        meta_data = OrderedDict()
        try:
            where = self.q.get('where', {})
            order = self.q.get('order', None)
            page = self.q.get('page', None)
            page_size = self.q.get('page_size', 10)
            limit = self.q.get('limit', None)
            random = self.q.get('random', False)

            if 'expired' not in where:
                where['expired'] = False
            f = FILTERS[self.model_name](where, queryset=data)
            data = f.qs.all()
            if order:
                if self.model_name == 'company' and ('score' in order or '-score' in order):
                    data = data.annotate(score=Coalesce(Avg('scores__star'), 0))
                data = data.order_by(*order)
            if limit:
                data = self.slice(data, limit, random=random)
            cnt = self.type_count(data)
            if self.model_name == 'product' and cnt > 1:
                meta_data['count'] = cnt
                meta_data['code_count'] = self.type_count(data, 4)
                meta_data['offer_count'] = self.type_count(data, 3)
                meta_data['app_count'] = self.type_count(data, 2)
                meta_data['product_count'] = self.type_count(data, 1)

            if page:
                paginator = Paginator(data, page_size)
                meta_data['num_pages'] = paginator.num_pages
                meta_data['next'] = page + 1 if paginator.num_pages > page else None
                data = paginator.page(page)

            rep_data = super().to_representation(data)
            if type(rep_data) == list and len(rep_data) == 1:
                rep = rep_data[0]
            else:
                rep = {'data': rep_data}
            rep.update(meta_data)
            return rep
        except EmptyPage:
            rep = {'data': []}
            rep.update(meta_data)
            return rep
        except Exception as e:
            raise serializers.ValidationError(e)

    def type_count(self, data, product_type=None):
        qs = data.all()
        if product_type:
            return sum([1 for item in qs if item.type == product_type])
        else:
            return qs.count()

    @property
    def data(self):
        return super(ListSerializer, self).data

    def slice(self, data, limit, random=False):
        if random:
            return data.order_by('?')[:limit]
        else:
            return data[:limit]


class ClassField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            return eval(data.capitalize())
        except:
            raise serializers.ValidationError("class %s is not defined" % data.capitalize())


class BaseQuerySerializer(serializers.Serializer):
    attributes = serializers.ListField(child=serializers.CharField(), allow_empty=False)
    where = serializers.JSONField(required=False)
    order = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    limit = serializers.IntegerField(min_value=1, required=False)
    page = serializers.IntegerField(min_value=1, required=False)
    page_size = serializers.IntegerField(min_value=1, required=False)
    random = serializers.BooleanField(required=False, default=False)

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)

    def validate_where(self, value):
        if type(value) != dict:
            raise serializers.ValidationError("Should be a dictionary, but is of type '%s'" % type(value).__name__)
        return value


class IncludeQuerySeializer(BaseQuerySerializer):
    association = ClassField()

    def __init__(self, instance=None, queryset=None, depth=0, **kwargs):
        super().__init__(instance, **kwargs)
        if depth <= 5:
            self.fields['include'] = IncludeQuerySeializer(many=True, required=False, depth=depth + 1)

    def validate(self, data):
        for item in data['attributes']:
            if not hasattr(data['association'], item):
                raise serializers.ValidationError(
                    "Model '%s' has no attribute '%s'" % (data['association']._meta.model_name, item))
        return data


class QuerySerializer(BaseQuerySerializer):
    include = IncludeQuerySeializer(many=True, required=False)

    def __init__(self, instance=None, model=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.model = model

    def validate_attributes(self, value):
        for item in value:
            if not hasattr(self.model, item):
                raise serializers.ValidationError(
                    "Model '%s' has no attribute '%s'" % (self.model._meta.model_name, item))
        return value


class DynamicQueryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'
        list_serializer_class = FilteredListSerializer

    # def __new__(cls, *args, **kwargs):
    #     q = kwargs.get('q', None)
    #     if q:
    #         where = q.get('where', None)
    #         model = kwargs.get('model', None)
    #         instance = kwargs.get('instance', None)
    #         if where and model and instance:
    #             model_name = model._meta.model_name
    #             f = FILTERS[model_name](where, queryset=instance)
    #             new_instance = f.qs
    #             kwargs['instance'] = new_instance
    #     return super().__new__(cls, *args, **kwargs)

    def __init__(self, instance=None, model=None, q=None, **kwargs):
        self.q = q
        if model:
            self.Meta.model = self.meta_model = model
        self.model_name = self.Meta.model._meta.model_name
        super().__init__(**kwargs)

        if self.q:
            fields = q.get('attributes', None)
            include = q.get('include', None)
            if fields:
                self.Meta.fields = self.meta_fields = fields

            if include:
                for field_desc in include:
                    model = field_desc['association']
                    model_name = model._meta.model_name
                    if model_name in FIELD_NAMES[self.model_name]:
                        if model_name == 'category' and self.model_name == 'company':
                            serializer = DynamicQueryResponseSerializer(source='get_categories', model=model,
                                                                        q=field_desc,
                                                                        many=FIELD_NAMES[self.model_name][model_name][
                                                                            'iterable'])
                            # self.fields[
                            #     FIELD_NAMES[self.model_name][model_name]['name']] = ExtendedMethodField(
                            #     'get_categories', q=field_desc)
                            self.fields[FIELD_NAMES[self.model_name][model_name]['name']] = serializer
                        else:
                            serializer = DynamicQueryResponseSerializer(model=model, q=field_desc,
                                                                        many=FIELD_NAMES[self.model_name][model_name][
                                                                            'iterable'])
                            self.fields[FIELD_NAMES[self.model_name][model_name]['name']] = serializer
                    else:
                        raise serializers.ValidationError(
                            "model '%s' has no relation '%s'" % (self.model_name, model_name))

    def get_fields(self):
        self.Meta.model = self.meta_model
        self.Meta.fields = self.meta_fields
        self.Meta.depth = 1
        return super().get_fields()


class CouponSerializer(DynamicQueryResponseSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CompanySerializer(DynamicQueryResponseSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CategorySerializer(DynamicQueryResponseSerializer):
    class Meta:
        model = Category
        fields = '__all__'
