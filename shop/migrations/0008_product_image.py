# Generated by Django 2.1.2 on 2018-11-28 07:53

import django.core.files.storage
from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20181128_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, max_length=500, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/chavoshipour/sites/chatrbaazan/chatrbaazan'), upload_to=shop.models.generate_filename_ProductPic, verbose_name='تصویر'),
        ),
    ]