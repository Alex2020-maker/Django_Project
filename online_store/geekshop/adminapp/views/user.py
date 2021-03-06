from django.views.generic.list import ListView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from authapp.models import ShopUser
from operator import attrgetter
from django.contrib.auth.decorators import user_passes_test
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm
from django.utils.decorators import method_decorator


def check_is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    return True


class UserList(ListView):
    template_name = "adminapp/users.html"
    models = ShopUser

    def get_queryset(self):
        return ShopUser.objects.all().order_by(
            "-is_active", "-is_superuser", "-is_staff", "username"
        )


@user_passes_test(check_is_superuser)
def user_create(request):

    title = "пользователи/создание"

    if request.method == "POST":
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("admin:users"))
    else:
        user_form = ShopUserRegisterForm()

    content = {"title": title, "update_form": user_form}

    return render(request, "adminapp/user/user_update.html", content)


@user_passes_test(check_is_superuser)
def user_update(request, pk):

    title = "пользователи/редактирование"

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        edit_form = ShopUserAdminEditForm(
            request.POST, request.FILES, instance=edit_user
        )
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(
                reverse("admin:user_update", args=[edit_user.pk])
            )
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {"title": title, "update_form": edit_form}

    return render(request, "adminapp/user/user_update.html", content)


@user_passes_test(check_is_superuser)
def user_delete(request, pk):

    title = "пользователи/удаление"

    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse("admin:users"))

    content = {"title": title, "user_to_delete": user}

    return render(request, "adminapp/user/user_delete.html", content)
