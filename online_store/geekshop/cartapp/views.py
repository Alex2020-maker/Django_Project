from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from cartapp.models import Cart
from mainapp.models import Product

# Create your views here.

def cart(request):
    return render(request, 'cartapp/cart.html', context={
        'cart': request.user.cart.all()
    })


def add_to_card(request, pk=None):

    product = get_object_or_404(Product, pk=pk)
    
    cart_product = request.user.cart.filter(id=pk).first()

    if not cart_product:
        cart_product = Cart(user=request.user, product=product)

    cart_product.quantity += 1
    cart_product.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, pk):
    return render(request, 'cartapp/cart.html')
