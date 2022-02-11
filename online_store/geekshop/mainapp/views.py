from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import random
from .models import ProductCategory, Product
from cartapp.models import Cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    products = Product.objects.all()[:4]
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


def products(request, pk=None, page=1):

    title = "продукты"
    menu_links = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = Product.objects.filter(is_active=True,\
                   category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, \
                   is_active=True, category__is_active=True).order_by('price')
        
        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)  

        content = {
            "title": title,
            "links": menu_links,
            "category": category,
            "products": products_paginator
        }

        return render(request, "mainapp/products_list.html", context=content)

    same_products = Product.objects.all()[:3]
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
