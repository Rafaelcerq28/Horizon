from django.shortcuts import redirect, render, get_object_or_404
from .models import Produtos
from .forms import ProdutoForm,CorForm,CategoriaForm

def home(request):
    return render(request,'ecommerce/index.html')
# Create your views here.

def detalhesproduto(request,id):
    produto = get_object_or_404(Produtos,pk=id)
    return render(request,'ecommerce/detalhesproduto.html',{'produto':produto})

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

def cadcor(request):
    if request.method == 'POST':
        form = CorForm(request.POST)

        if form.is_valid():
            cores = form.save(commit=False)
            if cores.cor.isnumeric():
                return redirect('/cadcor')
            else:
                cores.cor = cores.cor.capitalize()
                cores.save()
                return redirect('/cadproduto')
    form = CorForm()
    return render(request,'ecommerce/cadcor.html',{'form':form})

def cadcategoria (request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categ = form.save(commit=False)
            
            categ.categoria = categ.categoria.capitalize()
            categ.save()
            return redirect('/cadproduto')

    form = CategoriaForm()
    return render(request,'ecommerce/cadcategoria.html',{'form':form})