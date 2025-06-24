from hashlib import scrypt
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .models import Create_User, Pedido, Endereco
from django.contrib.auth.hashers import make_password #criptografar senha
from django.contrib import messages 
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from .forms import PedidoForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from login.api_mercadoPago import gerar_link_pagamento
from django.contrib.auth import login as auth_login
import pyotp
import qrcode
from io import BytesIO
import base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

def login_view(request):
    return render(request, 'login/login.html')


def conta(request):
    return render(request, 'login/cadastro.html')

@csrf_exempt
@login_required
def cadastrar_endereco(request):
    usuario = request.user

    # Verifica se o usuário já tem endereço cadastrado
    endereco = Endereco.objects.filter(userEndereco=usuario).first()

    if request.method == 'POST':
        cep = request.POST.get("cep")
        endereco_txt = request.POST.get("endereco")
        bairro = request.POST.get("bairro")
        numero = request.POST.get("numero")
        complemento = request.POST.get("complemento")

        if endereco:
            # Atualiza o endereço existente
            endereco.cep = cep
            endereco.endereco = endereco_txt
            endereco.bairro = bairro
            endereco.numero = numero
            endereco.complemento = complemento
            endereco.save()
            messages.success(request, "Endereço atualizado com sucesso!")
        else:
            # Cria um novo endereço se não existir
            Endereco.objects.create(
                userEndereco=usuario,
                cep=cep,
                endereco=endereco_txt,
                bairro=bairro,
                numero=numero,
                complemento=complemento
            )
            messages.success(request, "Endereço cadastrado com sucesso!")

        return redirect('pagar')

    # Envia os dados existentes (se houver) para o template
    context = {'endereco': endereco}
    return render(request, 'login/endereco.html', context)


@login_required
def visualizar_perfil(request):
    usuario = request.user
    endereco = Endereco.objects.filter(userEndereco=usuario).first()

    if request.method == 'POST':
        # Dados do usuário
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')

        # Dados do endereço
        cep = request.POST.get('cep')
        endereco_txt = request.POST.get('endereco')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento')

        # Atualiza dados do usuário
        usuario.nome = nome
        usuario.telefone = telefone
        usuario.save()

        # Atualiza ou cria endereço
        if endereco:
            endereco.cep = cep
            endereco.endereco = endereco_txt
            endereco.bairro = bairro
            endereco.numero = numero
            endereco.complemento = complemento
            endereco.save()
        else:
            Endereco.objects.create(
                userEndereco=usuario,
                cep=cep,
                endereco=endereco_txt,
                bairro=bairro,
                numero=numero,
                complemento=complemento
            )

        messages.success(request, 'Dados atualizados com sucesso!')
        return redirect('visualizar_perfil')

    context = {
        'usuario': usuario,
        'endereco': endereco
    }
    return render(request, 'login/perfil.html', context)

def loja(request):
    pedidos = Pedido.objects.all()
    usuario = None

    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Create_User.objects.get(id=usuario_id)
        except Create_User.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")

    context = {
        'usuario': usuario,
        'pedidos': pedidos,
    }

    return render(request, 'loja/home.html', context)


def cadastrar_usuario(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("password")  
        telefone = request.POST.get("telefone")
        cpf = request.POST.get("cpf")

        if Create_User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return redirect('conta')

        if Create_User.objects.filter(cpf=cpf).exists():
            messages.error(request, "Este CPF já está cadastrado.")
            return redirect('conta')

        try:
            novo_usuario = Create_User.objects.create_user(
                email=email,
                nome=nome,
                password=senha,  
                telefone=telefone,
                cpf=cpf,
                mfa_secret=pyotp.random_base32(),
                mfa_enabled=True
            )

            if novo_usuario.mfa_enabled:
                img_str = gerar_qrcode_para(novo_usuario)
                request.session['temp_user_id'] = novo_usuario.id
                context = {
                    'user_id': novo_usuario.id,
                    'qr_code': img_str,
                    'usuario': novo_usuario,
                }
                return render(request, 'login/otp_verify.html', context)

            auth_login(request, novo_usuario)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('loja')

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar: {e}")
            return redirect('conta')

    return redirect('conta')

@csrf_exempt
def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")

        usuario = authenticate(request, email=email, password=senha)

        if usuario is not None:
            auth_login(request, usuario)
            request.session['usuario_id'] = usuario.id
            messages.success(request, f"Bem-vindo, {usuario.nome}!")
            return redirect('loja')
        else:
            messages.error(request, "E-mail ou senha incorretos.")
            return redirect('login')

    return render(request, 'loja/home.html')


@csrf_exempt
def verify_mfa(request):
    if request.method == 'POST':
        # Pegando os dados passados por parâmetro
        otp = request.POST.get('otp_code')
        user_id = request.POST.get('user_id')

        # Busca o usuário no banco
        try:
            user = Create_User.objects.get(id=user_id)
        except Create_User.DoesNotExist:
            messages.error(request, 'Usuário inválido.')
            return redirect('login')

        totp = pyotp.TOTP(user.mfa_secret)

        # Cria uma instância TOTP usando o segredo do usuário para verificar o código
        if totp.verify(otp):
            # Verifica se o código digitado está certo dentro do intervalo
            # Se der certo, vai para a loja
            request.session['usuario_id'] = user.id
            auth_login(request, user)
            messages.success(request, f"Login com 2FA bem-sucedido!")
            return redirect('loja')
        else:
            messages.error(request, 'Código OTP inválido. Tente novamente.')
            qr_code = gerar_qrcode_para(user)
            return render(request, 'login/otp_verify.html', {
                'user_id': user.id,
                'usuario': user,
                'qr_code': qr_code,
            })

    return redirect('login')


# Define uma função auxiliar para gerar o QR Code
def gerar_qrcode_para(usuario):
    # Cria a instância TOTP com o segredo do usuário.
    totp = pyotp.TOTP(usuario.mfa_secret)

    # Gera a URI padrão
    uri = totp.provisioning_uri(name=usuario.email, issuer_name="MadeMoments")

    # Gera a imagem QR code com a URI
    qr = qrcode.make(uri)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")

    # Codifica a imagem em base64 para ser embutida no HTML.
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # isso limpa as mensagens pendentes
    return redirect('login')


# Formulário para o administrador adicionar novos pedidos
@csrf_exempt
def criar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido cadastrado com sucesso!')
            # return redirect('/loja')
    else:
        form = PedidoForm()
    return render(request, 'loja/add_pedido.html', {'form': form})


# Leva para a página de detalhes do pedido ao clicar em comprar
@csrf_exempt
def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'loja/detalhe_pedido.html', {'pedido': pedido})


