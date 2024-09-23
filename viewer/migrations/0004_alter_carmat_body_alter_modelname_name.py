# Generated by Django 5.1.1 on 2024-09-20 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0003_alter_accessories_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmat',
            name='body',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.body'),
        ),
        migrations.AlterField(
            model_name='modelname',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]