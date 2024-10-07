from django.db import models
from datetime import datetime

# Create your models here.
from django.db.models import *


class ColorOfTrim(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'coloroftrim'

    def __repr__(self):
        return f"ColorOfTrim(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class ColorOfMat(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'colorofmat'

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
    quantity = PositiveIntegerField(default=1)
    price = FloatField(verbose_name='Cena', null=False, blank=False)
    availability = BooleanField(default=False)
    image = ImageField(default='no_image.png', upload_to='products/')
    mat_color = ForeignKey(ColorOfMat, default=1, on_delete=models.CASCADE, related_name='products')
    trim_color = ForeignKey(ColorOfTrim, default=1, on_delete=models.CASCADE, related_name='products')

    def __repr__(self):
        return (f"CarMat(name={self.name} brand_name={self.brand_name} model_name={self.model_name} "
                f"year_of_manufacture={self.year_of_manufacture} body={self.body})")

    def __str__(self):
        return f"{self.name}"

class ProductImage(Model):
    product = ForeignKey(Product, related_name='images',
                                on_delete=CASCADE)  # Establish one-to-many relationship
    image = ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"


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


class Cart(Model):
    session_key = CharField(max_length=40, unique=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    def __str__(self):
        return f"Cart {self.id} for session {self.session_key}"


class CartItem(Model):
    cart = ForeignKey(Cart, related_name='cart_items', on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    mat_color = ForeignKey(ColorOfMat, on_delete=models.CASCADE, related_name='cart_items')
    trim_color = ForeignKey(ColorOfTrim, on_delete=models.CASCADE, related_name='cart_items')
    quantity = PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in cart {self.cart.id}"


class PaymentMethod(Model):
    name = CharField(max_length=50)
    description = TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Payment(Model):
    cart = OneToOneField(Cart, on_delete=models.CASCADE)
    total_price = DecimalField(max_digits=8, decimal_places=2)
    payment_method = ForeignKey(PaymentMethod, on_delete=models.PROTECT, null=True, blank=True)
    payment_status = CharField(max_length=40, default='Pending')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class ShippingMethod(Model):
    name = CharField(max_length=50)
    description = TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Shipping(Model):
    cart = OneToOneField(Cart, on_delete=models.CASCADE)
    address = TextField()
    city = CharField(max_length=100)
    postal_code = CharField(max_length=20)
    country = CharField(max_length=100)
    telefon = CharField(max_length=20)
    email = CharField(max_length=60)
    shipping_method = ForeignKey(ShippingMethod, on_delete=models.PROTECT)
    shipping_status = CharField(max_length=50, default='Pending')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

