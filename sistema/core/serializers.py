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
    # Usamos FileField ou ImageField para que o DRF gere a URL completa da imagem
    path = serializers.ImageField(required=True)

    class Meta:
        model = Imagem
        fields = ['id', 'path', 'exame']


# ProjetoDefCoders/sistema/core/serializers.py

class ExameSerializer(serializers.ModelSerializer):
    imagens = ImagemSerializer(many=True, read_only=True)
    medico_nome = serializers.ReadOnlyField(source='medico.nome')
    paciente_nome = serializers.ReadOnlyField(source='paciente.nome') # Adicionado

    class Meta:
        model = Exame
        fields = [
            'id', 
            'medico',         # Adicionado pois é obrigatório no modelo
            'medico_nome', 
            'paciente', 
            'paciente_nome', 
            'descricao', 
            'data_criacao', 
            'resultado_ia', 
            'resultado_medico', 
            'assinatura',     # Adicionado pois é obrigatório no modelo
            'disponibilidade',
            'imagens', 
        ]