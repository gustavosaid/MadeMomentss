import mercadopago
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from .models  import Pedido 

def gerar_link_pagamento(request):
    sdk = mercadopago.SDK("APP_USR-196813989457405-052710-78cdc9696d2d484a8350fd468c79024b-482306893")

    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        return JsonResponse({"erro": "Carrinho vazio"}, status=400)

    items = []
    for pedido_id, quantidade in carrinho.items():
        pedido = get_object_or_404(Pedido, id=pedido_id)

        items.append({
            "title": pedido.descricao,  # ou pedido.nome, depende do seu modelo
            "quantity": quantidade,
            "unit_price": float(pedido.valor),
            "currency_id": "BRL"
        })

    payment_data = {
        "items": items,
        "back_urls": {
            "success": "http://127.0.0.1:8000/compracerta/",
            "pending": "http://127.0.0.1:8000/compraerrada/",
            "failure": "http://127.0.0.1:8000/pagamento_errado/",
        },
        #"auto_return": "all"
    }


    result = sdk.preference().create(payment_data)
    payment = result.get("response", {})

    if "init_point" not in payment:
        return JsonResponse({"erro": "init_point não encontrado", "detalhes": payment}, status=500)

    return HttpResponseRedirect(payment["init_point"])
