import imp
from django.conf import settings
from django.db import models
from mainapp.models import Product
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

# Create your models here.


class Order(models.Model):
    FORMING = "FM"
    SENT_TO_PROCEED = "STP"
    PROCEEDED = "PRD"
    PAID = "PD"
    READY = "RDY"
    CANCEL = "CNC"

    ORDER_STATUS_CHOICES = (
        (FORMING, "формируется"),
        (SENT_TO_PROCEED, "отправлен в обработку"),
        (PAID, "оплачен"),
        (PROCEEDED, "собран"),
        (READY, "готов к выдаче"),
        (CANCEL, "отменен"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="создан", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="обновлен", auto_now=True)
    status = models.CharField(
        verbose_name="статус",
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING,
    )
    is_active = models.BooleanField(verbose_name="активен", default=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return "Текущий заказ: {}".format(self.id)

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
            }

    @cached_property
    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)




# при удалении заказа товар возвращается на склад
class OrderItemQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(OrderItemQuerySet, self).delete(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="orderitems", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, verbose_name="продукт", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name="количество", default=0)

    objects = OrderItemQuerySet.as_manager()

    def get_product_cost(self):
        return self.product.price * self.quantity

    def get_item(pk):
        return get_object_or_404(OrderItem, pk=pk)

    def save(self, *args, **kwargs):
        try:
            if self.pk:
                self.product.quantity -= (
                    self.quantity - self.__class__.get_item(self.pk).quantity
                )
            else:
                self.product.quantity -= self.quantity
            if self.product.quantity < 0:
                raise Exception("Количество превышает остаток на складе")
        except Exception as exp:
            print(exp)
        else:
            self.product.save()
            super(self.__class__, self).save(*args, **kwargs)

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete()
