from django.urls import path
from adminapp.views import product

urlpatterns = [
    path('products/create/category/<int:pk>/', product.product_create, name='product_create'),
    path('products/read/category/<int:pk>/', product.products, name='products'),
    path('products/read/<int:pk>/', product.product_read, name='product_read'),
    path('products/update/<int:pk>/', product.product_update, name='product_update'),
    path('products/delete/<int:pk>/', product.product_delete, name='product_delete'),
    path('products/<int:pk>/page/<int:page>/', product.products, name='page'),
]

