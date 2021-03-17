from django.shortcuts import render

def home(request):
    return render(request,'ecommerce/index.html')
# Create your views here.

def detalhesproduto(request):
    return render(request,'ecommerce/detalhesproduto.html')

def cart(request):
    return render(request,'ecommerce/cart.html')