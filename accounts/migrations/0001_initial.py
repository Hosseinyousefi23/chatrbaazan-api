# Generated by Django 2.1.2 on 2018-11-28 07:39

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('mobile', models.CharField(blank=True, db_index=True, max_length=11, null=True, unique=True, validators=[accounts.models.validate_mobile], verbose_name='mobile')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('email',)***REMOVED***,
        ),
    ]