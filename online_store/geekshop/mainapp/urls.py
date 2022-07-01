from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp import views

app_name = "mainapp"

urlpatterns = [
    path("", views.products, name="index"),
    path("category/<int:pk>/", views.products, name="category"),
    path("category/<int:pk>/page/<int:page>/", views.products, name="page"),
    path("product/<int:pk>/", views.product, name="product"),

    # AJAX views
    path("category/<int:pk>/ajax/", cache_page(3600)(views.products_ajax), name="category_ajax"),
    path("category/<int:pk>/page/<int:page>/ajax/", views.products_ajax, name="page_ajax"),
]
