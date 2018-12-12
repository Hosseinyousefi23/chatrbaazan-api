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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"سرویس اشتراک پیامک"
        verbose_name_plural = u"سرویس اشتراک پیامک"


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
    active_at = models.DateTimeField(blank=True, null=True, verbose_name=u"زمان تایید شده")
    send_at = models.DateTimeField(auto_now_add=True, verbose_name=u"زمان ارسال کد")

    def __str__(self):
        return self.user.mobile if self.user else self.phone

    class Meta:
        verbose_name = u"اشتراک پیامک کاربر"
        verbose_name_plural = u"اشتراک پیامک کاربر"


class SmsLog(models.Model):
    STATUS = (
        (1, "موفق"),
        (2, "نا موفق"),
        (3, "در حال ارسال")
    )
    sms = models.ForeignKey(Sms, related_name="smslog_sms", on_delete=models.CASCADE, verbose_name=u"sms")
    sms_user = models.ForeignKey(SmsUser, related_name="smsmlog_smsuser", on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=3, verbose_name=u"وضعیت")

    class Meta:
        verbose_name = u"گزارش دهی سرویس پیامک"
        verbose_name_plural = u"گزارش دهی سرویس پیامک"

    def __str__(self):
        return str(self.sms) + ' User: ' + str(self.sms_user)
