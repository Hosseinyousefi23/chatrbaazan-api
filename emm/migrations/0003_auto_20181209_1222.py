# Generated by Django 2.1.2 on 2018-12-09 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emm', '0002_auto_20181205_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillog',
            name='body',
            field=models.TextField(default=None, verbose_name='ایمیل'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emaillog',
            name='email',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='emm.EmailEMM', verbose_name='ایمیل'),
        ),
    ]
