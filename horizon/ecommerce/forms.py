from django import forms
from django.forms import fields, widgets
from django.utils.translation import ugettext_lazy as _
from .models import Produtos, Categorias, Cores, Clientes

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = {'nome','preco','percentual_desconto','descricao','especificacoes','quantidade_estoque','categoria','cor','imagem'}


class CorForm(forms.ModelForm):
    class Meta:
        model = Cores
        fields = {'cor'}

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = {'categoria'}

class ClientesForm (forms.ModelForm):
    class Meta:
        model = Clientes
        fields = {'endereco','numero','complemento','cidade','estado','cep','telefone','cpf','rg','sexo','idade'}

        labels = {
            'endereco': _('Endereço',),
            'numero': _('Número'),
            'cep': _('CEP'),
            'cpf': _('CPF'),
            'rg': _('RG'),
        }


class ClientesSubtotalForm (forms.ModelForm):
    class Meta:
        model = Clientes
        fields = {'endereco','numero','complemento','cidade','estado','cep','telefone'}

        labels = {
            'endereco': _('Endereço',),
            'numero': _('Número'),
            'cep': _('CEP'),
            'cpf': _('CPF'),
            'rg': _('RG'),
        }
