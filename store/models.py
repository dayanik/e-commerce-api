from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=500, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title


class Cart(models.Model):
    class CartStatus(models.TextChoices):
        ACTIVE = "active"
        ORDERED = "ordered"

    status = models.CharField(choices=CartStatus, default=CartStatus.ACTIVE)
    user = models.ForeignKey(
        User, 
        related_name="carts", 
        on_delete=models.PROTECT
    )


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.PROTECT,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_in_cart"
            )
        ]


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending"
        PAID = "paid"
        SHIPPED = "shipped"
        COMLETED = "completed"
        CANCELED = "canceled"

    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus,
        default=OrderStatus.PENDING
    )
