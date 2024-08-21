from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartItemSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from drf_spectacular.utils import extend_schema


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class AddCartItemView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CartItemSerializer,
        responses={200: CartItemSerializer},
        summary="Create a Cart Item",
        description="cart and product id are entered."
    )
    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        data = request.data.copy()
        data['cart'] = cart.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RemoveCartItemView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart_id = self.kwargs.get('cart_id')
        product_id = self.kwargs.get('product_id')
        try:
            return CartItem.objects.get(cart_id=cart_id, product_id=product_id)
        except CartItem.DoesNotExist:
            raise NotFound("Cart item not found.")


class CartItemsDetailView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        return CartItem.objects.filter(cart=cart)


class UpdateCartItemView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart_id = self.kwargs.get('cart_id')
        product_id = self.kwargs.get('product_id')
        try:
            return CartItem.objects.get(cart_id=cart_id, product_id=product_id)
        except CartItem.DoesNotExist:
            raise NotFound("Cart item not found.")

    @extend_schema(
        request=CartItemSerializer,
        responses={200: CartItemSerializer},
        summary="Update an item in the cart",
        description="Update the quantity of a product in the user's cart."
    )
    def put(self, request, *args, **kwargs):
        cart_id = self.kwargs.get('cart_id')
        product_id = self.kwargs.get('product_id')
        cart_item = self.get_object()

        if cart_item.cart.user != request.user:
            return Response({"detail": "Not authorized to update this cart item."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['cart'] = cart_id
        serializer = self.get_serializer(cart_item, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


def index(request):
    products = [
        {'name': "Product1", 'description': "Product1 description", 'price': 2.03, 'stock': 10},
        {'name': "Product2", 'description': "Product2 description", 'price': 20.03, 'stock': 10},
        {'name': "Product3", 'description': "Product3 description", 'price': 32.03, 'stock': 10}
    ]
    return render(request, 'products.html', {"products": products})
