# Generated by Django 2.1.2 on 2018-11-26 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20181126_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='link',
            field=models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='لینک'),
        ),
    ]