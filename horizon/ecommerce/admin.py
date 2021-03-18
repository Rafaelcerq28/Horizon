from django.contrib import admin

# Register your models here.
from .models import Produtos, Cores, Categorias, Clientes, Carrinho

admin.site.register(Produtos)
admin.site.register(Cores)
admin.site.register(Categorias)
admin.site.register(Clientes)
admin.site.register(Carrinho)