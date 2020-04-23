from rest_framework import serializers

from shop.models import Product, Category, Company
from shop.static import FIELD_NAMES


class ClassField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            return eval(data.capitalize())
        except:
            raise serializers.ValidationError("class %s is not defined" % data.capitalize())


class IncludeQuerySeializer(serializers.Serializer):
    association = ClassField()
    attributes = serializers.ListField(child=serializers.CharField(), allow_empty=False)

    def __init__(self, instance=None, depth=0, **kwargs):
        super().__init__(instance, **kwargs)
        if depth <= 5:
            self.fields['include'] = IncludeQuerySeializer(many=True, required=False, depth=depth + 1)


class QuerySerializer(serializers.Serializer):
    attributes = serializers.ListField(child=serializers.CharField(), required=False)
    include = IncludeQuerySeializer(many=True, required=False)

    def __init__(self, instance=None, model_name=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.model_name = model_name


class DynamicQueryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, instance=None, model=None, fields=None, include=None, **kwargs):
        super().__init__(instance, **kwargs)
        if model:
            self.Meta.model = model
        self.model_name = self.Meta.model._meta.model_name
        if fields:
            self.Meta.fields = fields
        if include:
            for field_desc in include:
                model = field_desc['association']
                model_name = model._meta.model_name
                fields = field_desc.get('attributes', None)
                include = field_desc.get('include', None)
                if model_name in FIELD_NAMES[self.model_name]:
                    serializer = DynamicQueryResponseSerializer(model=model, fields=fields, include=include,
                                                                many=FIELD_NAMES[self.model_name][model_name][
                                                                    'iterable'])
                    self.fields[FIELD_NAMES[self.model_name][model_name]['name']] = serializer
                else:
                    raise serializers.ValidationError("model '%s' has no relation '%s'" % (self.model_name, model_name))


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
