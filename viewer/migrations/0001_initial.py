# Generated by Django 5.1.1 on 2024-09-19 09:27

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
                ('name', models.CharField(max_length=20)),
                ('year_of_manufacture', models.DateField()),
                ('code', models.DateField(blank=True, null=True)),
                ('short_description', models.TextField()),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField(verbose_name='Cena')),
                ('availability', models.BooleanField(default=False)),
                ('img', models.ImageField(default='no_image.png', upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarMat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('year_of_manufacture', models.DateField()),
                ('body', models.CharField(blank=True, max_length=12, null=True)),
                ('code', models.DateField(blank=True, null=True)),
                ('short_description', models.TextField()),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField(verbose_name='Cena')),
                ('availability', models.BooleanField(default=False)),
                ('img', models.ImageField(default='no_image.png', upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='ColorOfMat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ColorOfTrim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryMain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('name_accessories', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.accessories')),
                ('name_car_mat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.carmat')),
            ],
        ),
        migrations.AddField(
            model_name='carmat',
            name='color_of_mat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.colorofmat'),
        ),
        migrations.AddField(
            model_name='carmat',
            name='color_of_trim',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.coloroftrim'),
        ),
        migrations.CreateModel(
            name='ModelName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('brand_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.brand')),
            ],
        ),
        migrations.AddField(
            model_name='carmat',
            name='model_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.modelname'),
        ),
        migrations.AddField(
            model_name='accessories',
            name='model_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.modelname'),
        ),
    ]
