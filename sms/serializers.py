import re
from builtins import BaseException

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from sms.models import SmsUser
from sms.services import send_verification_sms


def validate_phone(phone):
    if phone:
        if not re.match('^[0][9][1][0-9]{8,8***REMOVED***$', str(phone)):
            raise ValidationError(u'not Invalid Phone')


class SmsUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=14, validators=[validate_phone])

    class Meta:
        model = SmsUser
        fields = ('user', 'phone', 'status', 'code_verify')
        extra_kwargs = {
            'code_verify': {'write_only': True***REMOVED***,
            'user': {'write_only': True***REMOVED***,
            'status': {'write_only': True***REMOVED***,
        ***REMOVED***
