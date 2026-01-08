from rest_framework import serializers
from .models import Medico, Exame, Imagem

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
      model = Medico
      fields = ['CRM', 'especialidade']

class ExameSerializer(serializers.ModelSerializer):
   medico = MedicoSerializer(read_only=True)
   class Meta:
      model = Exame
      fields = ['assinatura','data','tipo','resultado']
      

class ImagemSerializer(serializers.ModelSerializer):
   exame = ExameSerializer(read_only=True)
   class Meta:
      model = Imagem
      fields = ['path']