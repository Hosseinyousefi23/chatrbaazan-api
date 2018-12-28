from datetime import datetime
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import random

from shop.renderers import CustomJSONRenderer
from sms.models import SmsUser
from sms.serializers import SmsUserSerializer, validate_phone
from sms.services import send_verification_sms


class SmsView(mixins.CreateModelMixin,
              generics.GenericAPIView):
    serializer_class = SmsUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = SmsUser.objects.all()

    def post(self, request, format=None, *args, **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True
        code_verify = random.randint(1, 3000) * 10
        request.data.update(status=2)
        request.data.update(user=request.user.pk if request.user and not request.user.is_anonymous else None)
        request.data.update(phone=request.POST.get('phone', None))
        request.data.update(code_verify=code_verify)
        request.POST._mutable = mutable
        print('str data sms post', str(request.data))
        validate_phone(request.POST.get('phone', ''))
        smsUser = SmsUser.objects.filter(phone=request.POST.get('phone'))
        if smsUser:
            return CustomJSONRenderer().render({'phone': 'A user is already this phone'}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_verification_sms(request.user, request, mobile=request.POST.get('phone'), verify_code=code_verify)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)

    def put(self, request, phone=None, format=None, *args, **kwargs):
        if phone is None:
            return CustomJSONRenderer().render400()
        validate_phone(phone)
        code_verify = request.POST.get('code_verify', None)
        if code_verify is None:
            return CustomJSONRenderer().render({'code': 'required'}, status=400)
        smsUser = SmsUser.objects.filter(phone=phone)
        if smsUser:
            smsUser = smsUser.first()
            if smsUser.active_at:
                return CustomJSONRenderer().render({'message': 'شماره همراه قبلا فعال شده است'}, status=401)
            if smsUser.code_verify == code_verify:
                SmsUser.objects.filter(pk=smsUser.pk).update(active_at=datetime.now(), status=1)
                return CustomJSONRenderer().render({'success': True}, status=200)
            else:
                return CustomJSONRenderer().render({'message': 'code not math'}, status=400)
        else:
            return CustomJSONRenderer().render404()
