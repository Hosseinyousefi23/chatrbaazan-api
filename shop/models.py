from platform import release

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.expressions import Combinable


class City(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    english_name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام (انگلیسی)")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")
    parent = models.ForeignKey("self", related_name="city", verbose_name=u"Parent", default=None, blank=True,
                               null=True)


class Category(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    english_name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام (انگلیسی)")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")
    parent = models.ForeignKey("self", related_name="category", verbose_name=u"Parent", default=None, blank=True,
                               null=True)


class Company(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    category = models.ForeignKey(Category, related_name="category_company", null=True, default=None, blank=True,
                                 verbose_name=u"دسته بندی")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")


class ProductLabel(models.Model):
    name = models.CharField()
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")


class ProductType(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام")
    english_name = models.CharField(max_length=150, blank=False, null=False, verbose_name=u"نام (انگلیسی)")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")


class Product(models.Model):
    name = models.CharField()
    category = models.ManyToManyField(Category)
    company = models.ManyToManyField(Company)
    label = models.ManyToManyField(ProductLabel)
    priority = models.AutoField(primary_key=False, verbose_name=u"اولویت")
    explanation = models.TextField(blank=True, null=True, verbose_name=u"توضیح")
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.ManyToManyField(City)
    is_dollar = models.BooleanField()
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_free = models.BooleanField()


class ProductProperty(models.Model):
    key = models.CharField()
    value = models.CharField()
    display = models.CharField()
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")
    product = models.ForeignKey(Product)


class Banner(models.Model):
    title = models.CharField()
    image = models.ImageField(upload_to='banner/', default='banner/None/no-img.jpg')
    category = models.ForeignKey(Category)
    product = models.ForeignKey(Product)


class Contact(models.Model):
    name = models.CharField()
    family = models.CharField()
    phone = models.CharField()
    mobile = models.CharField()
    email = models.CharField()
    contact = models.TextField()


class Transaction(models.Model):
    STATUS = (
        (0, u'موفق'),
        (1, u'خطا در پرداخت'),
        (2, u'کنسل شده'),
        (3, u'در حال پرداخت')
    )
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    status = models.PositiveSmallIntegerField(choices=STATUS)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserProduct(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
