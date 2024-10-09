# Generated by Django 5.1.1 on 2024-10-08 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accessories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('year_of_manufacture', models.CharField(max_length=20)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('short_description', models.TextField()),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField(verbose_name='Cena')),
                ('availability', models.BooleanField(default=False)),
                ('img', models.ImageField(default='no_image.png', upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ColorOfMat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'colorofmat',
            },
        ),
        migrations.CreateModel(
            name='ColorOfTrim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'coloroftrim',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_status', models.CharField(default='Pending', max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='viewer.cart')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='viewer.paymentmethod')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('year_of_manufacture', models.CharField(max_length=20)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('short_description', models.TextField()),
                ('description', models.TextField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.FloatField(verbose_name='Cena')),
                ('availability', models.BooleanField(default=False)),
                ('image', models.ImageField(default='no_image.png', upload_to='products/')),
                ('body', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.body')),
                ('mat_color', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='viewer.colorofmat')),
                ('trim_color', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='viewer.coloroftrim')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryMain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('name_accessories', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.accessories')),
                ('name_car_mat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='viewer.cart')),
                ('mat_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='viewer.colorofmat')),
                ('trim_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='viewer.coloroftrim')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='viewer.product')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('telefon', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=60)),
                ('shipping_status', models.CharField(default='Pending', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='viewer.cart')),
                ('shipping_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='viewer.shippingmethod')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='viewer.category')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='viewer.subcategory'),
        ),
        migrations.AddField(
            model_name='accessories',
            name='model_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.subcategory'),
        ),
    ]
