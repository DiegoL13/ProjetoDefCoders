from django.contrib import admin
from .models import Medico, Exame, Imagem

# Register your models here.
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
  list_display = ['especialidade']

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
  list_display = ['assinatura','data','tipo','resultado']

@admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
  list_display = ['path']