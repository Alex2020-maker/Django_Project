import profile
from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from authapp.models import ShopUserProfile
from mainapp.utils import get_or_create


class Command(BaseCommand):
    help = "Create user profiles"

    def handle(self, *args, **options):
        for user in ShopUser.objects.all():
            get_or_create(ShopUserProfile, user=user)
