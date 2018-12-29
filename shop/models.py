from platform import release

import itertools

from datetime import date
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.files.storage import FileSystemStorage
from django.core.mail.message import EmailMessage
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.utils.translation import gettext as _

# Create your models here.
from django.db.models.expressions import Combinable
import re
import os

from rest_framework.exceptions import ValidationError
from social_core.utils import slugify

from accounts.models import User
from chatrbaazan.settings import BASE_DIR

fs = FileSystemStorage(location=BASE_DIR)


def generate_filename_bannerPic(instance, filename):
    if not instance.id:
        instance.id = date.today().year
    return os.path.join(u"UpLoadedFiles", "Banner", str(instance.id), (filename))


def generate_filename_ProductPic(instance, filename):
    if not instance.id:
        instance.id = date.today().year
    return os.path.join(u"UpLoadedFiles", "Product", str(instance.id), (filename))


def generate_filename_company(instance, filename):
    if not instance.id:
        instance.id = date.today().year
    return os.path.join(u"UpLoadedFiles", "Company", str(instance.id), (filename))


def generate_filename_ProductPic(instance, filename):
    if not instance.id:
        instance.id = date.today().year
    return os.path.join(u"UpLoadedFiles", "Product", str(instance.id), (filename))


def generate_filename_fieldFileProduct(instance, filename):
    if not instance.id:
        instance.id = date.today().year
    return os.path.join(u"UpLoadedFiles", "Product", "File", str(instance.id), (filename))


def validate_mobile(mobile):
    if mobile:
        if not re.match('^[0][9][1][0-9]{8,8***REMOVED***$', str(mobile)):
            raise ValidationError({'message': u'not Invalid Mobile'***REMOVED***)


def validate_phone(phone):
    if phone:
        if not re.match('^[0][9][1][0-9]{8,8***REMOVED***$', str(phone)):
            raise ValidationError(u'not Invalid Phone')


class City(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    english_name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام (انگلیسی)")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")

    def __str__(self):
        return self.name or ''

    class Meta:
        verbose_name = u'شهر'
        verbose_name_plural = u'شهر'


class Category(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    english_name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام (انگلیسی)")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")
    slug = models.CharField(max_length=200, unique=True, blank=True, verbose_name=u"آدرس")

    def __str__(self):
        return self.name or ''

    def save(self, **kwargs):
        super(Category, self).save(**kwargs)
        if not self.slug:
            self.slug = orig = str((self.name)).replace(' ', '-')
            for x in itertools.count(1):
                if not Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    break
                self.slug = '%s-%d' % (orig, x)
            self.save()
            print(str(self.slug))

    class Meta:
        verbose_name = u'دسته بندی'
        verbose_name_plural = u'دسته بندی'


class Company(models.Model):
    PRIORITY = (
        (1, u"فعال"),
        (3, u"غیرفعال"),
        (4, u"سطح پایین"),
        (5, u"سطح معمولی"),
        (6, u"سطح بالا"),
        (7, u"سطح فوق بالا"),
    )
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    category = models.ForeignKey(Category, related_name="category_company", null=True, default=None, blank=True,
                                 verbose_name=u"دسته بندی", on_delete=models.CASCADE)
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")
    slug = models.CharField(max_length=200, unique=True, blank=True, verbose_name=u"آدرس")
    image = models.ImageField(storage=fs, upload_to=generate_filename_company, verbose_name=u"تصویر",
                              blank=True, null=True, max_length=500)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY, default=4, verbose_name=u"اولویت")
    description = models.TextField(verbose_name=u"توضیحات", blank=True, null=True, default=None)
    link = models.CharField(max_length=500, null=True, blank=True, default=None, verbose_name=u'لینک')

    def __str__(self):
        return self.name or ''

    def save(self, **kwargs):
        super(Company, self).save(**kwargs)
        if not self.slug:
            self.slug = orig = str((self.name)).replace(' ', '-')
            for x in itertools.count(1):
                if not Company.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    break
                self.slug = '%s-%d' % (orig, x)
            self.save()
            print(str(self.slug))

    class Meta:
        verbose_name = u'شرکت'
        verbose_name_plural = u'شرکت'


