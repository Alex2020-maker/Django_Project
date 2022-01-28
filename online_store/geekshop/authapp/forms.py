from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django import forms

from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ("username", "password")

    error_css_class = "has-error"

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class KazanRestrictionMixin:
    def clean_city(self):
        city_name = self.cleaned_data["city"]
        if city_name != "Казань":
            raise forms.ValidationError("Только для жителей Казани")

        return city_name


class ShopUserEditForm(KazanRestrictionMixin, UserChangeForm):
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


class ShopUserRegisterForm(KazanRestrictionMixin, UserCreationForm):
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
