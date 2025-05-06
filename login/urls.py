from django.urls import path
from login import views
from login.views import (login,conta,cadastrar_usuario,loja,login_usuario, logout_view, criar_pedido)

urlpatterns = [
    #rota, view responsavel, nome de referencia
    path('', views.login, name='login'),  # Página inicial: login
    path('cadastro/', conta, name='conta'),  # Formulário de cadastro
    path('usuarios/', cadastrar_usuario, name='cadastrar_usuario'),  # POST de cadastro
    path('login/', login_usuario, name='login_usuario'),  # POST de login
    path('loja/', loja, name='loja'),  # Página da loja após login
    path('logout/', logout_view, name='logout'), #view de logout
    path('pedido/novo/', criar_pedido, name='criar_pedido'), #criar novo pedido
#     path('pedidos/', listar_pedidos, name='listar_pedidos'),
]


