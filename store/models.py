from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=50, null=False)
    descroption = models.CharField(max_length=500, null=False)
    price = models.IntegerField(null=False)


class Cart(models.Model):
    ...


class CartItem(models.Model):
    ...


class Order(models.Model):
    ...


class User(models.Model):
    ...
