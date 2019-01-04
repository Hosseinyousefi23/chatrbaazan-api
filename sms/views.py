from _ast import Is
from datetime import datetime , timedelta
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins , generics , status
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
import random

from rest_framework.views import APIView

from shop.renderers import CustomJSONRenderer
from sms.models import SmsUser
from sms.serializers import SmsUserSerializer , validate_phone
from sms.services import send_verification_sms


class SmsView(mixins.CreateModelMixin ,
              generics.GenericAPIView):
    serializer_class = SmsUserSerializer
    permission_classes = (IsAuthenticated ,)
    queryset = SmsUser.objects.all()

    def post(self , request , format=None , *args , **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True
        code_verify = random.randint(1 , 3000) * 10
        request.data.update(status=2)
        request.data.update(user=request.user.pk if request.user and not request.user.is_anonymous else None)
        request.data.update(phone=request.POST.get('phone' , None))
        request.data.update(code_verify=code_verify)
        request.POST._mutable = mutable
        print('str data sms post' , str(request.data))
        validate_phone(request.POST.get('phone' , ''))
        smsUser = SmsUser.objects.filter(phone=request.POST.get('phone'))
        if smsUser.filter(status=1):
            return CustomJSONRenderer().render({'phone': 'A user is already this phone'} , status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if smsUser.filter(status=2).count() == 0:
            self.perform_create(serializer)
        else:
            code_verify = smsUser.filter(status=2).first().code_verify
        send_verification_sms(request.user , request , mobile=request.POST.get('phone') , verify_code=code_verify)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data , status=status.HTTP_201_CREATED , headers=headers)
        # return self.create(request, *args, **kwargs)

    def put(self , request , phone=None , format=None , *args , **kwargs):
        if phone is None:
            return CustomJSONRenderer().render400()
        validate_phone(phone)
        code_verify = request.POST.get('code_verify' , None)
        if code_verify is None:
            return CustomJSONRenderer().render({'code': 'required'} , status=400)
        smsUser = SmsUser.objects.filter(phone=phone).filter(status=2)
        if smsUser:
            smsUser = smsUser.first()
            if smsUser.active_at and smsUser.status == 1:
                return CustomJSONRenderer().render({'message': 'شماره همراه قبلا فعال شده است'} , status=401)
            if smsUser.code_verify == code_verify:
                SmsUser.objects.filter(pk=smsUser.pk).update(active_at=datetime.now() , status=1)
                return CustomJSONRenderer().render({'success': True} , status=200)
            else:
                return CustomJSONRenderer().render({'message': 'code not math'} , status=400)
        else:
            return CustomJSONRenderer().render404('sms' , '')


class ReSendSmsView(APIView):
    permission_classes = (IsAuthenticated ,)
    allowed_method = ('GET' ,)

    def get(self , request , phone='' , format=None , *args , **kwargs):
        validate_phone(phone)
        smsUser = SmsUser.objects.filter(phone=phone)
        if not smsUser:
            return CustomJSONRenderer().render404('Sms User' , '')

        smsUser = smsUser.first()
        now = datetime.now()
        if smsUser.active_at and smsUser.status == 1:
            return CustomJSONRenderer().render({'message': 'user is old active'} , status=400)
        time_app = smsUser.send_at + timedelta(minutes=5)

        if now.replace(tzinfo=None) > time_app.replace(tzinfo=None):
            code_verify = random.randint(1 , 3000) * 10
            send_verification_sms(request.user , request , mobile=phone , verify_code=code_verify)
            SmsUser.objects.filter(pk=smsUser.pk).update(code_verify=code_verify , send_at=datetime.now() ,
                                                         active_at=None)
            return CustomJSONRenderer().render({'success': True})
        else:
            return CustomJSONRenderer().render({'message': 'last time send code tl minutes 5 '} , status=400)
