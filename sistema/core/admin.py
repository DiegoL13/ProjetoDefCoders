from django.contrib import admin
from .models import Paciente, Medico, Exame, Laudo, Imagem

admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'sexo', 'telefone')
    
admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):        
    list_display = ('nome', 'crm', 'especialidade', 'cpf', 'sexo', 'telefone')

admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'data_criacao', 'data_atualizacao')
    list_filter = ('id_exame', 'imagem')
admin.register(Laudo)
class LaudoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'assinatura_medico') 
  

admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
    list_display = ('url')
    list_filter = ('exame')