from rest_framework import serializers
from .models import Paciente

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['nome', 'idade', 'endereco', 'cpf', 'genero', 'telefone'] 
