from django.shortcuts import redirect, render, get_object_or_404
from .models import Produtos,Clientes,Categorias,Cores,Carrinho
from .forms import ProdutoForm,CorForm,CategoriaForm,ClientesForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import datetime

#Página inicial
def home(request):
    lancamentos = Produtos.objects.filter(created_at__gte=datetime.datetime.now()-datetime.timedelta(days=7))
    ls = [1,2,2,2,2,2,2,2]
    if request.user.is_authenticated == True:
        #pega o id do cliente e verifica se há um cliente cadastrado com esse id, caso não haja ele encaminha para o cadastro de cliente
        cliente = Clientes.objects.filter(usuario = request.user.id).first()
        if cliente == None:
            return redirect('/cadclientes')

        carrinho = Carrinho.objects.filter(cliente = cliente.id)
    else:
        carrinho = ''
    return render(request,'ecommerce/index.html',{'lancamentos':lancamentos,'ls':ls,'carrinho':carrinho})
    
#view onde exibe os detalhes do produto
def detalhesproduto(request,id):
    produto = get_object_or_404(Produtos,pk=id)
    return render(request,'ecommerce/detalhesproduto.html',{'produto':produto})


#view para cadastrar os itens do carrinho
@login_required
def cart(request,id):
    cor= get_object_or_404(Cores,pk=request.GET.get('cor'))
    quantidade = request.GET.get('quantidade')
    cli = get_object_or_404(Clientes,usuario = request.user.id)
    prod = get_object_or_404(Produtos,pk=id)
    Carrinho.objects.create(cliente=cli,produto=prod,quantidade=quantidade,cor=cor)
    
    itens = Carrinho.objects.filter(cliente = cli.id)
    return redirect('/exibecarrinho')#render(request,'ecommerce/exibecarrinho.html')

#view para exibir o carrinho
def exibecarrinho(request):
    cli = get_object_or_404(Clientes,usuario = request.user.id)
    #itens do carrinho
    carrinho = Carrinho.objects.filter(cliente = cli.id)
    
    #operação para gerar os produtos, quantidades e valores atualizados
    produtos = []
    total = 0
    for item in carrinho:
        #lê cada um dos itens e salva em uma lista
        obj = []
        obj.append(item.quantidade)
        obj.append(item.produto.nome)
        obj.append(item.quantidade * item.produto.preco)
        #grava a lista com os itens em uma outra lista
        produtos.append(obj)
        #calcula os totais 
        total += (item.quantidade * item.produto.preco)

    
    return render(request,'ecommerce/cart.html',{'carrinho':carrinho,'produtos':produtos,'total':total})

def deletaitemdocarrinho(request,id):
    #deleta item do carrinho
    produto_do_carrinho = get_object_or_404(Carrinho,pk=id)
    produto_do_carrinho.delete()
    return redirect('/exibecarrinho')

def acrescentaitemcarrinho(request,id):
    acrescenta_item = get_object_or_404(Carrinho,pk=id)
    acrescenta_item.quantidade += 1
    acrescenta_item.save()
    return redirect('/exibecarrinho')
    
def subtraiitemcarrinho(request,id):
    subtrai_item = get_object_or_404(Carrinho,pk=id)
    if subtrai_item.quantidade > 1:
        subtrai_item.quantidade -= 1
        subtrai_item.save()
    return redirect('/exibecarrinho')

#view para cadastrar produtos
def cadproduto(request):
    if request.method == 'POST':
        #pega as informações do POST e a imagem e salva na form
        form = ProdutoForm(request.POST,request.FILES)
        if form.is_valid():
            produto = form.save()
            return redirect('/')
    #manda o formulario de produto para o template
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

#view para cadastro de cliente
def cadclientes (request):
    #verifica se há um cliente com esse id cadastrado, caso não haja ele segue com o cadastro
    existecliente = Clientes.objects.filter(usuario = request.user.id).first()
    if existecliente != None:
        return redirect('/')

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
            cliente.usuario = user
            cliente.save()
            return redirect('/cadclientes')
    form = ClientesForm()
    return render(request,'ecommerce/cadclientes.html',{'form':form})

#view para editar cliente
def editacliente (request):
    cliente = get_object_or_404(Clientes,usuario=request.user.id)
    #nome e sobrenome do usuario para mandar para a view
    nome = cliente.usuario.first_name
    sobrenome = cliente.usuario.last_name

    form = ClientesForm(instance=cliente)
    if request.method == 'POST':
        form = ClientesForm(request.POST,instance=cliente)
        formulario = request.POST
        #pega o nome e sobrenome do input
        nome = formulario.get('nome')
        sobrenome = formulario.get('sobrenome')
        if form.is_valid():
            #grava o nome e o sobrenome do usuario
            user = request.user
            user.first_name = nome
            user.last_name = sobrenome
            #salva o formulario e o usuario
            form.save()
            user.save()

            return redirect('/editacliente')
        else:
            return render(request,'ecommerce/editacliente',{'form':form,'nome':nome,'sobrenome':sobrenome})
    return render(request,'ecommerce/editacliente.html',{'form':form,'nome':nome,'sobrenome':sobrenome})