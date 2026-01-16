import hashlib
import json
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from .choices import *
from django.utils import timezone
from .middleware import get_current_request

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
    
    # IMPORTANTE: Adicione o Manager aqui
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

class Medico(Usuario):
  CRM = models.CharField(max_length=20, unique=True)
  especialidade = models.CharField(max_length=30)

  def __str__(self):
    return str(self.CRM)
  

class Exame(models.Model):
  medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
  paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE) # Campo adicionado
  assinatura = models.CharField(max_length=100)
  data = models.DateTimeField()
  
  tipo_escolha = (
      ('ANALISADO POR IA', 'Analisado por IA'),
      ('REVISADO POR HUMANO', 'Revisado por Humano')
  )
  tipo = models.CharField(choices=tipo_escolha, max_length=30)
  
  resultados = (
      ('BENIGNO','Benigno'),
      ('MALIGNO', 'Maligno'),
      ('SAUDÁVEL', 'Saudável')
  )
  resultado = models.CharField(choices=resultados, max_length=20)

  def __str__(self):
      return f"Exame de {self.paciente.nome} ({self.data})"

class Imagem(models.Model):
    exame = models.ForeignKey(Exame, on_delete=models.CASCADE, related_name='imagens')
    path = models.ImageField(upload_to='imagens_exames/') # Caminho de upload definido

    def __str__(self):
        return f"Imagem do Exame {self.exame.id}"

# Relacionamento One-to-One entre Exame e Laudo    
class Laudo(models.Model):
    exame = models.OneToOneField(Exame, on_delete=models.CASCADE, related_name='laudo')
    conteudo = models.TextField()
    medico = models.ForeignKey('Medico', on_delete=models.PROTECT, related_name='laudos_assinados')
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    imagem = models.OneToOneField('Imagem', on_delete=models.CASCADE)
    modelo_ia = models.ForeignKey('ModeloIA', on_delete=models.PROTECT)

# Resultados da IA
    resultado_ia = models.CharField(max_length=100)
    tipo_cancer = models.CharField(max_length=100, blank=True, null=True)
    score_confianca = models.FloatField()

# Validação Médica
    concorda_ia = models.BooleanField(default=False)
    parecer_medico = models.TextField(verbose_name="Objeções ou Observações")
    data_assinatura = models.DateTimeField(auto_now_add=True)

# Integridade e Segurança
    hash_assinatura = models.CharField(max_length=255, editable=False)

    def __str__(self):
        return f"Laudo do Exame {self.exame.id} - Paciente: {self.paciente.nome}"

# Gera um hash único baseado nos dados do laudo  
    def save(self, *args, **kwargs):
        if not self.hash_assinatura: 
            self.hash_assinatura = self.gerar_hash_integridade()

# Salva o objeto primeiro para garantir que tenha um ID
        is_new = self.pk is None
        super().save(*args, **kwargs)

# Registro automático em AuditLog
        acao_desc = "Criação de Laudo" if is_new else "Finalização/Assinatura de Laudo"

        AuditLog.objects.create(
            usuario=self.medico,
            acao=f"{acao_desc} ID: {self.id}",
            ip_origem="" # Pode ser preenchido com o IP real se disponível
        )
   
# Salvar automaticamente o hash e o Log de Auditoria
# Conteúdo obrigatório do log de auditoria
class AuditLog(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    acao = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_origem = models.GenericIPAddressField() 

    @staticmethod
    def registrar_acao(acao_desc):
        request = get_current_request()
        
        if request and request.user.is_authenticated:
            AuditLog.objects.create(
                usuario=request.user,
                acao=acao_desc,
                ip_origem=getattr(request, 'user_ip', '0.0.0.0')
            )

# Impede edição via admin
    def save(self, *args, **kwargs):
        if self.detalhes:
            raise PermissionError("Registro de log não pode ser modificado após criação.")
        super().save(*args, **kwargs)

def save(self, *args, **kwargs):
    is_new = self.pk is None
    if not self.hash_assinatura:
        self.hash_assinatura = self.gerar_hash_integridade()

    super().save(*args, **kwargs)

# Registro automático
    desc = f"Criou Laudo ID: {self.id}" if is_new else f"Validou o Laudo ID: {self.id}"
    AuditLog.registrar_acao(desc)


