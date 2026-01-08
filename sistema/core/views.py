from rest_framework import viewsets 
from .serializers import PacienteSerializer
from .models import Paciente    

class PacienteViewSet(viewsets.ModelViewSet):
    serializer_class = PacienteSerializer
    queryset = Paciente.objects.all()   
