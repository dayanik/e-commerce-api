from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from . import views

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('products', views.ProductListView.as_view(), name="products"),
    path('products/<int:pk>', views.ProductView.as_view(), name="get_product"),
    path('cart', views.CartView.as_view(), name='cart'),
    path('cart/items', views.CartItemCreateView.as_view(), name='add_cart_item'),
    path('cart/items/<int:pk>', views.CartItemDeleteView.as_view(), name='remove_cart_item'),
]
