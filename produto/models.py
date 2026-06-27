from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField(max_length=255)
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples')
        )
    )


class Variacao(models.Model):
    nome = models.CharField(max_length=255)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    preco = models.FloatField()
    preco_promocional = models.FloatField()
    estoque = models.IntegerField()