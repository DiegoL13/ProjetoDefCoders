from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser #para não dar erro no json ao fazer upload de imagens
from .models import Medico, Exame, Imagem, Usuario, Paciente, Imagem
from .serializers import UsuarioSerializer, PacienteSerializer, MedicoSerializer, ExameSerializer,ExameDetailSerializer, ImagemSerializer

# Create your views here.
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    

class ExameViewSet(viewsets.ModelViewSet):
    serializer_class = ExameSerializer

    def get_queryset(self):
        user = self.request.user
        
        # Se não estiver logado, não vê nada
        if not user.is_authenticated:
            return Exame.objects.none()

        #Médico vê todos os exames que ele criou
        if hasattr(user, 'medico'):
            return Exame.objects.filter(medico=user.medico)

        #Paciente
        elif hasattr(user, 'paciente'):
            return Exame.objects.filter(
                paciente=user.paciente,
                liberado_para_paciente=True # Só vê se estiver liberado
            )

        return Exame.objects.none()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ExameDetailSerializer
        return ExameSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if hasattr(request.user, 'medico'):
            serializer.save(medico=request.user.medico)
        else:
            serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        '''2. Extraímos os dados limpos
        dados = serializer.validated_data
        imagens_ids = dados.pop('imagens_ids', []) 
        paciente = dados.get('paciente')
        
        #Usamos uma transação para garantir a integridade dos dados
'''
'''
        with transaction.atomic():
            
            if imagens_ids:

                imagens_erradas = Imagem.objects.filter(
                    id__in=imagens_ids
                ).exclude(paciente=paciente).exists()

                if imagens_erradas:
                    # Retorna erro 400 
                    return Response(
                        {"error": "Você tentou adicionar imagens que pertencem a outro paciente!"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            if hasattr(request.user, 'medico'):
                 serializer.save(medico=request.user.medico)
            else:
                 serializer.save()
            
            exame_criado = serializer.instance

            if imagens_ids:
                Imagem.objects.filter(id__in=imagens_ids).update(exame=exame_criado)
            
        #retorna os dados criados
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
'''

class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer
    parser_classes = (MultiPartParser, FormParser)