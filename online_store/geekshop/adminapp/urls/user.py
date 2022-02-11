from django.urls import path
import adminapp.views as adminapp
from adminapp.views import user


urlpatterns = [
    path('users/create/', user.user_create, name='user_create'),
    path('users/read/', user.UserList.as_view(), name='users'),
    path('users/update/<int:pk>/', user.user_update, name='user_update'),
    path('users/delete/<int:pk>/', user.user_delete, name='user_delete'),
]

