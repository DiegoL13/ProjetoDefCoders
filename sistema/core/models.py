import time
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .choices import *

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Criptografa a senha
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=20, choices=SEXO_BIOLOG_CHOICES)
    contato = models.CharField(max_length=45, blank=True, null=True)
    email = models.EmailField(unique=True)
    
    objects = UsuarioManager()

    # Configurações de Autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf'] 

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    def __str__(self):
        return self.nome
    
class Paciente(Usuario):
    historico_medico = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Nome: {self.nome}"

class Medico(Usuario):
  crm = models.CharField(max_length=20, unique=True)
  especialidade = models.CharField(max_length=30)

  def __str__(self):
    return f"Nome: {self.nome} - CRM: {self.crm}"
  

class Exame(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)
    descricao = models.TextField(max_length=2000)
    resultado_ia = models.CharField(choices=RESULTADOS, max_length=20)
    resultado_medico = models.CharField(choices=RESULTADOS, max_length=20)
    assinatura = models.CharField(max_length=100)
    disponibilidade = models.BooleanField(default=False)

    def __str__(self):
        return f"Exame de {self.paciente.nome} ({self.data_criacao})"
  

class Imagem(models.Model):
    exame = models.ForeignKey(Exame, on_delete=models.CASCADE, related_name='imagens')
    path = models.ImageField(upload_to='imagens_exames/')

    def __str__(self):
        return f"Imagem do Exame {self.exame.id}"
    

class LogExames(models.Model):
    exame = models.ForeignKey(Exame, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log do Exame {self.exame.id} em {self.timestamp}"