# Leva para a página de adicionar ao carrinho e escolher a quantidade que vai ser comprada
@csrf_exempt
def add_carrinho(request, pedido_id):
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))
        pedido = get_object_or_404(Pedido, id=pedido_id)

        carrinho = request.session.get('carrinho', {})

        # Armazena o pedido no carrinho com a quantidade
        carrinho[str(pedido_id)] = carrinho.get(str(pedido_id), 0) + quantidade

        request.session['carrinho'] = carrinho

        # ✅ Redireciona para a página do carrinho após adicionar
        return redirect('ver_carrinho')  # Certifique-se de que essa URL existe

    # # ✅ Redireciona caso o método não seja POST
    # return redirect('home')  # ou qualquer página que faça sentido


def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens = []
    total = 0

    for pedido_id, quantidade in carrinho.items():
        pedido = get_object_or_404(Pedido, id=pedido_id)
        subtotal = pedido.valor * quantidade
        total += subtotal
        itens.append({
            'pedido': pedido,
            'quantidade': quantidade,
            'subtotal': quantidade * pedido.valor,
        })

    context = {
        'itens': itens,
        'total_geral': total,
    }

    return render(request, 'loja/itens_carrinho.html', context)


@csrf_exempt
def remover_carrinho(request, pedido_id):
    carrinho = request.session.get('carrinho', {})

    if str(pedido_id) in carrinho:
        del carrinho[str(pedido_id)]
        request.session['carrinho'] = carrinho

    return redirect('ver_carrinho')


def pagamento_certo(request):
    return render(request, 'loja/mercado_pagoCerta.html')


def pagamento_errado(request):
    return render(request, 'loja/mercado_pagoErrada.html')



###LUIS HENRIQUE ZAZAZAZZZZZZ E ZAZZ O CODIGO FIUNCIONAR - LOKO SONHADOR E ZAZZZZ
###### ARRUMAR OS MEUS IMPORTS QUEM MEXER NISSO AQUI POR FAVOR JOGAR TODOS FROM PARA O TOPO DO ARQUVIO

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido
from .forms import PedidoForm  


def is_admin(user):
    return getattr(user, 'is_staff', False)

@csrf_exempt
@login_required
@user_passes_test(is_admin, login_url='loja')
def painel_admin(request):
    pedidos = Pedido.objects.all()
    return render(request, 'admin/painel_admin.html', {'pedidos': pedidos})

# ADD PRODUTOZZZZZZZZZZ
@csrf_exempt
@login_required
@user_passes_test(is_admin, login_url='loja')
def adicionar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido adicionado com sucesso!")
            return redirect('painel_admin')
        else:
            messages.error(request, "Erro ao adicionar o pedido. Verifique os dados.")
    else:
        form = PedidoForm()
    
    return render(request, 'admin/adicionar_pedido.html', {'form': form, 'titulo': 'Adicionar Pedido'})

# EDITAR PRODUTOZZZZZZZZZ
@csrf_exempt
@login_required
@user_passes_test(is_admin, login_url='loja')
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES, instance=pedido)  
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido atualizado com sucesso!")
            return redirect('painel_admin')
        else:
            messages.error(request, "Erro ao atualizar o pedido. Verifique os dados.")
    else:
        form = PedidoForm(instance=pedido)  

    return render(request, 'admin/editar_pedido.html', {'form': form, 'pedido': pedido, 'titulo': 'Editar Pedido'})

# EXCLUIR PRODUTOZZZZZZZZ
@csrf_exempt
@login_required
@user_passes_test(is_admin, login_url='loja')
def excluir_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, "Pedido excluído com sucesso!")
        return redirect('painel_admin')
    
    return render(request, 'admin/excluir_pedido.html', {'pedido': pedido, 'titulo': 'Excluir Pedido'})
