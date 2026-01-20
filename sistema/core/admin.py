from django.contrib import admin
from .models import Medico, Exame, Imagem, Paciente

# Register your models here.
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
  list_display = ['nome','especialidade']
  exclude = ['password', 'last_login','groups', 'user_permissions']

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
  list_display = ['assinatura','data','tipo','resultado']

@admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
  list_display = ['path']

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf']
    exclude = ['password', 'last_login', 'groups', 'user_permissions']
