import hashlib
import random

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ("username", "password")

    error_css_class = "has-error"

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            "username",
            "first_name",
            "age",
            "email",
            "city",
            "phone_number",
            "avatar",
            "password",
        )

    error_css_class = "has-error"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
            if field_name == "password":
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data["age"]
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = (
            "username",
            "first_name",
            "password1",
            "password2",
            "age",
            "email",
            "city",
            "phone_number",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""

    def clean_age(self):
        data = self.cleaned_data["age"]
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data

    def save(self):
        user = super(ShopUserRegisterForm, self).save()
        
        user.is_active = True
        salt = hashlib.sha1(str(random.random()).encode("utf8")).hexdigest()[:6]
        user.activation_key = hashlib.sha1(
            (user.email + salt).encode("utf8")
        ).hexdigest()
        user.save()

        return user


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ("tagline", "aboutMe", "gender")

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
