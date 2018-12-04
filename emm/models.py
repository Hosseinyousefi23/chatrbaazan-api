from django.core.mail import EmailMessage

from django.db import models
from django.template import Context
from django.template.loader import get_template

from accounts.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# Create your models here.
class EmailEMM(models.Model):
    user = models.ManyToManyField(User, related_name="emailEmm_user", verbose_name=u"کاربر")
    text = models.TextField(verbose_name=u"متن ایمیل", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EmailLog(models.Model):
    STATUS = (
        (1, u"ارسال شده"),
        (2, u"مشکل در ارسال"),
        (3, u"در حال ارسال")
    )
    user = models.ForeignKey(User, related_name="emailLog_user", verbose_name=u"کاربر", on_delete=models.CASCADE)
    email = models.TextField(blank=False, null=False, verbose_name=u"ایمیل")
    status = models.PositiveSmallIntegerField(choices=STATUS, default=3, blank=False, null=False, verbose_name=u"وضعیت")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
