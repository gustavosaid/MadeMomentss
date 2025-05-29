from django.urls import path
from login import views
from login.views import (login,conta,cadastrar_usuario,loja,login_usuario, logout_view, criar_pedido,
 add_carrinho,ver_carrinho, remover_carrinho, pagamento_certo, pagamento_errado)
from login.api_mercadoPago import gerar_link_pagamento

urlpatterns = [
    #rota, view responsavel, nome de referencia
    path('', views.login, name='login'),  # Página inicial: login
    path('cadastro/', conta, name='conta'),  # Formulário de cadastro
    path('usuarios/', cadastrar_usuario, name='cadastrar_usuario'),  # POST de cadastro
    path('login/', login_usuario, name='login_usuario'),  # POST de login
    path('loja/', loja, name='loja'),  # Página da loja apos login
    path('logout/', logout_view, name='logout'), #view de logout
    path('pedido/novo/', criar_pedido, name='criar_pedido'), #criar novo pedido

    #parte dp carrinho 
    path('pedido/<int:pedido_id>/', views.detalhe_pedido, name='detalhe_pedido'), #detalhes ao clicar em comprar
    path('pedido/<int:pedido_id>/add_carrinho/', add_carrinho, name='add_carrinho'), #escolher quantidade a ser adicionada ao carrinho
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('removerCarrinho/<int:pedido_id>/', remover_carrinho, name='remover_carrinho'),
    path('compracerta/', pagamento_certo, name='pagamento_certo'),
    path('compraerrada/', pagamento_errado, name='pagamento_errado'),
    path('pagar/', gerar_link_pagamento, name='pagar'),

#     path('pedidos/', listar_pedidos, name='listar_pedidos'),
]


