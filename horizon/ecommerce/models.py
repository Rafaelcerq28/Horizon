from django.db import models

class Produtos(models.Model):
    nome = models.CharField(max_length=255,null=False,blank=False)
    preco = models.FloatField(null=False,blank=False)
    preco_desconto = models.FloatField(null=False,blank=False)
    percentual_desconto = models.IntegerField()
    #categoria = models.ForeignKey(Categorias,on_delete=models.CASCADE)
    descricao = models.TextField(null=False)
    especificacoes = models.TextField(null=False,blank=False)
    quantidade_estoque = models.IntegerField(null=False,blank=False)
    #cor = models.ManyToManyField("Cores")
    #imegem = models.ForeignKey(Imagens,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.modelo
