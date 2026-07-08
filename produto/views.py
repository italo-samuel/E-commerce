from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 6

    def get_queryset(self):
        # 1. Pega o QuerySet padrão (que traz todos os produtos)
        queryset = super().get_queryset()
        
        # 2. Captura o parâmetro 'categoria' enviado pela URL (?categoria=ID)
        # Nas CBVs, o 'request' fica guardado dentro de 'self.request'
        categoria_id = self.request.GET.get('categoria')
        
        # 3. Se houver um ID na URL, filtra os produtos por essa categoria
        if categoria_id:
            queryset = queryset.filter(categoria__id=categoria_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        # 1. Pega o contexto padrão da ListView (que já contém a paginação e os produtos)
        context = super().get_context_data(**kwargs)
        
        # 2. Adiciona a lista de todas as categorias no contexto do template
        context['categorias'] = models.Categoria.objects.all()
        
        return context

''''''
class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AdicionarAoCarrinho')

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinho')

class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')