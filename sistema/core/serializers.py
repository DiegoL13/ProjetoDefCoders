from rest_framework import serializers
from .models import Medico, Exame, Imagem, Usuario, Paciente, Laudo

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'data_nascimento', 'sexo', 'contato', 'email']

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
   paciente = PacienteSerializer(read_only=True)
   class Meta:
      model = Exame
      fields = ['medico','paciente','assinatura','data','tipo','resultado']
      

class ImagemSerializer(serializers.ModelSerializer):
   exame = ExameSerializer(read_only=True)
   class Meta:
      model = Imagem
      fields = ['path','exame']

class LaudoSerializer(serializers.ModelSerializer):
   exame = ExameSerializer(read_only=True)
   class Meta:
      model = Laudo
      fields = ['exame','conteudo','data_criacao']  

class LaudoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laudo
        fields = ['exame', 'conteudo']      
        read_only_fields = ['data_criacao']
    def create(self, validated_data):
        laudo = Laudo.objects.create(**validated_data)
        return laudo   
