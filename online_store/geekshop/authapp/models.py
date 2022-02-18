import re
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


def default_key_expiration_date():
    return timezone.now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name="возраст", default=0)
    city = models.CharField(max_length=64, verbose_name="город", blank=True)
    phone_number = models.CharField(
        max_length=14, verbose_name="номер телефона", blank=True
    )
    avatar = models.ImageField(upload_to="user_avatars", blank=True)
    activation_key = models.CharField(
        verbose_name="ключ активации", max_length=128, null=True
    )
    activation_expiration_date = models.DateTimeField(
        verbose_name="Истечение активации", default=default_key_expiration_date
    )

    def is_activation_key_expired(self):
        return self.activation_expiration_date > timezone.now()
