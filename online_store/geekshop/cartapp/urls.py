from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart, name="view"),
    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:pk>)/", views.remove_from_cart, name="remove_from_cart"),
    path("edit/<int:pk>/<int:quantity>/", views.cart_edit, name="edit"),
]
