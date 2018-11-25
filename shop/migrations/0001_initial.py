# Generated by Django 2.1.2 on 2018-11-25 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shop.models


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
                ('mobile', models.CharField(blank=True, db_index=True, max_length=11, null=True, unique=True, validators=[shop.models.validate_mobile], verbose_name='mobile')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='عنوان')),
                ('image', models.ImageField(default='banner/None/no-img.jpg', upload_to='banner/', verbose_name='تصویر')),
                ('is_slider', models.BooleanField(default=False, verbose_name='قرار دادن در اسلایدر')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام')),
                ('english_name', models.CharField(max_length=150, verbose_name='نام (انگلیسی)')),
                ('available', models.BooleanField(default=True, verbose_name='فعال')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام')),
                ('english_name', models.CharField(max_length=150, verbose_name='نام (انگلیسی)')),
                ('available', models.BooleanField(default=True, verbose_name='فعال')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام')),
                ('available', models.BooleanField(default=True, verbose_name='فعال')),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_company', to='shop.Category', verbose_name='دسته بندی')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='نام')),
                ('family', models.CharField(blank=True, max_length=350, null=True, verbose_name='فامیلی')),
                ('phone', models.CharField(blank=True, max_length=13, null=True, verbose_name='تلفن')),
                ('mobile', models.CharField(blank=True, max_length=13, null=True, verbose_name='همراه')),
                ('email', models.CharField(max_length=50, verbose_name='ایمیل')),
                ('contact', models.TextField(verbose_name='متن')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='نام')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, 'فعال'), (3, 'غیرفعال'), (4, 'سطح پایین'), (5, 'سطح معمولی'), (6, 'سطح بالا'), (7, 'سطح فوق بالا')], default=1, verbose_name='اولویت')),
                ('explanation', models.TextField(blank=True, null=True, verbose_name='توضیح')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انقضاء')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='مبلغ')),
                ('is_free', models.BooleanField(default=False, verbose_name='رایگان')),
                ('english_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='نام کالا به انگلیسی\u200c')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(related_name='product_category', to='shop.Category', verbose_name='دسته بندی')),
                ('city', models.ManyToManyField(related_name='product_city', to='shop.City', verbose_name='شهر')),
                ('company', models.ManyToManyField(related_name='product_company', to='shop.Company', verbose_name='کمپانی')),
            ],
            options={
                'verbose_name': 'محصولات',
                'verbose_name_plural': 'محصولات',
            ***REMOVED***,
        ),
        migrations.CreateModel(
            name='ProductLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='نام')),
                ('available', models.BooleanField(default=True, verbose_name='فعال')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'موفق'), (1, 'خطا در پرداخت'), (2, 'کنسل شده'), (3, 'در حال پرداخت')], default=3, verbose_name='وضعیت')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='مبلغ')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_product', to='shop.Product', verbose_name='کالا')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_user', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='UserProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userProduct_product', to='shop.Product', verbose_name='محصول')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userProduct_user', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='label',
            field=models.ManyToManyField(related_name='product_label', to='shop.ProductLabel', verbose_name='تگ'),
        ),
        migrations.AddField(
            model_name='banner',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banner_category', to='shop.Category', verbose_name='دسته بندی'),
        ),
        migrations.AddField(
            model_name='banner',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banner_product', to='shop.Product', verbose_name='محصول'),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('email',)***REMOVED***,
        ),
    ]
