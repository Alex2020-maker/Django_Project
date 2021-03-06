# Generated by Django 3.2.7 on 2021-12-23 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productcategory",
            name="name",
            field=models.CharField(
                blank=True, max_length=64, unique=True, verbose_name="имя"
            ),
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, unique=True, verbose_name="имя"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="описание"),
                ),
                (
                    "short_description",
                    models.TextField(
                        blank=True, max_length=64, verbose_name="короткое описание"
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=8, verbose_name="цена"
                    ),
                ),
                (
                    "price_with_discount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=8,
                        verbose_name="цена со скидкой",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        default=0, verbose_name="количество товаров на складе"
                    ),
                ),
                ("image", models.ImageField(blank=True, upload_to="products_image")),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="mainapp.productcategory",
                    ),
                ),
            ],
        ),
    ]
