import datetime
from django.core.mail import EmailMessage
from time import sleep

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import re

from django.db.models import Q

from sms.models import SmsLog

from django.utils.html import strip_tags
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        allSms = SmsLog.objects.filter(Q(status=3) | Q(status=2))
        if allSms.count() == 0:
            print('Sms List Empty')

        try:
            id_send_sms = []
            url_post = 'http://smspanel.Trez.ir/SendMessageWithPost.ashx'
            for key in allSms:
                params = {
                    'UserName': 'Vahidsaadat1',
                    'Password': 'vma#123',
                    'PhoneNumber': '50002237242500',
                    'MessageBody': strip_tags(key.sms.text),
                    'RecNumber': key.mobile,
                    'Smsclass': '1',
                }

                r = requests.post(url_post, data=params)
                print(r.url)
                print(r.status_code)
                print(r.text)
                if int(r.status_code) > 1000:
                    id_send_sms.append(key.id)
                print('id_email_send', str(id_send_sms))
            SmsLog.objects.filter(id__in=id_send_sms).update(status=1)

        except Exception as e:
            print('error', str(e))
