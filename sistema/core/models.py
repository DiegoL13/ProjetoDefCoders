from django.db import models
from .choices import *

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    sexo = models.CharField(verbose_name='Sexo Biológico', max_length=20, choices=SEXO_BIOLOG_CHOICES)
    contato = models.CharField(verbose_name='Contato', max_length=45, help_text='Insira uma forma de contato (Telefone, email, etc)')
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=40)
    
    
    class Meta:
        abstract = True  # Define que esta classe não criará uma tabela própria no banco

    def __str__(self):
        return self.nome
    
class Paciente(Usuario):
    historico_medico = models.TextField(blank=True, null=True)

class Medico(Usuario):
  CRM = models.IntegerField(primary_key=True)
  especialidade = models.CharField(max_length=30)

  def __str__(self):
    return str(self.CRM)
  
class Exame(models.Model):
  medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
  assinatura = models.CharField(max_length=100)
  data = models.DateTimeField()
  tipo_escolha = (
    ('ANALISADO POR IA', 'Analisado por IA'),
    ('REVISADO POR HUMANO', 'Revisado por Humano')
    )
  tipo = models.CharField(choices=tipo_escolha)
  resultados = (
    ('BENIGNO','Benigno'),
    ('MALIGNO', 'Maligno'),
    ('SAUDÁVEL', 'Saudável')
  )
  resultado = models.CharField(choices=resultados)

class Imagem(models.Model):
  exame = models.ForeignKey(Exame, on_delete=models.CASCADE)
  path = models.ImageField()