# Code Here
from rest_framework import serializers

from contact.models import Contact
from emm.models import EmailRegister, validate_email
from shop.models import validate_mobile, validate_phone


class EmailRegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=300, required=True, validators=[validate_email])
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = EmailRegister
        fields = ('email', 'is_active')
