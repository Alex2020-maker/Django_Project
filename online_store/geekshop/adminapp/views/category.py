from unicodedata import category
from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def check_is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    return True


@user_passes_test(check_is_superuser)
def categories(request, page=1):
    title = "админка/категории"

    categories_list = ProductCategory.objects.all()
    paginator = Paginator(categories_list, 2)
    try:
        categories_paginator = paginator.page(page)
    except PageNotAnInteger:
        categories_paginator = paginator.page(1)
    except EmptyPage:
        categories_paginator = paginator.page(paginator.num_pages)

    content = {"title": title, "objects": categories_paginator}

    return render(request, "adminapp/categories.html", content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = "adminapp/category/category_update.html"
    success_url = reverse_lazy("admin:categories")
    fields = "__all__"


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = "adminapp/category/category_update.html"
    success_url = reverse_lazy("admin:categories")
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "категории/редактирование"
        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = "adminapp/category/category_delete.html"
    success_url = reverse_lazy("admin:categories")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
