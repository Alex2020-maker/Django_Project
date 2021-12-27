from django.shortcuts import get_object_or_404, render
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
    return render(request, 'mainapp/index.html', context={
        'title': 'Магазин',
        'content_block_class': 'slider',
        'links': MENU_LINKS,
        'products': products,
    })

def products(request, pk=None):
    if not pk:
        selected_category = ProductCategory.objects.first()
    else:
        selected_category = get_object_or_404(ProductCategory, id=pk)
    
    categories = ProductCategory.objects.all()
    products = Product.objects.filter(category=selected_category)

    return render(request, 'mainapp/products.html', context={
        'title': 'Каталог',
        'content_block_class': 'hero-white',
        'links': MENU_LINKS,
        'selected_category': selected_category,
        'categories': categories,
        'products': products,
    })

def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'title': 'Контакты',
        'content_block_class': 'hero',
        'links': MENU_LINKS,
    })