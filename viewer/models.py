from django.db import models

# Create your models here.
from django.db.models import *


class ColorOfTrim(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    def __repr__(self):
        return f"ColorOfTrim(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class ColorOfMat(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    def __repr__(self):
        return f"ColorOfMat(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Category(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    def __repr__(self):
        return f"Brand(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Subcategory(Model):
    name = CharField(max_length=50, null=False, blank=False, unique=True)
    category  = ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __repr__(self):
        return f"ModelName(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Body(Model):
    name = CharField(max_length=20, null=True, blank=True, unique=True)

    def __repr__(self):
        return f"Body(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Product(Model):
    name = CharField(max_length=60, null=False, blank=False)
    subcategory = ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')
    year_of_manufacture = CharField(max_length=20, null=False, blank=False)
    body = ForeignKey(Body, null=True, blank=True, on_delete=CASCADE)
    code = CharField(max_length=20, null=True, blank=True)
    short_description = TextField()
    description = TextField()
    quantity = IntegerField()
    price = FloatField(verbose_name='Cena', null=False, blank=False)
    availability = BooleanField(default=False)
    image = ImageField(default='no_image.png', upload_to='products/')

    def __repr__(self):
        return (f"CarMat(name={self.name} brand_name={self.brand_name} model_name={self.model_name} "
                f"year_of_manufacture={self.year_of_manufacture} body={self.body})")

    def __str__(self):
        return f"{self.name}"


class Accessories(Model):
    name = CharField(max_length=50, null=False, blank=False)
    model_name = ForeignKey(Subcategory, null=True, blank=False, on_delete=CASCADE)
    year_of_manufacture = CharField(max_length=20, null=False, blank=False)
    code = CharField(max_length=20, null=True, blank=True)
    short_description = TextField()
    description = TextField()
    quantity = IntegerField()
    price = FloatField(verbose_name='Cena', null=False, blank=False)
    availability = BooleanField(default=False)
    img = ImageField(default='no_image.png', upload_to='images')

    def __repr__(self):
        return f"Accessories(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class CategoryMain(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)
    name_car_mat = ForeignKey(Product, null=True, blank=False, on_delete=CASCADE)
    name_accessories = ForeignKey(Accessories, null=True, blank=False, on_delete=CASCADE)
