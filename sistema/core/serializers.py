from rest_framework import serializers
from .models import Medico, Exame, Imagem, Usuario, Paciente

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nome','cpf','data_nascimento','sexo','contato','email']

class MedicoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    class Meta:
        model = Medico
        fields = ['id', 'usuario', 'crm', 'especialidade']

class PacienteSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    class Meta:
        model = Paciente
        fields = ['id', 'usuario', 'historico_medico']

    
class ImagemSerializer(serializers.ModelSerializer):
   exame = serializers.PrimaryKeyRelatedField(queryset=Exame.objects.all())
   class Meta:
      model = Imagem
      fields = ['id','path','exame','data_upload','paciente' ]

def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['exame'] = ExameSerializer(instance.exame).data
        return representation


class ExameSerializer(serializers.ModelSerializer):
    medico =  serializers.PrimaryKeyRelatedField(queryset=Medico.objects.all())
    paciente =  serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all())
    imagens_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    imagens = ImagemSerializer(many=True, read_only=True)
    class Meta:
      model = Exame
      fields = ['id','medico','paciente','assinatura','status','data_criacao','descricao', 'liberado_para_paciente', 'imagens', 'imagens_ids' ]

class ExameDetailSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(read_only=True)
    paciente = PacienteSerializer(read_only=True)

    class Meta:
        model = Exame
        fields = '__all__'

   
def get_queryset(self):
        user = self.request.user
        
        # Se for Médico: Vê todos os exames que ELE criou
        if hasattr(user, 'medico'):
            return Exame.objects.filter(medico=user.medico)
            
        # Se for Paciente: Vê APENAS os seus exames QUE JÁ FORAM LIBERADOS
        elif hasattr(user, 'paciente'):
            return Exame.objects.filter(paciente=user.paciente,liberado_para_paciente=True)
            
        return Exame.objects.none()

class ImagemSerializer(serializers.ModelSerializer):
   exame = serializers.PrimaryKeyRelatedField(queryset=Exame.objects.all())
   class Meta:
      model = Imagem
      fields = ['id','path','exame','data_upload' ]

'''
def create(self, validated_data):
        
        usuario_data = validated_data.pop('usuario')

        usuario_instance = Usuario.objects.create(**usuario_data)


        # 3. Criamos o Médico no banco (Tabela Filho), ligando ao usuário criado acima
        medico_instance = Medico.objects.create(usuario=usuario_instance, **validated_data)

        # 4. Retornamos a instância completa do médico
        return medico_instance
'''
