from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    endereco = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    genero = models.CharField(max_length=10)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome
