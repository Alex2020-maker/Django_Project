import imp
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from .models import Cart
from mainapp.models import Product
from django.conf import settings

# Create your views here.

# Ограничение доступа к корзине только для зарегистрированных пользователей с
# помощью декоратора @login_required


@login_required
def cart(request):
    products = request.user.cart.order_by("product__category")
    return render(
        request,
        "cartapp/cart.html",
        context={
            "cart": products,
        },
    )


@login_required
def add_to_cart(request, pk=None):

    product = get_object_or_404(Product, pk=pk)

    cart_product = request.user.cart.filter(id=pk).first()

    if not cart_product:
        cart_product = Cart(user=request.user, product=product)

        cart_product.quantity += 1
        cart_product.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# добавляем AJAX: по сети передаем только ту часть страницы, которая реально изменилась
@login_required
def cart_edit(request, pk, quantity):
    if request.is_ajax():
        try:
            pk = int(pk)
            quantity = int(quantity)
        except Exception as exp:
            print(f"Wrong input numbers! {exp}")
            raise exp
        new_cart_item = Cart.objects.get(pk=pk)
        product = get_object_or_404(Product, pk=new_cart_item.product_id)

        # Проверяем что товар еще есть на складе, или что уменьшаем количество.
        if product.quantity > 0 or new_cart_item.quantity > quantity:
            new_cart_item.quantity = quantity
            new_cart_item.save()
        else:
            print('превышено количество на складе')
        if quantity == 0:
            new_cart_item.delete()

        cart_items = Cart.objects.filter(user=request.user).order_by("product__category")

        content = {
            "cart_items": cart_items,
            "media_url": settings.MEDIA_URL,
        }

        result = render_to_string("cartapp/include/inc_cart_list.html", content)

        return JsonResponse({"result": result})
