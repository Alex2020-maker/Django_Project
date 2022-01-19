from django.db import models
from django.contrib.auth.models import AbstractUser

class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name = 'возраст', default=0)  
    city = models.CharField(max_length=64, verbose_name='город', blank=True)
    phone_number =  models.CharField(max_length=14, verbose_name='номер телефона', blank=True) 
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
