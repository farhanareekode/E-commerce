from django.urls import path
from . import views

urlpatterns = [
    path('cart_details/', views.cart_details, name='cart_details'),
    path('add_cart/<int:pk>/', views.add_cart, name='add_cart'),
    path('min_cart/<int:pk>/', views.min_cart, name='min_cart'),
    path('cart_delete/<int:pk>/', views.cart_delete, name='cart_delete'),



]

