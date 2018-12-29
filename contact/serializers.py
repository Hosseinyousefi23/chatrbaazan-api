# Code Here
from rest_framework import serializers

from contact.models import Contact
from shop.models import validate_mobile, validate_phone


class ContactSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=300, required=True)
    family = serializers.CharField(max_length=350, required=False)
    phone = serializers.CharField(max_length=14, required=False, validators=[validate_phone])
    mobile = serializers.CharField(max_length=14, required=False, validators=[validate_mobile])
    email = serializers.CharField(max_length=50, required=True)
    contact = serializers.CharField(max_length=1000, required=True)

    class Meta:
        model = Contact
        fields = ('name', 'family', 'phone', 'mobile', 'email', 'contact')
