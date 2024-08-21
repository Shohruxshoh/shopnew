from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, AddCartItemView, RemoveCartItemView, CartItemsDetailView, UpdateCartItemView, index

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('cart/items/', AddCartItemView.as_view(), name='add_cart_item'),
    path('cart/items/<int:cart_id>/<int:product_id>/', RemoveCartItemView.as_view(), name='remove_cart_item'),
    path('cart/items/details/', CartItemsDetailView.as_view(), name='cart_items_details'),
    path('cart/items/<int:cart_id>/<int:product_id>/update/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('index/', index),
]
