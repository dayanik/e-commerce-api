from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from . import serializers, models


User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User
    serializer_class = serializers.SignUpSerializer
    permission_classes = [AllowAny]


class ProductListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class CartView(generics.RetrieveAPIView):

    def get(self, request):
        cart, created = models.Cart.objects.get_or_create(
            user=request.user,
            status=models.Cart.CartStatus.ACTIVE
        )
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)


class CartItemCreateView(generics.GenericAPIView):
    serializer_class = serializers.AddCartItemSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(
            models.Product,
            id=serializer.validated_data["product_id"])
        quantity = serializer.validated_data["quantity"]

        cart, created = models.Cart.objects.get_or_create(
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
