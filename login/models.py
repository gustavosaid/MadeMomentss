from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, senha=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido.')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, senha=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nome, senha, **extra_fields)

class Create_User(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        default='cliente',
        choices=[('cliente', 'Cliente'), ('admin', 'Admin')]
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(default=timezone.now)

    # Autenticação 2FA
    mfa_secret = models.CharField(max_length=16, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)

    # Campos exigidos pelo Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.nome

# Classe de pedidos
class Pedido(models.Model):
    categoria = models.CharField(max_length=50, null=True, blank=True)
    foto = models.ImageField(upload_to='static/pedidos_fotos')
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao[:30]} - R${self.valor}"

class Carrinho(models.Model):
    usuario = models.ForeignKey(Create_User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)


class Endereco(models.Model):
    userEndereco = models.ForeignKey(Create_User, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=50, blank=False)
    bairro = models.CharField(max_length=50, blank=False)
    numero = models.CharField(max_length=5, blank=False)
    complemento = models.CharField(max_length=25)
    cep = models.CharField(max_length=9)

    def __str__(self):
        return f'{self.endereco}, {self.numero} - {self.bairro}'