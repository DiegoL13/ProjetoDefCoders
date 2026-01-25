from django.contrib import admin
from .models import Medico, Exame, Imagem, Paciente, LogExames

# Register your models here.
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
  list_display = ['nome','especialidade']
  exclude = ['password', 'last_login','groups', 'user_permissions']

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
  list_display = ['descricao','assinatura', 'data_criacao', 'resultado_medico', 'resultado_ia', 'disponibilidade']

@admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
  list_display = ['path']

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf']
    exclude = ['password', 'last_login', 'groups', 'user_permissions']


@admin.register(LogExames)
class LogExamesAdmin(admin.ModelAdmin):
    # Colunas visíveis na lista
    list_display = ('exame_id', 'nome_evento', 'data_evento', 'medico_id')
    
    # Impede alterações manuais nos logs para manter a integridade
    readonly_fields = ('exame', 'nome_evento', 'data_evento', 'medico_id')