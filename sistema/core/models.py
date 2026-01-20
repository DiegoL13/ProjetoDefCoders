from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .choices import *
from django.conf import settings

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
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=20, choices=SEXO_BIOLOG_CHOICES)
    contato = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    
    objects = UsuarioManager()

    # Configurações de Autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf'] 

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
class Paciente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='paciente')
    historico_medico = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Paciente: {self.usuario.nome}"

class Medico(models.Model):
        usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='medico')
        crm = models.CharField(max_length=20, unique=True)
        especialidade = models.CharField(max_length=100, blank=True)

        def __str__(self):
            return f"Dr. {self.usuario.nome} - CRM: {self.crm}"

class Exame(models.Model):
  medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
  status = models.CharField(max_length=20,choices=STATUS_EXAME,default="PENDENTE")
  data_criacao = models.DateTimeField(auto_now_add=True)
  paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT) # Campo adicionado
  assinatura = models.CharField(max_length=100)
  descricao = models.TextField(blank=True) 
  liberado_para_paciente = models.BooleanField(default=False)
#resultado = models.CharField(choices=resultados, max_length=20)
def __str__(self):
      return f"Exame de {self.paciente.usuario.nome} ({self.data_criacao.strftime('%Y-%m-%d')})"

def caminho_upload_exame(instance, filename):
    # Note o uso de .exame_id em vez de .exame.id
    return f'imagens_exames/exame_{instance.exame_id}/{filename}'

class Imagem(models.Model):
    exame = models.ForeignKey(Exame, on_delete=models.CASCADE, related_name='imagens')
    path = models.ImageField(upload_to=caminho_upload_exame) 
    data_upload = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Imagem pertencente ao Exame:  {self.exame.id}"
