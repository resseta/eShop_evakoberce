from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from .models import Product, Cart, CartItem, ColorOfMat, ColorOfTrim, Payment, Shipping, PaymentMethod, ShippingMethod
from .forms import AddToCartForm
from django.contrib import messages

from viewer.models import Accessories, Category, Subcategory, Product


# Create your views here.


def home(request):
    products = Product.objects.all()
    cart = None
    if request.session.session_key:
        cart = Cart.objects.get(session_key=request.session.session_key)

    context = {
        'products': products,
        'cart': cart
    }
    return render(request, 'home.html', context)


class AccessoriesListView(ListView):
    template_name = "accessories.html"
    model = Accessories
    context_object_name = 'accessories'


def accessories(request, pk):
    if Accessories.objects.filter(id=pk).exists():
        accessories_ = Accessories.objects.get(id=pk)
        context = {'accessories': accessories_}
        return render(request, "accessories.html", context)
    return redirect('accessories')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    return render(request, 'subcategory_list.html', {'category': category, 'subcategories': subcategories})


def product_list(request, subcategory_id):
    categories = Category.objects.all()
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    products = subcategory.products.all()
    return render(request, 'product_list.html', {'subcategory': subcategory, 'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    mat_colors = ColorOfMat.objects.filter()
    trim_colors = ColorOfTrim.objects.filter()
    form = AddToCartForm()

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
            CartItem.objects.create(
                cart=cart,
                product=product,
                mat_color=form.cleaned_data['mat_color'],
                trim_color=form.cleaned_data['trim_color'],
                quantity=form.cleaned_data['quantity']
            )
            messages.success(request, 'Product was successfully added to the cart!')
            return redirect('product_detail', id=product.id)
    else:
        form = AddToCartForm(initial={'product_id': product.id})

    context = {
        'product': product,
        'mat_colors': mat_colors,
        'trim_colors': trim_colors,
        'form': form
    }
    return render(request, 'product_detail.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
            CartItem.objects.create(
                cart=cart,
                product=product,
                mat_color=form.cleaned_data['mat_color'],
                trim_color=form.cleaned_data['trim_color'],
                quantity=form.cleaned_data['quantity']
            )
            messages.success(request, 'Product was successfully added to the cart!')
            return redirect('home')  # Přesměrování na hlavní stránku

    else:
        form = AddToCartForm(initial={'product_id': product.id})

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'product_detail.html', context)

def view_cart(request):
    if not request.session.session_key:
        request.session.create()

    try:
        cart = Cart.objects.get(session_key=request.session.session_key)
    except Cart.DoesNotExist:
        cart = None

    context = {'cart': cart}
    return render(request, 'cart.html', context)


def checkout(request):
    cart = Cart.objects.get(session_key=request.session.session_key)

    if request.method == 'POST':
        payment_method = PaymentMethod.objects.get(id=request.POST['payment_method'])
        shipping_method = ShippingMethod.objects.get(id=request.POST['shipping_method'])

        # Zpracování a vytvoření/aktualizace platby
        payment, created = Payment.objects.get_or_create(
            cart=cart,
            defaults={
                'total_price': cart.total_price(),
                'payment_method': payment_method
            }
        )
        if not created:
            payment.total_price = cart.total_price()
            payment.payment_method = payment_method
            payment.save()

        # Zpracování a vytváření/aktualizace doručení
        shipping, created = Shipping.objects.get_or_create(
            cart=cart,
            defaults={
                'address': request.POST['address'],
                'city': request.POST['city'],
                'postal_code': request.POST['postal_code'],
                'country': request.POST['country'],
                'telefon': request.POST['phone'],
                'email': request.POST['email'],
                'shipping_method': shipping_method
            }
        )
        if not created:
            shipping.address = request.POST['address']
            shipping.city = request.POST['city']
            shipping.postal_code = request.POST['postal_code']
            shipping.country = request.POST['country']
            shipping.telefon = request.POST['phone']
            shipping.email = request.POST['email']
            shipping.shipping_method = shipping_method
            shipping.save()

        messages.success(request, 'Your order has been processed successfully!')
        return redirect('success_view')

    payment_methods = PaymentMethod.objects.all()
    shipping_methods = ShippingMethod.objects.all()

    return render(request, 'checkout.html', {
        'cart': cart,
        'payment_methods': payment_methods,
        'shipping_methods': shipping_methods,
    })

def success_view(request):
    if not request.session.session_key:
        request.session.create()

    try:
        cart = Cart.objects.get(session_key=request.session.session_key)
        item = cart.cart_items.first()  # nebo jiná metoda pro získání potřebného item
    except Cart.DoesNotExist:
        item = None

    return render(request, 'success.html', {'item': item})

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def place_order(request):
    if not request.session.session_key:
        request.session.create()

    try:
        cart = Cart.objects.get(session_key=request.session.session_key)
        item = cart.cartitem_set.first()  # Používejte správné spojení
    except Cart.DoesNotExist:
        cart = None
        item = None

    if request.method == 'POST':
        # Логика оформления заказа
        messages.success(request, 'Your order has been processed successfully!')
        return redirect('success_view')

    return render(request, 'checkout.html', {'cart': cart, 'item': item})

def error_view(request):
    return render(request, 'error.html')

