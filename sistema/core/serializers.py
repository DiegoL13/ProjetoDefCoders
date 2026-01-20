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
    
    class Meta:
        model = Imagem
        fields = ['id', 'path', 'exame']


class ExameSerializer(serializers.ModelSerializer):
    # Leitura (Aninhados)
    medico = MedicoSerializer(read_only=True)
    paciente_detail = PacienteSerializer(source='paciente', read_only=True)
    imagens = ImagemSerializer(many=True, read_only=True)

    # Escrita (IDs)
    paciente = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all())
    
    # Upload de Imagens (Write Only - Apenas para receber os arquivos)
    imagens_upload = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Exame
        fields = [
            'id', 'medico', 'paciente', 'paciente_detail', 'data_criacao', 'resultado_ia', 
            'resultado_medico', 'assinatura', 'disponibilidade', 'imagens', 
            'imagens_upload'
        ]
        extra_kwargs = {
            'resultado_medico': {'required': False},
            'resultado_ia': {'required': False},
            'assinatura': {'required': False},
            'disponibilidade': {'required': False},
        }