from django.db import models
from django.utils import timezone
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UsuarioManager(BaseUserManager):

    def create_user(self, email, nome, senha=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido.')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(senha)  # Agora vai funcionar!
        user.save(using=self._db)
        return user

class Create_User(AbstractBaseUser, PermissionsMixin):  
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=20, default='cliente', choices=[('cliente', 'Cliente'), ('admin', 'Admin')])
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.nome


#classe de pedidos.
class Pedido(models.Model):
    categoria = models.CharField(max_length=50,null=True, blank=True)
    foto = models.ImageField(upload_to='static/pedidos_fotos')
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.descricao[:30]} - R%{self.valor}"
    



