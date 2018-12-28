import re

from django.core.mail import EmailMessage

from django.db import models
from django.template import Context
from django.template.loader import get_template
from rest_framework.exceptions import ValidationError

from accounts.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


def validate_email(email):
    if email:
        if not re.match('^[^@]+@[^@]+\.[^@]+', str(email)):
            raise ValidationError(u'is not valid email')


class EmailRegister(models.Model):
    email = models.CharField(max_length=250, verbose_name=u"ایمیل")
    is_active = models.BooleanField(default=True, verbose_name=u"فعال")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.email)


class EmailEMM(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name=u"عنوان ایمیل")
    user = models.ManyToManyField(User, related_name="emailEmm_user", verbose_name=u"کاربر")
    email_register = models.ManyToManyField(EmailRegister, null=True, blank=True,
                                            related_name="emailEmm_email_register",
                                            verbose_name=u"انتخاب ایمیل از لیست خبرنامه")
    text = models.TextField(verbose_name=u"متن ایمیل", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"ایمیل مارکتینگ"
        verbose_name_plural = u"ایمیل مارکتینگ"

    def __str__(self):
        return str(self.title) if self.title else 'ایمیل ' + str(self.created_at)


class EmailLog(models.Model):
    STATUS = (
        (1, u"ارسال شده"),
        (2, u"مشکل در ارسال"),
        (3, u"در حال ارسال")
    )
    email = models.ForeignKey(EmailEMM, default=None, blank=True, null=True, verbose_name=u"ایمیل",
                              on_delete=models.SET_NULL)
    user = models.ForeignKey(User, related_name="emailLog_user", verbose_name=u"کاربر", on_delete=models.CASCADE)
    body = models.TextField(blank=False, null=False, verbose_name=u"ایمیل")
    status = models.PositiveSmallIntegerField(choices=STATUS, default=3, blank=False, null=False, verbose_name=u"وضعیت")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"ایمیل های داخل صف"
        verbose_name_plural = u"ایمیل های داخل صف"

    def __str__(self):
        return str(self.user)

# @receiver(post_save, sender=EmailEMM)
# def send_user_data_when_created_by_admin(sender, instance, created=True, raw=True, *args, **kwargs):
#     print(str(sender))
#     if created and raw:
#         print('/// save Model After save Loge ///')
#
#         print('Inserted Mail Log ******')
#         # print(dir(instance))
#         # print(str(instance.user.))
#         try:
#
#             for user in instance.user.all():
#                 print('user', str(user))
#                 # first_name = instance.user.first_name
#                 # print('first name is', first_name)
#                 print(str(user))
#                 EmailLog.objects.create(
#                     user=user,
#                     email=get_template('email/emm.html').render(
#                         {
#                             'user': user,
#                             'text': instance.text
#                         }
#                     )
#                 )
#         except Exception as e:
#             print('error when insert data To Email Log', str(e))
