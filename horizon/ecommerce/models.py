from django.db import models
from django.contrib.auth import get_user_model
from django.forms.widgets import SelectDateWidget

class Produtos(models.Model):
    nome = models.CharField(max_length=255,null=False,blank=False)
    preco = models.FloatField(null=False,blank=False)
    preco_desconto = models.FloatField()
    percentual_desconto = models.IntegerField()
    categoria = models.ForeignKey('Categorias',on_delete=models.CASCADE)
    descricao = models.TextField(null=True)
    especificacoes = models.TextField(null=False,blank=True)
    quantidade_estoque = models.IntegerField(null=False,blank=False)
    quantidade_vendida = models.IntegerField(blank=True,null=True)
    cor = models.ManyToManyField('Cores')
    imagem = models.ImageField(null=True,blank=True, upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nome

class Cores (models.Model):
    class Meta:
        ordering = ['cor']
    
    cor = models.CharField(max_length=255,blank=False,null=False,unique=True)

    def __str__(self) -> str:
        return self.cor

class Categorias (models.Model):
    class Meta:
        ordering = ['categoria']
    
    categoria = models.CharField(max_length=255,blank=False,null=False,unique=True)

    def __str__(self) -> str:
        return self.categoria
    
class Clientes (models.Model):

    STATUS = (
        ('m','Masculino'),
        ('m','Feminino'),
        ('outros','Outros')
    )

    usuario = models.ForeignKey(get_user_model(),on_delete = models.CASCADE)
    #nome = models.CharField(max_length=255,blank=False,null=False)
    endereco = models.CharField(max_length=255,blank=False,null=False)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=255,null=False)
    cep = models.CharField(max_length=8,blank=False,null=False)
    telefone = models.CharField(max_length=11,blank=False,null=False)
    cpf = models.CharField(max_length=11,blank=False,null=False)
    rg = models.CharField(max_length=9,blank=False,null=False)
    sexo = models.CharField(max_length=1,choices=STATUS)
    idade = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.usuario.first_name

class Carrinho (models.Model):
    cliente = models.ForeignKey('Clientes',on_delete=models.CASCADE)    
    produto = models.ForeignKey('Produtos',on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.cliente.id) + ' - ' + str(self.produto.id)   
