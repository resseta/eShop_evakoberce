import os

from django.db import models
from datetime import datetime
from uuid import uuid4

from django.template.defaultfilters import default
from django.utils import timezone

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


def upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    new_filename = f"{base}_{uuid4().hex}{ext}"
    return os.path.join('products/', new_filename)


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
        return sum(item.total_price() for item in self.cart_items.all())  # Используем related_name cart_items

    def total_amount(self):
        return sum(item.quantity for item in self.cart_items.all())

    def __str__(self):
        return f"Cart {self.id} for session {self.session_key}"


class CartItem(Model):
    cart = ForeignKey(Cart, related_name='cart_items', on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    mat_color = ForeignKey(ColorOfMat, on_delete=models.CASCADE, related_name='cart_items')
    trim_color = ForeignKey(ColorOfTrim, on_delete=models.CASCADE, related_name='cart_items')
    quantity = PositiveIntegerField(default=1)
    price = DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        # return self.product.price * self.quantity
        return self.quantity * self.price

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
    shipping_method = ForeignKey(ShippingMethod, on_delete=PROTECT)
    shipping_status = CharField(max_length=50, default='Pending')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Order(Model):
    order_id = AutoField(primary_key=True)
    cart = ForeignKey('Cart', on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = CharField(max_length=85)
    customer_email = EmailField()
    customer_phone = CharField(max_length=20, default='000 000 000')
    customer_address = CharField(max_length=255)
    customer_city = CharField(max_length=100)
    customer_postal_code = CharField(max_length=20)
    customer_country = CharField(max_length=100, default='Česká republika')
    order_date = DateTimeField(auto_now_add=True)
    total_amount = DecimalField(max_digits=10, decimal_places=2)
    status = CharField(max_length=30,
                              choices=(('New', 'New'), ('Processing', 'Processing'), ('Completed', 'Completed')))
    created_at = DateTimeField(auto_now_add=True)
    payment_method = CharField(max_length=50, null=True, blank=True)
    shipping_method = CharField(max_length=50, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.id = self.order_id  # Ссылка id на order_id

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"


class OrderItem(Model):
    order = ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = ForeignKey('Product', on_delete=models.CASCADE)
    mat_color = CharField(max_length=50)
    trim_color = CharField(max_length=50)
    quantity = PositiveIntegerField()
    price = DecimalField(max_digits=10, decimal_places=2)  # Assuming each item has a price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"