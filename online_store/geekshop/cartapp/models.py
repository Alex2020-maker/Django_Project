from django.db import models
from django.conf import settings
from mainapp.models import Product


class CartManager(models.Manager):
    @property
    def amount(self):
        return sum(item.quantity for item in self.all())

    @property
    def total_cost(self):
        return sum(item.product.price * item.quantity for item in self.all())

    @property
    def has_items(self):
        return bool(len(self.all()))


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="количество", default=0)
    add_datetime = models.DateTimeField(verbose_name="время", auto_now_add=True)

    objects = CartManager()
