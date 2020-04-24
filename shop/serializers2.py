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


class BaseQuerySerializer(serializers.Serializer):
    attributes = serializers.ListField(child=serializers.CharField(), allow_empty=False)
    where = serializers.JSONField(required=False)

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

    def __init__(self, instance=None, model=None, q=None, **kwargs):
        super().__init__(instance, **kwargs)
        if model:
            self.Meta.model = model
        self.model_name = self.Meta.model._meta.model_name
        self.q = q
        if self.q:
            fields = q.get('attributes', None)
            include = q.get('include', None)
            if fields:
                self.Meta.fields = fields
            if include:
                for field_desc in include:
                    model = field_desc['association']
                    where = field_desc.get('where', None)
                    model_name = model._meta.model_name
                    if model_name in FIELD_NAMES[self.model_name]:
                        serializer = DynamicQueryResponseSerializer(model=model, q=field_desc,
                                                                    many=FIELD_NAMES[self.model_name][model_name][
                                                                        'iterable'])
                        self.fields[FIELD_NAMES[self.model_name][model_name]['name']] = serializer
                    else:
                        raise serializers.ValidationError(
                            "model '%s' has no relation '%s'" % (self.model_name, model_name))


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