class ProductLabel(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name=u"نام")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")

    def __str__(self):
        return self.name or ''

    class Meta:
        verbose_name = u'تگ ها'
        verbose_name_plural = u'تگ ها'


class Discount(models.Model):
    discount = models.CharField(max_length=500, verbose_name=u"کد تخفیف")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")

    def __str__(self):
        return self.discount or ''

    class Meta:
        verbose_name = u"کدتخفیف"
        verbose_name_plural = u"کد تخفیف"


class ProductGallery(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name=u"نام فایل")
    image = models.ImageField(storage=fs, upload_to=generate_filename_ProductPic, verbose_name=u"تصویر",
                              blank=True, null=True, max_length=500)

    # def save(self, *args, **kwargs):
    #     super(ProductGallery, self).save(*args, **kwargs)
    # self.title = 's'
    # self.save()

    def __str__(self):
        return self.title if self.title else 'Image {***REMOVED***'.format(self.pk)

    class Meta:
        verbose_name = u'گالری'
        verbose_name_plural = u'گالری'


class Product(models.Model):
    PRIORITY = (
        (1, u"فعال"),
        (3, u"غیرفعال"),
        (4, u"سطح پایین"),
        (5, u"سطح معمولی"),
        (6, u"سطح بالا"),
        (7, u"سطح فوق بالا"),
    )
    TYPE = (
        (1, u"محصول"),
        (2, u"اپ"),
        (3, u"همایش"),
        (4, u"کد تخفیف"),
    )
    name = models.CharField(max_length=300, blank=False, null=False, verbose_name=u"نام")
    category = models.ManyToManyField(Category, related_name="product_category", verbose_name=u"دسته بندی")
    company = models.ManyToManyField(Company, related_name="product_company", verbose_name=u"کمپانی", null=True,
                                     blank=True)
    # discount = models.ForeignKey(Discount, null=True, blank=True, verbose_name=u"کد تخفیف", on_delete=models.CASCADE)
    discount_code = models.CharField(max_length=300, null=True, blank=True, verbose_name=u"کد تخفیف")
    label = models.ManyToManyField(ProductLabel, related_name="product_label", verbose_name=u"تگ", null=True,
                                   blank=True)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY, default=1, verbose_name=u"اولویت")
    explanation = models.TextField(blank=True, null=True, verbose_name=u"توضیح")
    expiration_date = models.DateTimeField(blank=True, null=True, verbose_name=u"تاریخ انقضاء")
    city = models.ManyToManyField(City, related_name="product_city", verbose_name=u"شهر", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=u"مبلغ")
    chatrbazi = models.IntegerField(default=0, null=True, blank=True, verbose_name=u"مقدار چتر بازی")
    is_free = models.BooleanField(default=False, verbose_name=u"رایگان")
    english_name = models.CharField(max_length=500, blank=True, null=True, verbose_name=u"نام کالا به انگلیسی‌")
    image = models.ImageField(storage=fs, upload_to=generate_filename_ProductPic, verbose_name=u"تصویر",
                              blank=True, null=True, max_length=500)
    gallery = models.ManyToManyField(ProductGallery, related_name="product_gallery", null=True, blank=True,
                                     verbose_name=u"گالری")
    slug = models.CharField(max_length=200, unique=True, blank=True, verbose_name=u"آدرس")
    failure = models.IntegerField(null=True, blank=True, default=0, verbose_name=u"تعداد گزارش خرابی")
    click = models.IntegerField(null=True, blank=True, default=0, verbose_name=u"تعداد لایک")
    link = models.CharField(max_length=350, blank=True, null=True, default=None, verbose_name=u'لینک')
    file = models.FileField(storage=fs, upload_to=generate_filename_fieldFileProduct,
                            verbose_name=u"فایل", blank=True, null=True, max_length=500)
    type = models.PositiveSmallIntegerField(choices=TYPE, default=1, verbose_name=u"نوع")
    count = models.IntegerField(default=0, verbose_name=u"تعداد")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"محصول"
        verbose_name_plural = u"محصولات"

    def save(self, **kwargs):
        super(Product, self).save(**kwargs)
        if not self.slug:
            self.slug = orig = str((self.name)).replace(' ', '-')
            for x in itertools.count(1):
                if not Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    break
                self.slug = '%s-%d' % (orig, x)
            self.save()
            print('slug product write', str(self.slug))

    def __str__(self):
        return str(self.name)


