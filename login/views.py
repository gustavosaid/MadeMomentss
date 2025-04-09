from hashlib import scrypt
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .models import Create_User
from django.contrib.auth.hashers import make_password #criptografar senha
from django.contrib import messages  # ✅ Esse é o import correto
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout



def login(request):
    return render(request,'login/login.html')

def conta(request):
    return render(request,'login/cadastro.html')

def loja(request):
    usuario = None
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Create_User.objects.get(id=usuario_id)
        except Create_User.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
    return render(request, 'loja/home.html', {"usuario": usuario})

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

def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        print("Tentativa de login:", email, senha)

        try:
            usuario = Create_User.objects.get(email=email)

            if usuario.check_password(senha):
                request.session['usuario_id'] = usuario.id
                messages.success(request, f"Bem-vindo, {usuario.nome}!")
                return redirect('loja')
            else:
                messages.error(request, "Senha incorreta.")
                return redirect('login')

        except Create_User.DoesNotExist:
            messages.error(request, "E-mail não cadastrado.")
            return redirect('login')

    return redirect('login')  # se GET

def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # isso limpa as mensagens pendentes
    return redirect('login')
    