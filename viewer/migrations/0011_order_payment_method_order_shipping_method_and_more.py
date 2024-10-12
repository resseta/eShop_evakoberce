# Generated by Django 5.1.1 on 2024-10-12 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0010_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_method',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_name',
            field=models.CharField(max_length=85),
        ),
    ]
