from nis import cat
from django.shortcuts import get_object_or_404, render
from django.template import context
from django.urls import reverse
from .models import ProductCategory, Product

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
    products = Product.objects.all()
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

    title = 'продукты'
    menu_links = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'title': title,
            "links": menu_links,
            'category': category,
            'products': products,
        }

        return render(request, 'mainapp/products_list.html', context=content)

        
    same_products = Product.objects.all()
    
    content = {
        'title': title, 
        "links": menu_links,
        'same_products': same_products
    }
    
    return render(request, 'mainapp/products.html', content)


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
