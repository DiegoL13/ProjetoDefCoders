from django.contrib import admin
from .models import Medico, Exame, Imagem, Laudo, Usuario, Paciente

# Register your models here.
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
  list_display = ['especialidade']

@admin.register(Laudo)
class LaudoAdmin(admin.ModelAdmin):
  list_display = ['exame', 'conteudo', 'data_assinatura']

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
  list_display = ['assinatura','data','tipo','resultado']

@admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
  list_display = ['path']

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
  list_display = ['nome','cpf','data_nascimento','sexo','contato','email']  

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
  list_display = ['historico_medico']
