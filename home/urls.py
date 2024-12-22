from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='home' ),#calling

    #path(url_name, function(module.function_name),name of path)
    path('search',views.searching, name='search'),
    path('home/search',views.searching, name='search'),

    path('page/<int:page_num>/', views.home, name='home_paginated'),

    path('about',views.about, name='about'),
    path('blog',views.blog, name='blog'),
    # path('contact',views.contact, name='contact'),
    path('<slug:category_slug>/<slug:product_slug>/product_single/',views.product_single, name='product_single'),
    # path('category/<slug:slug>/',views.category_products, name='category_products'),
    path('<slug:category_slug>',views.home, name='category' ),

]