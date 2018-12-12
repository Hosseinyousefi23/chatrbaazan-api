from rest_framework import serializers

from sms.models import SmsUser


class SmsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsUser
        fields = '__all__'
