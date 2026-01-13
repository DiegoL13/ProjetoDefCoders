from django.db import models
from .options import SEX_OPTIONS

class Usuario(models.Model):
    nome = models.CharField(max_length=100, help_text="Digite seu nome completo.")
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True, help_text="Digite apenas o CPF sem pontos ou traços.")
    sexo = models.CharField(max_length=20,choices=SEX_OPTIONS)
    class Meta:
        abstract = True

    def __str__(self):
        return f'nome = {self.nome}, cpf = {self.cpf}'

class Paciente(Usuario):
    exames_realizados = models.ManyToManyField('Medico',through='Exame')
    def __str__(self):
        return f'nome = {self.nome}, cpf = {self.cpf}'

class Medico(Usuario):
    crm = models.CharField(null=False,max_length=6, unique=True, primary_key=True)
    especialidade = models.CharField(max_length=50)
    exames_realizados = models.ManyToManyField('Paciente',through='Exame')
    def __str__(self):
        return f' nome = {self.nome}, crm = {self.crm}'

class Laudo(models.Model):
    descricao = models.TextField(max_length=500, null=True)
    assinatura_medico = models.CharField(max_length=100, null=False, help_text='Assinatura do Médico')
    def __str__(self):
        return f'ID: {self.id}, Médico: {self.assinatura_medico}'

class Exame(models.Model):
    tipo = models.CharField(max_length=100, null=False)
    data_criacao = models.DateTimeField(help_text="Data e hora de criação do exame", auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    laudo = models.ForeignKey( 'Laudo', on_delete=models.SET_NULL, null=True, related_name='exames')

    def __str__(self):
        return 'criado'
    

class Imagem(models.Model):
    url = models.URLField(null=False, max_length=30)
    exame = models.ForeignKey('Exame', on_delete=models.CASCADE, related_name='imagens', null=True)
    def __str__(self):
        return f'ID: {self.id}, URL: {self.url}'
