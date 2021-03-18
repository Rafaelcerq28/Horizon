from django import forms
from django.forms import fields, widgets
from .models import Produtos

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = {'nome','preco','preco_desconto','percentual_desconto','descricao','especificacoes','quantidade_estoque'}

