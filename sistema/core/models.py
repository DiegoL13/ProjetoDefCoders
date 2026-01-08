from django.db import models

# Create your models here.
class Medico(models.Model):
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
  path = models.URLField()