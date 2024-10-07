# viewer/management/commands/transfer_payment_data.py
from django.core.management.base import BaseCommand
from viewer.models import Payment, PaymentMethod


class Command(BaseCommand):
    help = 'Transfer data from payment_method_temp to payment_method'

    def handle(self, *args, **kwargs):
        self.stdout.write('Заполнение таблицы PaymentMethod уникальными значениями из payment_method_temp...')

        unique_payment_methods = Payment.objects.exclude(payment_method_temp__isnull=True).exclude(
            payment_method_temp__exact='').values_list('payment_method_temp', flat=True).distinct()

        for method_name in unique_payment_methods:
            if method_name:
                try:
                    payment_method, created = PaymentMethod.objects.get_or_create(name=method_name)
                    self.stdout.write(f"Создан или найден PaymentMethod: {method_name} (Создано: {created})")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка при создании PaymentMethod '{method_name}': {e}"))

        self.stdout.write('Перенос данных из payment_method_temp в payment_method...')
        unresolved_payments = []

        for payment in Payment.objects.exclude(payment_method_temp__isnull=True).exclude(payment_method_temp__exact=''):
            if payment.payment_method_temp:
                try:
                    method = PaymentMethod.objects.get(name=payment.payment_method_temp)
                    payment.payment_method = method
                    payment.save(update_fields=["payment_method"])
                    self.stdout.write(f"Перенесено Payment ID {payment.id}: {payment.payment_method_temp}")
                except PaymentMethod.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"PaymentMethod '{payment.payment_method_temp}' не найден для Payment ID {payment.id}"))
                    unresolved_payments.append(payment.id)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка при переносе Payment ID {payment.id}: {e}"))

        if unresolved_payments:
            self.stdout.write(
                self.style.WARNING(f"Не удалось перенести Payment ID: {', '.join(map(str, unresolved_payments))}"))

        self.stdout.write(self.style.SUCCESS('Data transfer completed successfully.'))
