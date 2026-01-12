from rest_framework import viewsets
from .models import Medico, Exame, Imagem, Usuario, Paciente
from .serializers import UsuarioSerializer, PacienteSerializer, MedicoSerializer, ExameSerializer, ImagemSerializer

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
    queryset = Exame.objects.all()
    serializer_class = ExameSerializer

class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer