from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('detalhesproduto',views.detalhesproduto),
    path('cart',views.cart),
]