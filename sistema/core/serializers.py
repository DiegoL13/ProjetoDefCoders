from rest_framework import serializers
from .models import Medico, Exame, Imagem, Usuario, Paciente

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'data_nasc', 'sexo', 'contato', 'email', 'senha']

class MedicoSerializer(UsuarioSerializer):
    class Meta(UsuarioSerializer.Meta):
        model = Medico
        fields = UsuarioSerializer.Meta.fields + ['CRM', 'especialidade']

class PacienteSerializer(UsuarioSerializer):
    class Meta(UsuarioSerializer.Meta):
        model = Paciente
        fields = UsuarioSerializer.Meta.fields + ['historico_medico']

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