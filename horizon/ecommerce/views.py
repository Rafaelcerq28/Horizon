from django.shortcuts import redirect, render, get_object_or_404
from .models import Produtos
from .forms import ProdutoForm,CorForm,CategoriaForm,ClientesForm
from django.contrib.auth import get_user_model
import datetime

#página inicial
def home(request):
    #entrada_ult_30d = Movimentacoes.objects.filter(tipo_mov='entrada', created_at__gte=datetime.datetime.now()-datetime.timedelta(days=30)).count()
    lancamentos = Produtos.objects.filter(created_at__gte=datetime.datetime.now()-datetime.timedelta(days=7))
    ls = [1,2,2,2,2,2,2,2]
    return render(request,'ecommerce/index.html',{'lancamentos':lancamentos,'ls':ls})
    
#view onde exibe os detalhes do produto
def detalhesproduto(request,id):
    produto = get_object_or_404(Produtos,pk=id)
    return render(request,'ecommerce/detalhesproduto.html',{'produto':produto})

#view para exibir os itens do carrinho
def cart(request):
    return render(request,'ecommerce/cart.html')

#view para cadastrar produtos
def cadproduto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)

        if form.is_valid():
            produto = form.save()
            return redirect('/')

    form = ProdutoForm()
    return render(request,'ecommerce/cadproduto.html',{'form':form})

#view para cadastrar a cor 
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

#view para cadastrar a categoria
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

def cadclientes (request):
    if request.method == 'POST':
        formulario = request.POST
        #Guarda o nome e sobrenome retidados do input
        nome = formulario.get('nome')
        sobrenome = formulario.get('sobrenome')

        form = ClientesForm(request.POST)
        if form.is_valid():
            #Instancia o usuario
            user = request.user
            #grava o nome e o sobrenome
            user.first_name = nome
            user.last_name = sobrenome
            #grava os dados do usuario 
            user.save()
            cliente = form.save(commit=False)
            return redirect('/cadclientes')
    form = ClientesForm()
    return render(request,'ecommerce/cadclientes.html',{'form':form})