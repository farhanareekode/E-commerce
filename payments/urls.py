# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('payment_details', views.payments, name='payments'),
    path('initiate_payment', views.initiate_payment, name='initiate_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),

    path('payment/payment_success_print', views.payment_success_print, name='payment_success_print'),
    path('stripe-payment/', views.stripe_payment, name='stripe_payment'),
    path('stripe_payment_success/', views.payment_success_print, name='stripe_payment_success'),

]