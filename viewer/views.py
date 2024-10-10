from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .models import Category, Subcategory, Subsubcategory, Product, Cart, CartItem, Order, OrderItem, ColorOfMat, \
    ColorOfTrim
from .forms import OrderForm


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def subcategory_list(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    subcategories = category.subcategories.all()
    return render(request, 'subcategory_list.html', {'category': category, 'subcategories': subcategories})


def subsubcategory_list(request, category_name, subcategory_name):
    category = get_object_or_404(Category, name=category_name)
    subcategory = get_object_or_404(Subcategory, name=subcategory_name, category=category)
    subsubcategories = subcategory.subsubcategories.all()
    return render(request, 'subsubcategory_list.html',
                  {'category': category, 'subcategory': subcategory, 'subsubcategories': subsubcategories})


def product_list(request, category_name, subcategory_name, subsubcategory_name):
    category = get_object_or_404(Category, name=category_name)
    subcategory = get_object_or_404(Subcategory, name=subcategory_name, category=category)
    subsubcategory = get_object_or_404(Subsubcategory, name=subsubcategory_name, subcategory=subcategory)
    products = subsubcategory.products.all()
    return render(request, 'product_list.html', {'subcategory': subsubcategory, 'products': products})


def product_detail(request, category_name, subcategory_name, subsubcategory_name, product_name):
    product = get_object_or_404(Product, name=product_name)
    mat_colors = ColorOfMat.objects.all()
    trim_colors = ColorOfTrim.objects.all()
    return render(request, 'product_detail.html',
                  {'product': product, 'mat_colors': mat_colors, 'trim_colors': trim_colors})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{product.name} добавлен в корзину.')
    return redirect('view_cart')


def view_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart = Cart.objects.filter(session_key=session_key).first()
    return render(request, 'cart.html', {'cart': cart})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            cart = Cart.objects.filter(session_key=session_key).first()
            if not cart:
                messages.error(request,
                               'Ваша корзина пуста. Пожалуйста, добавьте товары в корзину перед тем, как оформить заказ.')
                return redirect('view_cart')

            cart_items = CartItem.objects.filter(cart=cart)
            with transaction.atomic():
                order = Order.objects.create(
                    cart=cart,
                    customer_name=form.cleaned_data['customer_name'],
                    customer_surname=form.cleaned_data['customer_surname'],
                    customer_email=form.cleaned_data['customer_email'],
                    customer_phone=form.cleaned_data['customer_phone'],
                    customer_address=form.cleaned_data['customer_address'],
                    customer_city=form.cleaned_data['customer_city'],
                    customer_postal_code=form.cleaned_data['customer_postal_code'],
                    customer_country=form.cleaned_data['customer_country'],
                    total_amount=cart.total_price(),
                )

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )

                cart.delete()

            request.session['order_id'] = order.id
            messages.success(request, 'Ваш заказ успешно оформлен!')
            return redirect('success')

    messages.error(request, 'Ошибка при оформлении заказа. Пожалуйста, попробуйте снова.')
    return redirect('view_cart')


def success_view(request):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, 'Order ID не найден в сессии. Пожалуйста, попробуйте снова.')
        return redirect('view_cart')

    order = get_object_or_404(Order, id=order_id)
    return render(request, 'success.html', {'order': order})
