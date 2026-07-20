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
            return redirect(http_referer)
        
        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        variacao_estoque = variacao.estoque

        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        variacao_id = variacao.id
        preco_unitario = variacao.preco
        preco_unitario_promocional  = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.erro(self.request, 'Sem estoque!')
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(self.request, 
                                 f'Estoque insuficiente para {quantidade_carrinho}x no '
                                 f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                                 f'no seu carrinho')
            
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_quantitativo,
                'preco_quantitativo_promocional': preco_quantitativo_promocional,
                'quantidade': 1,
                'slug': slug, 
                'imagem': imagem,
            }

        self.request.session.save()
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