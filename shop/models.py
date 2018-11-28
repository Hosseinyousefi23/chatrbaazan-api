from platform import release

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, PermissionsMixin, AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
from django.db.models.expressions import Combinable
import re
import os

from rest_framework.exceptions import ValidationError

from chatrbaazan.settings import BASE_DIR

fs = FileSystemStorage(location=BASE_DIR)


def generate_filename_participiantPic(instance, filename):
    return os.path.join(u"UpLoadedFiles", "Banner", str(instance.id), (filename))


def validate_mobile(mobile):
    if mobile:
        if not re.match('^09[\d]{9***REMOVED***$', mobile):
            raise ValidationError(u'شماره موبایل صحیح نمی باشد.')


class UserManager(BaseUserManager):
    def create_user(self, email, mobile, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            mobile=mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            mobile=None
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    mobile = models.CharField(max_length=11, blank=True, null=True,
                              verbose_name="mobile", db_index=True, validators=[validate_mobile], unique=True)
    first_name = models.CharField(max_length=150, verbose_name="first name")
    last_name = models.CharField(max_length=150, verbose_name="last name")

    objects = UserManager()

    # REQUIRED_FIELDS = ['email', 'mobile']
    USERNAME_FIELD = 'email'

    class Meta:
        unique_together = ('email',)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


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
    image = models.ImageField(storage=fs, upload_to=generate_filename_participiantPic, verbose_name=u"تصویر",
                              blank=True, null=True, max_length=500)
    category = models.ForeignKey(Category, related_name="banner_category", blank=True, null=True,
                                 verbose_name=u"دسته بندی", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="banner_product", blank=True, null=True,
                                verbose_name=u"محصول")
    is_slider = models.BooleanField(default=False, verbose_name=u"قرار دادن در اسلایدر")
    link = models.CharField(max_length=500, default=None, null=True, blank=True, verbose_name=u"لینک")
    available = models.BooleanField(default=True, blank=False, null=False, verbose_name=u"فعال")

    class Meta:
        verbose_name = u"بنر"
        verbose_name_plural = u"بنر"

    def __unicode__(self):
        return 'بنر {***REMOVED***'.format(self.title)


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
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=u"مبلغ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"بنر"
        verbose_name_plural = u"بنر"

    def __unicode__(self):
        return 'بنر {***REMOVED***'.format(self.title)

    class UserProduct(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="userProduct_product",
                                    verbose_name=u"محصول")
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userProduct_user",
                                 verbose_name=u"کاربر")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
