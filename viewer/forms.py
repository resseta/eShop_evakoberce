from django import forms
from .models import Product, ColorOfMat, ColorOfTrim


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    mat_color = forms.ModelChoiceField(queryset=ColorOfMat.objects.filter(), required=True)
    trim_color = forms.ModelChoiceField(queryset=ColorOfTrim.objects.filter(), required=True)
    quantity = forms.IntegerField(min_value=1, initial=1)