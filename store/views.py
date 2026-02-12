from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers, models


class SignUpView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return Response(data=tokens, status=status.HTTP_201_CREATED)


class ProductListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class CartView(generics.RetrieveAPIView):
    serializer_class = serializers.CartSerializer

    def get(self, request):
        # user = models.User.objects.get()
        cart, _ = models.Cart.objects.get_or_create(
            user=request.user,
            status=models.Cart.CartStatus.ACTIVE
        )
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemCreateView(generics.GenericAPIView):
    serializer_class = serializers.AddCartItemSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(
            models.Product,
            id=serializer.validated_data["product_id"]
        )
        quantity = serializer.validated_data["quantity"]

        cart, _ = models.Cart.objects.get_or_create(
            user=request.user,
            status=models.Cart.CartStatus.ACTIVE
        )

        cart_item, created = models.CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(
            {"message": "Product added to cart"},
            status=status.HTTP_201_CREATED
        )


class CartItemDeleteView(generics.DestroyAPIView):
    def get_queryset(self):
        return models.CartItem.objects.filter(
            cart__user=self.request.user,
            cart__status=models.Cart.CartStatus.ACTIVE
        )


class CheckOutView(APIView):

    @transaction.atomic
    def get(self, request):
        cart = models.Cart.objects.filter(
            user=request.user,
            status=models.Cart.CartStatus.ACTIVE
        ).prefetch_related("items__product").first()

        amount = 0
        for cart_item in cart.items.all():
            amount += cart_item.product.price * cart_item.quantity

        order = models.Order.objects.create(
            cart=cart,
            amount=amount
        )

        cart.status = models.Cart.CartStatus.ORDERED
        cart.save()
        order.save()

        return Response(
            {
                "order_id": order.id,
                "amount": amount,
                "status": order.status
            },
            status=status.HTTP_201_CREATED
        )
