from dataclasses import field

from gettext import translation
from multiprocessing import context

from cartapp.models import Cart
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ordersapp.models import Order, OrderItem

from .forms import OrderForm, OrderItemForm
from django.http import JsonResponse
from mainapp.models import Product


# Create your views here.

# Использование декларативного метода
class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# Форма создания заказа
class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy("ordersapp:orders_list")

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            cart_items = Cart.get_items(self.request.user)
            if len(cart_items):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=len(cart_items)
                )
                formset = OrderFormSet()
                for form, cart_item in zip(formset.forms, cart_items):
                    form.initial["product"] = cart_item.product
                    form.initial["quantity"] = cart_item.quantity
                    form.initial["price"] = cart_item.product.price

                cart_items.delete()
            else:
                formset = OrderFormSet()

        data["orderitems"] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


# Форма чтения заказа
class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context["title"] = "заказ/просмотр"
        return context


# Форма удаления заказа
class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy("ordersapp:orders_list")


# Форма редактирования заказа
class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy("order:orders_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )

        if self.request.POST:
           data['orderitems'] = OrderFormSet(self.request.POST,
                                             instance=self.object)
        else:
           formset = OrderFormSet(instance=self.object)
           for form in formset.forms:
               if form.instance.pk:
                   form.initial['price'] = form.instance.product.price
           data['orderitems'] = formset
           
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse("ordersapp:orders_list"))

def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=int(pk)).first()
    if product:
        return JsonResponse({'price': product.price})
    else:
        return JsonResponse({'price': 0})
