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


class ModelName(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    def __repr__(self):
        return f"ModelName(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Brand(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)
    model_name = ForeignKey(ModelName, null=False, blank=False, on_delete=CASCADE)

    def __repr__(self):
        return f"Brand(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class CarMat(Model):
    name = CharField(max_length=20, null=False, blank=False)
    brand_name = ForeignKey(Brand, null=True, blank=False, unique=False, on_delete=SET_NULL)
    model_name = ForeignKey(ModelName, null=True, blank=False, on_delete=CASCADE)
    year_of_manufacture = DateField(null=False, blank=False)
    body = CharField(max_length=12, null=True, blank=True)
    color_of_mat = ForeignKey(ColorOfMat, null=True, blank=False, on_delete=SET_NULL, related_name='mats_color')
    color_of_trim = ForeignKey(ColorOfTrim, null=True, blank=False, on_delete=SET_NULL, related_name='trims_color')
    code_product = DateField(null=True, blank=True)

    def __repr__(self):
        return (f"CarMat(name={self.name} brand_name={self.brand_name} model_name={self.model_name} "
                f"year_of_manufacture={self.year_of_manufacture} body={self.body})")

    def __str__(self):
        return f"{self.name}"


class Accessories(Model):
    name = CharField(max_length=20, null=False, blank=False)
    brand_name = ForeignKey(Brand, null=True, blank=False, unique=False, on_delete=SET_NULL)
    model_name = ForeignKey(ModelName, null=True, blank=False, on_delete=CASCADE)
    year_of_manufacture = DateField(null=False, blank=False)
    code = DateField(null=True, blank=True)

    def __repr__(self):
        return f"Accessories(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class CategoryMain(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)
    name_car_mat = ForeignKey(CarMat, null=True, blank=False, on_delete=CASCADE)
    name_accessories = ForeignKey(Accessories, null=True, blank=False, on_delete=CASCADE)


