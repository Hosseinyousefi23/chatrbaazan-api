import datetime
from django.core.mail import EmailMessage
from time import sleep

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import re

from django.db.models import Q

from emm.models import EmailLog


class Command(BaseCommand):
    def handle(self, *args, **options):
        allEmail = EmailLog.objects.filter(Q(status=3) | Q(status=2))
        if allEmail.count() == 0:
            print('Email List Empty')

        try:
            id_email_send = []
            for list in allEmail:
                message = EmailMessage(subject=list.title_email if list.title_email else 'چتر بازان',
                                       body=list.body,
                                       to=[list.user.email if list.user else list.email_address])
                message.content_subtype = 'html'
                message.send()
                id_email_send.append(list.id)
                print('id_email_send', str(id_email_send))
            EmailLog.objects.filter(id__in=id_email_send).update(status=1)
        except Exception as e:
            print('error', str(e))
