from django.db import models

# Create your models here.
from accounts.models import User
from shop.models import Category, fs
from datetime import date
import os


def generate_filename_phone(instance, filename):
    if not instance.id:
        instance.id = date.today().year
    return os.path.join(u"UpLoadedFiles", "SmsFile", str(instance.id), (filename))


class Sms(models.Model):
    title = models.CharField(max_length=350, blank=False, null=False, verbose_name=u"عنوان")
    text = models.TextField(verbose_name=u"متن پیامک", blank=False, null=False)
    category = models.ManyToManyField(Category, related_name="sms_category", verbose_name=u"دسته بندی")
    phone = models.FileField(storage=fs, upload_to=generate_filename_phone, verbose_name=u"فایل",
                             blank=True, null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SmsUser(models.Model):
    STATUS = (
        (1, u"فعال"),
        (2, u"غیرفعال")
    )
    user = models.ForeignKey(User, related_name=u"کاربر", blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, verbose_name=u"شماره همراه", null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=2, verbose_name=u"وضعیت")
    code_verify = models.CharField(max_length=350, blank=False, null=False, verbose_name=u"کدتایید شده")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active_at = models.DateTimeField(blank=False, null=False, verbose_name=u"زمان تایید شده")
    send_at = models.DateTimeField(auto_now_add=True, verbose_name=u"زمان ارسال کد")


# class SmsLog(models.Model):
#     sms