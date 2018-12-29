# Generated by Django 2.1.2 on 2018-12-24 12:59

import django.core.files.storage
from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_auto_20181224_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='file',
            field=models.FileField(blank=True, max_length=500, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/chavoshipour/sites/chatrbaazan/chatrbaazan'), upload_to=shop.models.generate_filename_fieldFileProduct, verbose_name='فایل'),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'محصول'), (2, 'اپ'), (3, 'همایش'), (4, 'کد تخفیف')], default=1, verbose_name='نوع'),
        ),
    ]