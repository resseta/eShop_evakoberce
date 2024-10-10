from django import forms
from .models import Product, ColorOfMat, ColorOfTrim, Order, Product


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    mat_color = forms.ModelChoiceField(queryset=ColorOfMat.objects.filter(), required=True)
    trim_color = forms.ModelChoiceField(queryset=ColorOfTrim.objects.filter(), required=True)
    quantity = forms.IntegerField(min_value=1, initial=1)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 'total_amount']
        model = Product
        fields = ['name', 'image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image']