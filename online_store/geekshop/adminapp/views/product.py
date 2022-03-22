from django.shortcuts import render, get_object_or_404
from adminapp.forms import EditProductsForm
from mainapp.models import ProductCategory, Product
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def products(request, pk, page=1):

    title = "админка/продукт"

    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category__pk=pk).order_by("name")

    paginator = Paginator(products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    content = {"title": title, "category": category, "objects": products_paginator}
    return render(request, "adminapp/products.html", content)


def product_create(request, pk):
    title = "продукт/создать"

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == "POST":
        product_form = EditProductsForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse("admin:products", args=[pk]))
    else:
        product_form = EditProductsForm(initial={"category": category})

    content = {"title": title, "update_form": product_form, "category": category}

    return render(request, "adminapp/product/product_update.html", content)


def product_read(request, pk):
    title = "продукт/подробнее"

    product = get_object_or_404(Product, pk=pk)
    content = {
        "title": title,
        "object": product,
    }

    return render(request, "adminapp/product/product_read.html", content)


def product_update(request, pk):
    title = "продукт/редактирование"

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        edit_form = EditProductsForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(
                reverse("admin:product_update", args=[edit_product.pk])
            )
    else:
        edit_form = EditProductsForm(instance=edit_product)

    content = {
        "title": title,
        "update_form": edit_form,
        "category": edit_product.category,
    }

    return render(request, "adminapp/product/product_update.html", content)


def product_delete(request, pk):
    title = "продукт/удаление"

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return HttpResponseRedirect(
            reverse("admin:products", args=[product.category.pk])
        )

    content = {"title": title, "product_to_delete": product}

    return render(request, "adminapp/product/product_delete.html", content)
