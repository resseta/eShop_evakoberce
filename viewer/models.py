from django.db import models

# Create your models here.
from django.db.models import *


class Color(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    def __repr__(self):
        return f"Color(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Brand(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    def __repr__(self):
        return f"Brand(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class ModelName(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    def __repr__(self):
        return f"ModelName(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class CatalogMain(Model):
    brand_name = ForeignKey(Brand, null=False, blank=False, unique=True)
    model_name = ForeignKey(ModelName, null=False, blank=False, unique=True)
    year_of_manufacture = DateField(null=False, blank=False)
    color_of_mat = ForeignKey(Color, null=False, blank=False)
    color_of_trim = ForeignKey(Color, null=False, blank=False)
    code_product = DateField(null=True, blank=True)
    body = CharField(max_length=12, null=True, blank=True)

    def __repr__(self):
        return f"CatalogMain(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Accessories(Model):
    name = CharField(max_length=20, null=False, blank=False)

    def __repr__(self):
        return f"Accessories(name={self.name})"

    def __str__(self):
        return f"{self.name}"



