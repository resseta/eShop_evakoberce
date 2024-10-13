from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_order_confirmation_email(order):
    subject = 'Nová objednávka v e-shopu EVA koberce'
    html_message = render_to_string('order_confirmation.html', {'order': order})
    plain_message = strip_tags(html_message)
    from_email = 'evakoberce@gmail.com'
    to = order.customer_email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
