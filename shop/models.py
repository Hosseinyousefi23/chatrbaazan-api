from platform import release

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.expressions import Combinable


class City(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    english_name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام (انگلیسی)")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")


class Category(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    english_name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام (انگلیسی)")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")


class Company(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    category = models.ForeignKey(Category, related_name="category_company", null=True, default=None, blank=True,
                                 verbose_name=u"دسته بندی", on_delete=models.CASCADE)
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")


class ProductLabel(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name=u"نام")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")


class Product(models.Model):
    PRIORITY = (
        (1, u"فعال"),
        (3, u"غیرفعال"),
        (4, u"سطح پایین"),
        (5, u"سطح معمولی"),
        (6, u"سطح بالا"),
        (7, u"سطح فوق بالا"),
    )
    name = models.CharField(max_length=300, blank=False, null=False, verbose_name=u"نام")
    category = models.ManyToManyField(Category, related_name="product_category", verbose_name=u"دسته بندی")
    company = models.ManyToManyField(Company, related_name="product_company", verbose_name=u"کمپانی")
    label = models.ManyToManyField(ProductLabel, related_name="product_label", verbose_name=u"تگ")
    priority = models.PositiveSmallIntegerField(choices=PRIORITY, default=1, verbose_name=u"اولویت", )
    explanation = models.TextField(blank=True, null=True, verbose_name=u"توضیح")
    expiration_date = models.DateTimeField(blank=True, null=True, verbose_name=u"تاریخ انقضاء")
    city = models.ManyToManyField(City, related_name="product_city", verbose_name=u"شهر")
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=u"مبلغ")
    is_free = models.BooleanField(default=False, verbose_name=u"رایگان")
    english_name = models.CharField(max_length=500, blank=True, null=True, verbose_name=u"نام کالا به انگلیسی‌")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"محصولات"
        verbose_name_plural = u"محصولات"


class Banner(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False, verbose_name=u"عنوان")
    image = models.ImageField(upload_to='banner/', default='banner/None/no-img.jpg', verbose_name=u"تصویر")
    category = models.ForeignKey(Category, related_name="banner_category", blank=True, null=True,
                                 verbose_name=u"دسته بندی", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="banner_product", blank=True, null=True,
                                verbose_name=u"محصول")
    is_slider = models.BooleanField(default=False, verbose_name=u"قرار دادن در اسلایدر")


class Contact(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name=u"نام")
    family = models.CharField(max_length=350, null=True, blank=True, verbose_name=u"فامیلی")
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name=u"تلفن")
    mobile = models.CharField(max_length=13, null=True, blank=True, verbose_name=u"همراه")
    email = models.CharField(max_length=50, null=False, blank=False, verbose_name=u"ایمیل")
    contact = models.TextField(null=False, blank=False, verbose_name=u"متن")

    class Transaction(models.Model):
        STATUS = (
            (0, u'موفق'),
            (1, u'خطا در پرداخت'),
            (2, u'کنسل شده'),
            (3, u'در حال پرداخت')
        )
        product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transaction_product",
                                    verbose_name=u"کالا")
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_user", verbose_name=u"کاربر")
        status = models.PositiveSmallIntegerField(choices=STATUS, verbose_name=u"وضعیت", default=3)
        price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=u"مبلغ")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

    class UserProduct(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="userProduct_product",
                                    verbose_name=u"محصول")
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userProduct_user", verbose_name=u"کاربر")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
