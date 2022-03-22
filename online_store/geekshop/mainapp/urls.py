from django.urls import path

from mainapp import views

app_name = "mainapp"

urlpatterns = [
    path("", views.products, name="index"),
    path("category/<int:pk>/", views.products, name="category"),
    path("category/<int:pk>/page/<int:page>/", views.products, name="page"),
    path("product/<int:pk>/", views.product, name="product"),
    path("product/<int:pk>/price", views.product_price, name="product_price"),
]
