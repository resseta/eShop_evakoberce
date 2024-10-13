from venv import logger

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import get_language
import logging

from .models import Product, Cart, CartItem, ColorOfMat, ColorOfTrim, Payment, Shipping, PaymentMethod, ShippingMethod, \
    OrderItem
from .forms import AddToCartForm, ProductForm
from django.contrib import messages
from django.utils.translation import get_language

from viewer.models import Accessories, Category, Subcategory, Product, Order

from .sendmail import send_order_confirmation_email

logger = logging.getLogger(__name__)

# Create your views here.


def home(request):
    products = Product.objects.all()
    cart = None
    # if request.session.session_key:
    #     cart = Cart.objects.get(session_key=request.session.session_key)

    context = {
        'products': products,
        # 'cart': cart
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

    # Логирование данных для отладки
    print("Category:", category)
    print("Subcategories:", subcategories)
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
            # Získáme nebo vytvoříme košík
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

            # Vložíme položku do košíku s uvedením ceny
            CartItem.objects.create(
                cart=cart,
                product=product,
                mat_color=form.cleaned_data['mat_color'],
                trim_color=form.cleaned_data['trim_color'],
                quantity=form.cleaned_data['quantity'],
                price=product.price  # Обязательно указываем цену продукта
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

def cart_empty_view(request):
    return render(request, 'cart_empty.html')


def checkout(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart = get_object_or_404(Cart, session_key=request.session.session_key)

    if cart.cart_items.count() == 0:
        messages.error(request, 'Váš koš je prázdný. Před zadáním objednávky přidejte zboží do košíku.')
        return redirect('cart_empty')

    if request.method == 'POST':
        payment_method = get_object_or_404(PaymentMethod, id=request.POST['payment_method'])
        shipping_method = get_object_or_404(ShippingMethod, id=request.POST['shipping_method'])

        with transaction.atomic():
            try:
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

                customer_name = request.POST.get('customer_name')
                customer_email = request.POST.get('customer_email')
                customer_phone = request.POST.get('customer_phone')
                customer_address = request.POST.get('customer_address')
                customer_city = request.POST.get('customer_city')
                customer_postal_code = request.POST.get('customer_postal_code')
                customer_country = request.POST.get('customer_country')

                if not all([customer_name, customer_email, customer_phone, customer_address, customer_city,
                            customer_postal_code, customer_country]):
                    messages.error(request, 'Все поля обязательны для заполнения.')
                    return redirect('checkout')

                order = Order.objects.create(
                    cart=cart,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_phone=customer_phone,
                    customer_address=customer_address,
                    customer_city=customer_city,
                    customer_postal_code=customer_postal_code,
                    customer_country=customer_country,
                    total_amount=cart.total_price(),
                    status='New',
                    payment_method=payment_method.name,
                    shipping_method=shipping_method.name
                )

                # Связать Payment и Shipping с заказом
                payment.cart = cart
                payment.save()
                shipping.cart = cart
                shipping.save()

                for cart_item in CartItem.objects.filter(cart=cart):
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.price,
                        mat_color=cart_item.mat_color,
                        trim_color=cart_item.trim_color
                    )

                CartItem.objects.filter(cart=cart).delete()
                cart.delete()

                # Odeslání e-mailu potvrzení objednávky.
                send_order_confirmation_email(order)

                messages.success(request, 'Vaše objednávka byla úspěšně zpracována!')
                return redirect('success', order_id=order.order_id)

            except Exception as e:
                print(f"Error while creating payment or shipping: {e}")
                messages.error(request, 'Při vytváření platby nebo dopravy došlo k chybě. Zkuste to prosím znovu.')
                return redirect('checkout')

    payment_methods = PaymentMethod.objects.all()
    shipping_methods = ShippingMethod.objects.all()

    return render(request, 'checkout.html', {
        'cart': cart,
        'payment_methods': payment_methods,
        'shipping_methods': shipping_methods,
    })

        # order=Order.objects.create(cart=cart,
        #                            total_amount=cart.total_price()
        #                            )


def success_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    cart = order.cart

    # Найдем связанные объекты Payment и Shipping
    # try:
    #     payment = Payment.objects.get(cart=order.cart)
    # except Payment.DoesNotExist:
    #     payment = None
    #
    # try:
    #     shipping = Shipping.objects.get(cart=order.cart)
    # except Shipping.DoesNotExist:
    #     shipping = None

    # Получение связанных объектов Payment и Shipping, если они есть
    payment = Payment.objects.filter(cart=order.cart).first()
    shipping = Shipping.objects.filter(cart=order.cart).first()

    order_items = OrderItem.objects.filter(order=order)

    print(f"Order ID: {order_id}")
    print(f"Payment: {payment}, Payment Method: {payment.payment_method if payment else None}")
    print(f"Shipping: {shipping}, Shipping Method: {shipping.shipping_method if shipping else None}")

    return render(request, 'success.html', {
        'order': order,
        'payment': payment,
        'shipping': shipping,
        'order_items': order_items
    })


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')


def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            saved_filename = product.image.name
            print(saved_filename)
            return redirect('success_url')
    else:
        form = ProductForm()
    return render(request, 'upload.html', {'form': form})

def error_view(request):
    return render(request, 'error.html')

