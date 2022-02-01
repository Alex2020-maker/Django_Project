from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import random
from .models import ProductCategory, Product
from cartapp.models import Cart


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(
        pk=hot_product.pk
    )[:3]

    return same_products


MENU_LINKS = [
    {"href": "index", "active_if": ["index"], "name": "домой"},
    {
        "href": "products:index",
        "active_if": ["products:index", "products:category"],
        "name": "продукты",
    },
    {"href": "contact", "active_if": ["contact"], "name": "контакты"},
]


def index(request):
    products = Product.objects.all()[:3]
    return render(
        request,
        "mainapp/index.html",
        context={
            "title": "Магазин",
            "content_block_class": "slider",
            "links": MENU_LINKS,
            "products": products,
        },
    )


def products(request, pk=None):

    title = "продукты"
    menu_links = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by("price")
            category = {"name": "все"}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by("price")

        content = {
            "title": title,
            "links": menu_links,
            "category": category,
            "products": products,
        }

        return render(request, "mainapp/products_list.html", context=content)

    same_products = Product.objects.all()[3:5]
    hot_product = get_hot_product()

    content = {
        "title": title,
        "links": menu_links,
        "hot_product": hot_product,
        "same_products": same_products,
    }

    return render(request, "mainapp/products.html", content)


def product(request, pk):
    title = "продукты"

    content = {
        "title": title,
        "links": ProductCategory.objects.all(),
        "product": get_object_or_404(Product, pk=pk),
    }

    return render(request, "mainapp/product.html", content)


def contact(request):
    return render(
        request,
        "mainapp/contact.html",
        context={
            "title": "Контакты",
            "content_block_class": "hero",
            "links": MENU_LINKS,
        },
    )
