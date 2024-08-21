import requests
from bs4 import BeautifulSoup
from .models import Product


def parse_and_save_products():
    # Misol yaratib test qilib ko'rish uchun localhosdan foydalanilgan
    url = 'http://127.0.0.1:8000/index/'  # Parsing qilinadigan sayt URL manzili
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        """
            Htmlni moslashtirish kerak, qaysi tagga productni qaysi fieldi kelayotganiga 
            qarab class va tag nomlarni to'g'irlab chiqish kerak
        """
        # Mahsulotlar ro'yxatini olish
        products = soup.find_all('div', class_='col-md-3')  # Elementlarni moslashtirish kerak
        print(products)
        for item in products:
            # Mahsulot nomini olish
            name = item.find('h5', class_='card-title').text.strip()

            # Mahsulot narxini olish
            price = item.find('p', class_='price').text.strip()

            # Tavsif mavjud bo'lmasa, standart qiymat
            description = item.find('p', class_='description').text.strip()

            # Stok miqdorini aniqlash (agar mavjud bo'lsa)
            stock = item.find('p', class_='stock').text.strip()

            # Narxni tozalash (masalan, 'сум' belgisini olib tashlash)
            price = float(price.replace('сум', '').replace(' ', '').replace(',', ''))

            # Ma'lumotlar bazasiga mahsulotni saqlash
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock=stock
            )
    else:
        print(f"Xatolik: Saytga kirishda muammo bo'ldi, status code: {response.status_code}")
