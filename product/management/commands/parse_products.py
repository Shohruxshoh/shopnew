from django.core.management.base import BaseCommand
from product.parsers import parse_and_save_products


class Command(BaseCommand):
    help = 'Mahsulotlarni sayt orqali parsing qilib, ma\'lumotlar bazasiga saqlaydi.'

    def handle(self, *args, **kwargs):
        parse_and_save_products()
        self.stdout.write(self.style.SUCCESS('Parsing muvaffaqiyatli tugadi!'))
