# Generated by Django 2.1.2 on 2018-12-22 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20181221_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='location',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Top'), (2, 'Middle'), (3, 'Down')], default=3, null=True),
        ),
    ]