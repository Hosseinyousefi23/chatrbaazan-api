import datetime
from django.core.mail import EmailMessage
from time import sleep

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import re

from emm.models import EmailLog


class Command(BaseCommand):
    def handle(self, *args, **options):
        allEmail = EmailLog.objects.filter(status=3).filter(status=2)
        if allEmail.count() == 0:
            print('Email List Empty')

        try:
            for list in allEmail:
                message = EmailMessage(subject='چتر بازان' if list.email.title is None else list.email.title,
                                       body=list.body,
                                       to=[list.user.email])
                message.content_subtype = 'html'
                message.send()
        except Exception as e:
            print('error', str(e))
