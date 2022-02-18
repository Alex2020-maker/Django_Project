from .category import urlpatterns as category
from .product import urlpatterns as product
from .user import urlpatterns as user

app_name = "adminapp"

urlpatterns = [*category, *product, *user]
