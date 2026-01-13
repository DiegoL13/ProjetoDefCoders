from rest_framework import serializers
from .models import Paciente, Medico, Exame, Imagem, Laudo

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['nome', 'email', 'cpf', 'sexo', 'exames_realizados'] 

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['nome', 'crm', 'especialidade', 'cpf', 'sexo']

class ExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exame
        fields = ['tipo', 'data_criacao', 'data_atualizacao', 'medico', 'paciente', 'laudo']

class LaudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laudo
        fields = [ 'descricao', 'assinatura_medico']

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = [ 'url', 'exame']
      
