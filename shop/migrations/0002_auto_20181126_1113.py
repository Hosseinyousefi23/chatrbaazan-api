# Generated by Django 2.1.2 on 2018-11-26 11:13

import django.core.files.storage
from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, max_length=500, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/chavoshipour/sites/chatrbaazan/chatrbaazan'), upload_to=shop.models.generate_filename_bannerPic, verbose_name='تصویر'),
        ),
    ]