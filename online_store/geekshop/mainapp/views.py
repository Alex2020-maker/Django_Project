from django.shortcuts import render

MENU_LINKS = [
    {'href': 'index', 'name': 'домой'},
    {'href': 'products', 'name': 'продукты'},
    {'href': 'contact', 'name': 'контакт'},

]

def index(request):
    products = [
        {
            'name': 'Суперлампа!',
            'description': 'Светит на все свои 100 ватт',
            'image_path': 'img/product-1.jpg',
        },
        {
            'name': 'Стул повышенного',
            'description': 'Не оторваться.',
            'image_path': 'img/product-2.jpg',
        },
        {
            'name': 'Настольный светильник из 90-х',
            'description': 'Мало того, что ламповый, так ещ и квартиру обогревает!',
            'image_path': 'img/product-3.jpg',
        },

    ] 
    return render(request, 'mainapp/index.html', context={
        'title': 'Магазин',
        'content_block_class': 'slider',
        'links': MENU_LINKS,
        'products': products,
    })

def products(request):
    products = [
        {
            'name': 'Суперлампа!',
            'description': 'Светит на все свои 100 ватт',
            'image_path': 'img/product-11.jpg',
        },
        {
            'name': 'Стул повышенного',
            'description': 'Не оторваться.',
            'image_path': 'img/product-21.jpg',
        },
        {
            'name': 'Настольный светильник из 90-х',
            'description': 'Мало того, что ламповый, так ещ и квартиру обогревает!',
            'image_path': 'img/product-31.jpg',
        },

    ] 
    return render(request, 'mainapp/products.html', context={
        'title': 'Каталог',
        'content_block_class': 'hero-white',
        'links': MENU_LINKS,
        'products': products,
    })

def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'title': 'Контакты',
        'content_block_class': 'hero',
        'links': MENU_LINKS,
    })