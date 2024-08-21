from django.test import TestCase

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem


class CartItemTests(TestCase):
    def setUp(self):
        # Foydalanuvchi yaratish
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Mahsulot yaratish
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                                              stock=100)

        # Savatcha yaratish
        self.cart = Cart.objects.create(user=self.user)

    def test_add_cart_item(self):
        response = self.client.post('/cart/items/', {'product': self.product.id, 'quantity': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().product, self.product)

    def test_update_cart_item(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.put(f'/cart/items/{self.cart.id}/{self.product.id}/update/', {'quantity': 3},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_remove_cart_item(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.delete(f'/cart/items/{self.cart.id}/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_items_detail(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.get('/cart/items/details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['product'], self.product.id)


class ProductParsingTests(TestCase):
    def setUp(self):
        # Bu yerda test uchun kerakli ma'lumotlar yaratiladi
        pass

    def test_parse_and_save_products(self):
        from .parsers import parse_and_save_products

        # Mahsulotlarni parse qilib saqlash
        parse_and_save_products()

        # Testdan keyin ma'lumotlar bazasida mahsulotlar mavjudligini tekshirish
        self.assertGreater(Product.objects.count(), 0)  # Mahsulotlar mavjudligini tekshiring

