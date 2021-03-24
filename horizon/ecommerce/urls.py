from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('detalhesproduto/<int:id>',views.detalhesproduto),
    path('cart',views.cart),
    path('cadproduto',views.cadproduto),
    path('cadcor',views.cadcor),
    path('cadcategoria',views.cadcategoria),
    path('cadclientes',views.cadclientes),
    path('editacliente',views.editacliente),
    path('cart/<int:id>/<int:quantidade>',views.cart),
    path('exibecarrinho',views.exibecarrinho),
    path('deletaitemdocarrinho/<int:id>',views.deletaitemdocarrinho)
]