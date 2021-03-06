from dataclasses import is_dataclass
import random
import decimal
from django.db import models
from django.db.models.fields import DecimalField, FloatField, CharField

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(verbose_name="имя", max_length=64, unique=True, blank=True)
    description = models.TextField(verbose_name="описание", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="активна", db_index=True, default=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    class Meta:
        ordering = ("-price", "name")

    name = models.CharField(verbose_name="имя", max_length=128, unique=True)
    description = models.TextField(verbose_name="описание", blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    short_description = models.TextField(
        verbose_name="короткое описание", max_length=64, blank=True
    )
    price = models.DecimalField(
        verbose_name="цена", max_digits=8, decimal_places=2, default=0
    )
    price_with_discount = models.DecimalField(
        verbose_name="цена со скидкой", max_digits=8, decimal_places=2, default=0
    )

    quantity = models.PositiveIntegerField(
        verbose_name="количество товаров на складе", default=0
    )

    image = models.ImageField(upload_to="products_image", blank=True)

    is_active = models.BooleanField(verbose_name="В каталоге", db_index=True, default=True)

    def total_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by("category", "name")
