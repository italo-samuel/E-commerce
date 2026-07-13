from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models
from django.contrib import messages

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
        http_referer = self.request.META['HTTP_REFERER']
        variacao_id = self.request.GET.get('vid')
        
    
        if not variacao_id:
            messages.error(self.request, 'Produto não existe')
        
        else:
            messages.success(self.request, 'Produto adicionado ao carrinho!')
        
        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            # TODO: Varição existe no carrinho
            pass
            
        else:
            # TODO: Variação não exixte no carrinho, então Adiconar produto no carrinho
            pass

        return HttpResponse(f'{variacao.produto} {variacao.nome}')

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoverDoCarrinho')

class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')