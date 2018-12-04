from django.db import models

# Create your models here.
from accounts.models import User
from shop.models import Product


# class CartSession(models.Model):
#     ip = models.CharField(max_length=150, verbose_name=u"Ip")
#     key = models.CharField(max_length=500, verbose_name=u"Key Session")
#     header = models.TextField(verbose_name="Header Request")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    STATUS = (
        (1, u"در حال انجام"),
        (3, u"موفق"),
        (4, u"لغو شده توسط کاربر"),
        (5, u"مشکل در درگاه پرداخت"),
    )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="cart_user",
                             verbose_name=u"کاربر")
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name=u"مبلغ")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name=u"مبلغ")
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1, verbose_name=u"وضعیت")
    # session = models.ForeignKey(CartSession, on_delete=models.CASCADE, related_name="cart_session",
    #                             verbose_name=u"جلسه")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name="cartItem_product", verbose_name=u"محصول")
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name=u"مبلغ")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name=u"مبلغ")
    cart = models.ForeignKey(Cart, models.CASCADE, related_name="cartItem_cart", verbose_name=u"سبد خرید")
    count = models.IntegerField(default=1, verbose_name=u"تعداد")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