class Failure(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='failure_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='failure_user', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name=u"Description")
    uuid = models.CharField(max_length=350, verbose_name=u"uuid")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        if int(self.product.failure) >= 10:
            message = EmailMessage(subject='چتربازان گزارش خرابی محصول',
                                   body=get_template('email/failure.html').render(
                                       {
                                           'product': self.product,
                                       ***REMOVED***),
                                   to=[user.email for user in User.objects.filter(is_admin=True)])
            # message.content_subtype = 'html'
            try:
                message.send()
            except Exception as e:
                raise str(e)
        super(Failure, self).save(**kwargs)


class Banner(models.Model):
    LOCATION = (
        (3, u'Top'),
        (2, u'Middle'),
        (1, u'Down'),
        (0, u'None'),
    )
    title = models.CharField(max_length=150, null=False, blank=False, verbose_name=u"عنوان")
    image = models.ImageField(storage=fs, upload_to=generate_filename_bannerPic, verbose_name=u"تصویر",
                              blank=True, null=True, max_length=500)
    category = models.ForeignKey(Category, related_name="banner_category", blank=True, null=True,
                                 verbose_name=u"دسته بندی", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="banner_product", blank=True, null=True,
                                verbose_name=u"محصول")
    is_slider = models.BooleanField(default=False, verbose_name=u"قرار دادن در اسلایدر")
    link = models.CharField(max_length=500, default=None, null=True, blank=True, verbose_name=u"لینک")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")
    location = models.PositiveSmallIntegerField(choices=LOCATION, default=3, blank=True, null=True)

    class Meta:
        verbose_name = u"بنر"
        verbose_name_plural = u"بنر"

    def __str__(self):
        return self.title or ''


class Transaction(models.Model):
    STATUS = (
        (0, u'موفق'),
        (1, u'خطا در پرداخت'),
        (2, u'کنسل شده'),
        (3, u'در حال پرداخت')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transaction_product",
                                verbose_name=u"کالا")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_user",
                             verbose_name=u"کاربر")
    status = models.PositiveSmallIntegerField(choices=STATUS, verbose_name=u"وضعیت", default=3)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=u"مبلغ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"پرداخت"
        verbose_name_plural = u"پرداخت"

    def __unicode__(self):
        return 'پرداخت {***REMOVED***'.format(self.title)


class UserProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="userProduct_product",
                                verbose_name=u"محصول")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userProduct_user",
                             verbose_name=u"کاربر")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product) + ' User: ' + str(self.user)

    class Meta:
        verbose_name = u"محصولات خریداری شده"
        verbose_name_plural = u"محصولات خریداری شده"


class ShopSetting(models.Model):
    instagram = models.CharField(max_length=350, blank=True, default="#", verbose_name=u"اینستاگرام")
    telegram = models.CharField(max_length=350, blank=True, default="#", verbose_name=u"تلگرام")
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"تلفن")
    email = models.CharField(max_length=350, blank=True, null=True, verbose_name=u"ایمیل")
    map_x = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"نقطه ی x در نقشه")
    map_y = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"نقطه ی y در نقشه")
    enable = models.BooleanField(default=False, verbose_name=u'فعال')
    address = models.TextField(blank=True, null=True, verbose_name=u"آدرس فروشگاه")

    class Meta:
        verbose_name = u'تنظمیات فروشگاه'
        verbose_name_plural = u'تنظیمات فروشگاه'

    def __str__(self):
        return str(self.telegram)
