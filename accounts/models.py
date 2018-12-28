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


def validate_mobile(mobile):
    if mobile:
        if not re.match('^09[\d]{9***REMOVED***$', mobile):
            raise ValidationError(u'شماره موبایل صحیح نمی باشد.')


# Create your models here.
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
    address = models.TextField(null=True, blank=True, default=None, verbose_name=u"آدرس")
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        unique_together = ('email',)
        verbose_name = u"کاربران"
        verbose_name_plural = u"کاربران"

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



class UserSendCode(models.Model):
    STATUS = (
        (1, u"تایید شده"),
        (2, u"در انتظار تایید"),
        (3, u"لغو شده")
    )
    user = models.ForeignKey(User, related_name="user_send_code_user", blank=False, null=False,
                             on_delete=models.CASCADE, verbose_name=u"کاربر")
    code = models.CharField(max_length=300, blank=False, null=False, verbose_name=u"کد تخفیف")
    explanation = models.TextField(blank=True, null=True, verbose_name=u"توضیح")
    expiration_date = models.DateTimeField(blank=True, null=True, verbose_name=u"تاریخ انقضاء")
    chatrbazi = models.CharField(max_length=150, default=None, null=True, blank=True, verbose_name=u"مقدار چتر بازی")
    status = models.PositiveSmallIntegerField(choices=STATUS, default=2, verbose_name=u"وضعیت")

    class Meta:
        verbose_name = u"کدهای ارسال کاربران"
        verbose_name_plural = u"کدهای ارسال کاربران"
