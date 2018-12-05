# Code Here
from rest_framework import serializers

from .models import About
from shop.models import validate_mobile, validate_phone


class AboutSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = About
        fields = ('text', 'image')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        else:
            pass
