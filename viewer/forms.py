from django import forms


class OrderForm(forms.Form):
    customer_name = forms.CharField(max_length=35)
    customer_surname = forms.CharField(max_length=35)
    customer_email = forms.EmailField()
    customer_phone = forms.CharField(max_length=20, default='+420 000 000 000')
    customer_address = forms.CharField(max_length=255)
    customer_city = forms.CharField(max_length=50)
    customer_postal_code = forms.CharField(max_length=6)
    customer_country = forms.CharField(max_length=100, initial='Česká republika')
    delivery_method = forms.ChoiceField(choices=[('standard', 'Standard'), ('express', 'Express')])
    comments = forms.CharField(widget=forms.Textarea, required=False)
