from rest_framework import serializers
from .models import Medico, Exame, Imagem, Usuario, Paciente

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'data_nascimento', 'sexo', 'contato', 'email']

class MedicoSerializer(UsuarioSerializer):
    class Meta(UsuarioSerializer.Meta):
        model = Medico
        fields = UsuarioSerializer.Meta.fields + ['crm', 'especialidade']

class PacienteSerializer(UsuarioSerializer):
    class Meta(UsuarioSerializer.Meta):
        model = Paciente
        fields = UsuarioSerializer.Meta.fields + ['historico_medico']


class ImagemSerializer(serializers.ModelSerializer):
    path = serializers.ImageField(required=True)

    class Meta:
        model = Imagem
        fields = ['id', 'path', 'exame']


class ExameSerializer(serializers.ModelSerializer):
    imagens = ImagemSerializer(many=True, read_only=True)
    medico_nome = serializers.ReadOnlyField(source='medico.nome')
    paciente_nome = serializers.ReadOnlyField(source='paciente.nome') # Adicionado

    class Meta:
        model = Exame
        fields = [
            'id', 'medico', 'medico_nome', 'paciente', 'paciente_nome', 'descricao', 'data_criacao', 
            'resultado_ia', 'resultado_medico', 'assinatura','disponibilidade','imagens', 
        ]

class ExamePacienteSerializer(serializers.ModelSerializer):
    medico_nome = serializers.ReadOnlyField(source='medico.nome')
    imagens = ImagemSerializer(many=True, read_only=True)

    class Meta:
        model = Exame
        fields = [
            'id', 'medico_nome', 'descricao', 'data_criacao', 'resultado_medico', 'disponibilidade','imagens', 
        ]