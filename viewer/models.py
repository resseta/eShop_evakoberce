from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class Body(models.Model):
    name = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class ColorOfMat(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class ColorOfTrim(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Subsubcategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='subsubcategories')
    image = models.ImageField(upload_to='subsubcategories/', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=60)
    subsubcategory = models.ForeignKey(Subsubcategory, on_delete=models.CASCADE, related_name='products')
    year_of_manufacture = models.CharField(max_length=20)
    body = models.ForeignKey(Body, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, null=True, blank=True)
    short_description = models.TextField()
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(verbose_name=_('Cena'))
    availability = models.BooleanField(default=False)
    image = models.ImageField(default='no_image.png', upload_to='products/')
    mat_color = models.ForeignKey(ColorOfMat, default=1, on_delete=models.CASCADE, related_name='products')
    trim_color = models.ForeignKey(ColorOfTrim, default=1, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

class Cart(models.Model):
    session_key = models.CharField(max_length=100)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart {self.id} - {self.session_key}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Cart {self.cart.id}"


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=35)
    customer_surname = models.CharField(max_length=35)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, default='+420 000 000 000')
    customer_address = models.CharField(max_length=255)
    customer_city = models.CharField(max_length=50)
    customer_postal_code = models.CharField(max_length=6)
    customer_country = models.CharField(max_length=100, default='Česká republika')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"
