from django import forms
from django.forms import fields, widgets
from .models import Produtos, Categorias, Cores

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = {'nome','preco','preco_desconto','percentual_desconto','descricao','especificacoes','quantidade_estoque','categoria','cor'}


class CorForm(forms.ModelForm):
    class Meta:
        model = Cores
        fields = {'cor'}

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = {'categoria'}