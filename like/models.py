from django.db import models

# Create your models here.
from shop.models import Product, User


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    like = models.IntegerField(default=0, verbose_name=u"لایک")
    disslike = models.IntegerField(default=0, verbose_name=u"دیس لایک")
    session = models.CharField(max_length=350, verbose_name=u"جلسه", null=True, blank=True)
