from rest_framework import viewsets 
from .serializers import PacienteSerializer, MedicoSerializer, ExameSerializer, LaudoSerializer, ImagemSerializer
from .models import Paciente, Medico, Exame, Laudo, Imagem 


class PacienteViewSet(viewsets.ModelViewSet):
    serializer_class = PacienteSerializer
    queryset = Paciente.objects.all() 

class MedicoViewSet(viewsets.ModelViewSet):
    serializer_class = MedicoSerializer
    queryset = Medico.objects.all()

class ExameViewSet(viewsets.ModelViewSet):
    serializer_class = ExameSerializer
    queryset = Exame.objects.all()

class LaudoViewSet(viewsets.ModelViewSet):
    serializer_class = LaudoSerializer
    queryset = Laudo.objects.all()

class ImagemViewSet(viewsets.ModelViewSet):
    serializer_class = ImagemSerializer
    queryset = Imagem.objects.all()
