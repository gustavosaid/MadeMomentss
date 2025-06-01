from hashlib import scrypt
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .models import Create_User, Pedido
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


def login_view(request):
    return render(request,'login/login.html')

def conta(request):
    return render(request,'login/cadastro.html')

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

@csrf_exempt
def cadastrar_usuario(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        telefone = request.POST.get("telefone")

        # Verifica se o e-mail já está cadastrado
        if Create_User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return redirect('conta')  # Página de cadastro

        # Cria o usuário usando o manager personalizado
        novo_usuario = Create_User.objects.create_user(
            email=email,
            nome=nome,
            senha=senha,
            telefone=telefone
        )
        

        #messages.success(request, f"Usuário {novo_usuario.nome} cadastrado com sucesso!")
        return render(request, 'loja/home.html', {"usuario": novo_usuario})
    request.session['usuario_id'] = novo_usuario.id

    return redirect('conta')

@csrf_exempt
def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            usuario = Create_User.objects.get(email=email)

            if usuario.check_password(senha):
                if usuario.mfa_enabled:#Se o usuário tem 2FA ativado (mfa_enabled = True):

                    #Gera o QR code chamando a funcao e salva na variavel
                    img_str = gerar_qrcode_para(usuario)

                    # salva id temporário e passa img para o template
                    request.session['temp_user_id'] = usuario.id
                    context = {
                        'user_id': usuario.id,
                        'qr_code': img_str,
                        'usuario': usuario,
                    }
                    return render(request, 'login/otp_verify.html', context)

                # Login direto sem 2FA
                request.session['usuario_id'] = usuario.id
                auth_login(request, user)
                messages.success(request, f"Bem-vindo, {usuario.nome}!")
                return redirect('loja')

            else:
                messages.error(request, "Senha incorreta.")
                return redirect('login')

        except Create_User.DoesNotExist:
            messages.error(request, "E-mail não cadastrado.")
            return redirect('login')

    return redirect('login')

@csrf_exempt
def verify_mfa(request):
    if request.method == 'POST':
        #Pegando os dados passados por parametro
        otp = request.POST.get('otp_code')
        user_id = request.POST.get('user_id')

        #Busca o usuário no banco
        try:
            user = Create_User.objects.get(id=user_id)
        except Create_User.DoesNotExist:
            messages.error(request, 'Usuário inválido.')
            return redirect('login')

        totp = pyotp.TOTP(user.mfa_secret)

        #Cria uma instância TOTP usando o segredo do usuário para verificar o código
        if totp.verify(otp):
            #Verifica se o codigo digita ta certo dentro o intervalo se der certo vai para a loja
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

#Define uma função auxiliar para gerar o QR Code
def gerar_qrcode_para(usuario):

    #Cria a instância TOTP com o segredo do usuário.
    totp = pyotp.TOTP(usuario.mfa_secret)

    #Gera a URI padrão
    uri = totp.provisioning_uri(name=usuario.email, issuer_name="MadeMoments")

    #Gera a imagem QR code com a URI
    qr = qrcode.make(uri)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")

    
    #Codifica a imagem em base64 para ser embutida no HTML.
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str



def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # isso limpa as mensagens pendentes
    return redirect('login')
    
#formulario para o administrator adicionar novos pedidos
@csrf_exempt
def criar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido cadastrado com sucesso!')
            #return redirect('/loja')
    else:
        form = PedidoForm()
    return render(request, 'loja/add_pedido.html', {'form': form})


#leva pra pagina de detalhes do produto ao clicar em comprar
@csrf_exempt
def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'loja/detalhe_pedido.html', {'pedido': pedido})






#leva pra pagina de adiconar ao carrinho e escolher a quantidade que vai ser comprada
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
    return render(request,'loja/mercado_pagoCerta.html')

def pagamento_errado(request):
    return render(request,'loja/mercado_pagoErrada.html')



# def carrinho_context(request):
#     if request.user.is_authenticated:
#         carrinho = Carrinho.objects.filter(usuario=request.user)
#     else:
#         carrinho = []
#         return {'itens_carrinho': carrinho}



# def listar_pedidos(request):
#     pedidos = Pedido.objects.all()
#     return render(request, 'loja/listar_pedido.html', {'pedidos': pedidos})
    
# def home(request):
#     pedidos = Pedido.objects.all()
#     return render(request, 'loja/home.html', {'pedidos': pedidos})