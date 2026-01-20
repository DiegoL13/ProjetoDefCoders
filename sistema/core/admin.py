from django.contrib import admin
from django.utils.html import format_html # Importante para mostrar a miniatura da foto
from .models import Paciente, Medico, Exame, Imagem

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    # Mostra o nome do usuário e CRM
    list_display = ('usuario', 'crm', 'especialidade')
    search_fields = ('usuario__username', 'crm') # buscar pelo nome ou CRM

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'id', 'historico_medico')
    search_fields = ('usuario__username',)

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ('medico', 'paciente', 'data_criacao', 'status', 'liberado_para_paciente')
    
    # Adicione filtros laterais para facilitar a gestão
    list_filter = ('status', 'liberado_para_paciente', 'data_criacao')
    
    # Permite buscar exames pelo nome do médico ou do paciente
    search_fields = ('medico__usuario__username', 'paciente__usuario__username')

@admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'exame', 'miniatura_imagem')
    
    def miniatura_imagem(self, obj):
        if obj.path:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.path.url)
        return "Sem Imagem"
    
    miniatura_imagem.short_description = "Pré-visualização"

