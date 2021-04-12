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
    path('cart/<int:id>',views.cart),
    path('exibecarrinho',views.exibecarrinho),
    path('deletaitemdocarrinho/<int:id>',views.deletaitemdocarrinho),
    path('acrescentaitemcarrinho/<int:id>',views.acrescentaitemcarrinho),
    path('subtraiitemcarrinho/<int:id>',views.subtraiitemcarrinho),
    path('subtotal',views.subtotal),
    path('vendafinalizada',views.vendafinalizada),
    path('loja/<int:id>',views.loja),
    path('listadedesejos/<int:id>',views.listadedesejos),
    path('exibelistadedesejos',views.exibelistadedesejos),
    path('removelistadedesejos/<int:id>',views.removelistadedesejos),
]