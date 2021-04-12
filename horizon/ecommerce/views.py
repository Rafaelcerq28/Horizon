from typing import Tuple
from django.shortcuts import redirect, render, get_object_or_404
from .models import Produtos,Clientes,Categorias,Cores,Carrinho,ListaDeDesejos
from .forms import ProdutoForm,CorForm,CategoriaForm,ClientesForm,ClientesSubtotalForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import datetime

#========================================================
#==== PÁGINA INICIAL ====================================
#========================================================

#Página inicial
def home(request):
    lancamentos = Produtos.objects.all().order_by('-created_at')[:5]
    categorias = Categorias.objects.all().order_by('categoria')
    produtos_vendidos = Produtos.objects.filter(quantidade_vendida__gt = 0).order_by('-quantidade_vendida')

    if request.user.is_authenticated == True:
        #pega o id do cliente e verifica se há um cliente cadastrado com esse id, caso não haja ele encaminha para o cadastro de cliente
        cliente = Clientes.objects.filter(usuario = request.user.id).first()
        if cliente == None:
            return redirect('/cadclientes')

        carrinho = Carrinho.objects.filter(cliente = cliente.id)
    else:
        carrinho = ''
    return render(request,'ecommerce/index.html',{'lancamentos':lancamentos,'carrinho':carrinho,'categorias':categorias,'produtos_vendidos':produtos_vendidos})


#========================================================
#==== LOJA ==============================================
#========================================================

#view para acessar a loja com todos os produtos de determinada categoria
def loja(request,id):
    categorias = Categorias.objects.all().order_by('categoria')
    categoria_a_ser_buscada = get_object_or_404(Categorias,pk=id)
    produtos = Produtos.objects.filter(categoria = categoria_a_ser_buscada.id)

    return render(request,'ecommerce/loja.html',{'categorias':categorias,'produtos':produtos,'categoria_a_ser_buscada':categoria_a_ser_buscada})   


#view onde exibe os detalhes do produto
def detalhesproduto(request,id):
    produto = get_object_or_404(Produtos,pk=id)
    return render(request,'ecommerce/detalhesproduto.html',{'produto':produto})

#========================================================
#==== LISTA DE DESEJOS ==================================
#========================================================

@login_required
def listadedesejos(request,id):
    produto = get_object_or_404(Produtos,pk=id)
    cliente = get_object_or_404(Clientes,usuario = request.user.id)

    check = ListaDeDesejos.objects.filter(produto=produto,cliente=cliente)
    print(len(check))
    
    if len(check) == 0:
        ListaDeDesejos.objects.create(produto=produto,cliente=cliente)
        return redirect('/exibelistadedesejos')
    #inserir um return para a página do produto e exibir uma mensagem informando que ele foi salvo na lista de desejos
    return redirect('/exibelistadedesejos')

@login_required
def exibelistadedesejos(request):
    cliente = get_object_or_404(Clientes,usuario = request.user.id)
    lista = ListaDeDesejos.objects.filter(cliente = cliente.id)
    
    if len(lista) == 0:
        vazio = True
    else:
        vazio = False

    return render(request,'ecommerce/exibelistadedesejos.html',{'lista':lista,'vazio':vazio})

@login_required
def removelistadedesejos(request,id):
    desejo = get_object_or_404(ListaDeDesejos,pk=id)
    desejo.delete()
    return redirect('/exibelistadedesejos')

#========================================================
#==== CARRINHO ==========================================
#========================================================

#view para cadastrar os itens do carrinho
@login_required
def cart(request,id):
    cor= get_object_or_404(Cores,pk=request.GET.get('cor'))
    quantidade = request.GET.get('quantidade')
    cli = get_object_or_404(Clientes,usuario = request.user.id)
    prod = get_object_or_404(Produtos,pk=id)
    Carrinho.objects.create(cliente=cli,produto=prod,quantidade=quantidade,cor=cor)
    
    #itens = Carrinho.objects.filter(cliente = cli.id)
    return redirect('/exibecarrinho')#render(request,'ecommerce/exibecarrinho.html')


#view para exibir o carrinho
@login_required
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
    
    if len(carrinho) == 0:
        vazio = True    
    else:
        vazio = False
        
    return render(request,'ecommerce/cart.html',{'carrinho':carrinho,'produtos':produtos,'total':total,'vazio':vazio})

@login_required
def deletaitemdocarrinho(request,id):
    #deleta item do carrinho
    produto_do_carrinho = get_object_or_404(Carrinho,pk=id)
    produto_do_carrinho.delete()
    return redirect('/exibecarrinho')

@login_required
def acrescentaitemcarrinho(request,id):
    acrescenta_item = get_object_or_404(Carrinho,pk=id)
    acrescenta_item.quantidade += 1
    acrescenta_item.save()
    return redirect('/exibecarrinho')
    
@login_required
def subtraiitemcarrinho(request,id):
    subtrai_item = get_object_or_404(Carrinho,pk=id)
    if subtrai_item.quantidade > 1:
        subtrai_item.quantidade -= 1
        subtrai_item.save()
    return redirect('/exibecarrinho')

@login_required
#Subtotal e finalização da venda
def subtotal(request):
    #busca os itens no banco
    cli = get_object_or_404(Clientes,usuario=request.user)
    carrinho = Carrinho.objects.filter(cliente = cli.id)
    #cria o formulario
    form = ClientesSubtotalForm(instance=cli)

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
    
    #Verifica se a requisição é um POST
    if request.method == 'POST':
        #armazena os dados da requisição em um formulario instanciando o objeto produto
        form = ClientesSubtotalForm(request.POST,instance=cli)
        #Veridica se o formulario é valido
        if form.is_valid():
            #salva o cliente
            cli = form.save()            
            #passa por cada item do carrinho atualizando a quantidade vendida em cada um deles
            for item in carrinho:
                if item.produto.quantidade_vendida != None:
                    item.produto.quantidade_vendida += item.quantidade
                else:
                    item.produto.quantidade_vendida = item.quantidade
                #salva as modificações no produto
                item.produto.save()
            #Apaga os itens do carrinho
            carrinho.delete()

            return redirect('/vendafinalizada')
    return render(request,'ecommerce/subtotal.html',{'form':form,'cli':cli,'carrinho':carrinho,'produtos':produtos,'total':total})

#tela de venda finalizada
@login_required
def vendafinalizada(request):
    return render(request,'ecommerce/vendafinalizada.html')

#========================================================
#==== CADASTRO DE PRODUTOS ==============================
#========================================================

#view para cadastrar produtos
@login_required
def cadproduto(request):
    if request.method == 'POST':
        #pega as informações do POST e a imagem e salva na form
        form = ProdutoForm(request.POST,request.FILES)
        if form.is_valid():
            produto = form.save()
            produto.preco_desconto = produto.preco - ((produto.preco/100) * produto.percentual_desconto)
            if produto.preco_desconto <= 0:
                produto.preco_desconto = produto.preco
                produto.percentual_desconto = 0
            produto.save()
            return redirect('/')
    #manda o formulario de produto para o template
    form = ProdutoForm()
    return render(request,'ecommerce/cadproduto.html',{'form':form})


#view para cadastrar a cor 
@login_required
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
@login_required
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

#========================================================
#==== CADASTRO DE CLIENTES ==============================
#========================================================

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