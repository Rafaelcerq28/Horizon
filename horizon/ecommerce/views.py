from django.shortcuts import redirect, render
from .models import Produtos
from .forms import ProdutoForm

def home(request):
    return render(request,'ecommerce/index.html')
# Create your views here.

def detalhesproduto(request):
    return render(request,'ecommerce/detalhesproduto.html')

def cart(request):
    return render(request,'ecommerce/cart.html')

def cadproduto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)

        if form.is_valid():
            produto = form.save()
            return redirect('/')

    form = ProdutoForm()
    return render(request,'ecommerce/cadproduto.html',{'form':form})