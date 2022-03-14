from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.shortcuts import get_object_or_404


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


class CartQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(CartQuerySet, self).delete(*args, **kwargs)


objects = CartQuerySet.as_manager()


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="количество", default=0)
    add_datetime = models.DateTimeField(verbose_name="время", auto_now_add=True)

    def get_item(pk):
        return get_object_or_404(Cart, pk=pk)

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete()

    @classmethod
    def get_items(self, user):
        return Cart.objects.filter(user=user)

    objects = CartManager()
