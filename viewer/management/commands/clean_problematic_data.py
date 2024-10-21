from django.core.management.base import BaseCommand
from viewer.models import ProductImage, Product


class Command(BaseCommand):
    help = 'Clean problematic ProductImage data with invalid foreign keys before migrations.'

    def handle(self, *args, **kwargs):
        # Найти все ProductImage, у которых есть неверные значения в колонке image
        invalid_records = ProductImage.objects.exclude(image__in=Product.objects.values_list('image', flat=True))

        if invalid_records.exists():
            self.stdout.write(self.style.ERROR(f"Некорректные записи найдены:"))
            for record in invalid_records:
                self.stdout.write(self.style.ERROR(f'ID: {record.id}, image: {record.image}'))

            deleted_count, _ = invalid_records.delete()
            self.stdout.write(self.style.SUCCESS(f'Было удалено {deleted_count} некорректных записей из ProductImage.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Некорректные записи не найдены, ничего не удалено.'))
