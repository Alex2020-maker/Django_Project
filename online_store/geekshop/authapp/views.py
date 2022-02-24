from django.contrib import auth
from django.db import transaction
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from authapp.forms import (
    ShopUserEditForm,
    ShopUserLoginForm,
    ShopUserProfile,
    ShopUserProfileEditForm,
    ShopUserRegisterForm,
)
from authapp.models import ShopUser
from authapp.utils import send_verify_mail


def register(request):
    title = "регистрация"

    if request.method == "POST":
        register_form = ShopUserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save()
            send_verify_mail(user)
            return HttpResponseRedirect(reverse("auth:login"))
    else:
        register_form = ShopUserRegisterForm()

    content = {"title": title, "register_form": register_form}

    return render(request, "authapp/register.html", content)


@transaction.atomic
def edit(request):
    title = "редактирование"

    if request.method == "POST":
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(
            request.POST, instance=request.user.shopuserprofile
        )
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse("auth:edit"))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {"title": title, "edit_form": edit_form, "profile_form": profile_form}

    return render(request, "authapp/edit.html", content)


def login(request):
    title = "вход"

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == "POST" and login_form.is_valid():
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("index"))

    content = {"title": title, "login_form": login_form}
    return render(request, "authapp/login.html", content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if (
            user.activation_key == activation_key
            and not user.is_activation_key_expired()
        ):
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, "authapp/verification.html")
        else:
            print(f"error activation user: {user}")
            return render(request, "authapp/verification.html")
    except Exception as e:
        print(f"error activation user : {e.args}")
        return HttpResponseRedirect(reverse("index"))
