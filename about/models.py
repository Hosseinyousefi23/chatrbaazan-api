from datetime import date

from django.db import models
import os

from shop.models import fs


def generate_filename_ProductPic(instance, filename):
    if not instance.id:
        instance.id = date.today().year
    return os.path.join(u"UpLoadedFiles", "About", str(instance.id), (filename))


# Create your models here.
class About(models.Model):
    STATUS = (
        (1, u"فعال"),
        (2, u"غیرفعال")
    )
    text = models.TextField(blank=False, null=False, verbose_name=u"متن")
    status = models.PositiveSmallIntegerField(choices=STATUS, default=2, verbose_name=u"وضعیت")
    image = models.ImageField(storage=fs, upload_to=generate_filename_ProductPic, verbose_name=u"تصویر",
                              blank=True, null=True, max_length=500)

    class Meta:
        verbose_name_plural = u"درباره ما"
        verbose_name = u"درباره ما"

    def __str__(self):
        return 'متن {} صفحه درباره ما'.format(self.pk)
