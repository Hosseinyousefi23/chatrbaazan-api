# Generated by Django 2.1.2 on 2018-12-04 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(blank=True, max_length=200, unique=True, verbose_name='آدرس'),
        ),
    ]