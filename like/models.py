from django.db import models

# Create your models here.
from shop.models import Product, User


class Like(models.Model):
    LIKECHOICES = (
        (1, 'Like'),
        (2, 'DissLike')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    like = models.PositiveSmallIntegerField(choices=LIKECHOICES, default=1, verbose_name=u"لایک")
    session = models.CharField(max_length=350, verbose_name=u"جلسه", null=True, blank=True)

    def __str__(self):
        return str(self.product) + ' ' + str(self.get_like_display())
