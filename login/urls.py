from django.urls import path
from login import views
from login.views import (login_view, conta, cadastrar_usuario, loja, login_usuario, logout_view, criar_pedido,
                        add_carrinho, ver_carrinho, remover_carrinho, pagamento_certo, pagamento_errado,
                        visualizar_perfil, cadastrar_endereco)
from login.api_mercadoPago import gerar_link_pagamento

urlpatterns = [
    # Página inicial de login
    path('', loja, name='loja'),  # Página inicial
    path('login/', views.login_view, name='login'), 
    path('cadastro/', conta, name='conta'),  # Mostra o formulário
    path('cadastro/salvar/', cadastrar_usuario, name='cadastrar_usuario'),  # Processa o POST  # Formulário de cadastro
    path('usuarios/', cadastrar_usuario, name='cadastrar_usuario'),  # POST de cadastro
    path('login/', login_usuario, name='login_usuario'),  # POST de login
    path('logout/', logout_view, name='logout'), # View de logout
    path('pedido/novo/', criar_pedido, name='criar_pedido'), # Criar novo pedido
    path('perfil/', visualizar_perfil, name='visualizar_perfil'), # Criar novo pedido
    path('endereco/', cadastrar_endereco, name='cadastrar_endereco'), # Criar novo pedido

    # Parte do carrinho
    path('pedido/<int:pedido_id>/', views.detalhe_pedido, name='detalhe_pedido'), # Detalhes ao clicar em comprar
    path('pedido/<int:pedido_id>/add_carrinho/', add_carrinho, name='add_carrinho'), # Escolher quantidade a ser adicionada ao carrinho
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('removerCarrinho/<int:pedido_id>/', remover_carrinho, name='remover_carrinho'),
    path('compracerta/', pagamento_certo, name='pagamento_certo'),
    path('compraerrada/', pagamento_errado, name='pagamento_errado'),
    path('pagar/', gerar_link_pagamento, name='pagar'),
    path('verify-2fa/', views.verify_mfa, name='verify_mfa'), 

    # URLs do painel de administração
    path('painel/', views.painel_admin, name='painel_admin'),
    path('painel/adicionar/', views.adicionar_pedido, name='adicionar_pedido'),
    path('painel/editar/<int:pedido_id>/', views.editar_pedido, name='editar_pedido'),
    path('painel/excluir/<int:pedido_id>/', views.excluir_pedido, name='excluir_pedido'),
]
