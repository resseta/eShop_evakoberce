# context_processors.py

from .models import Cart, CartItem
from django.db.models import Sum


def cartitem_quantity(request):
    if not request.session.session_key:
        request.session.create()

    try:
        cart = Cart.objects.get(session_key=request.session.session_key)
        total_quantity = CartItem.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))[
                             'total_quantity'] or 0
    except Cart.DoesNotExist:
        total_quantity = 0

    return {'cartitem_quantity': total_quantity}
