from .models import Carrinho  # Importe seu modelo de itens no carrinho, se tiver

def carrinho_contexto(request):
    carrinho = request.session.get('carrinho', {})
    
    # Se você estiver usando o banco (modelo ItemCarrinho), substitua pelo queryset
    # Por exemplo:
    # itens = ItemCarrinho.objects.filter(usuario=request.user) if request.user.is_authenticated else []

    total_itens = sum(carrinho.values())

    
    return {
        'carrinho': carrinho,
        'total_itens_carrinho': total_itens,
    }
