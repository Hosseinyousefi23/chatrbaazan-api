from django.db import models


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name=u"نام")
    family = models.CharField(max_length=350, null=True, blank=True, verbose_name=u"فامیلی")
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name=u"تلفن")
    mobile = models.CharField(max_length=13, null=True, blank=True, verbose_name=u"همراه")
    email = models.CharField(max_length=50, null=False, blank=False, verbose_name=u"ایمیل")
    contact = models.TextField(null=False, blank=False, verbose_name=u"متن")

    class Meta:
        verbose_name = u"تماس با ما"
        verbose_name_plural = u"تماس با ما"

    def __str__(self):
        return str(self.name) + ' <' + str(self.email) + '>'
