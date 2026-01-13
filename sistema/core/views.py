from rest_framework import viewsets
from django.shortcuts import render
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


class PacienteExameViewSet(viewsets.ModelViewSet):
    queryset = Exame.objects.all()
    serializer_class = ExameSerializer

    def get_queryset(self):
        paciente_id = self.kwargs.get('paciente_id')
        if paciente_id is None:
            return Exame.objects.none()
        return Exame.objects.filter(paciente_id=paciente_id)

    def list(self, request, *args, **kwargs):
        """Return the paciente_exames template populated with serialized exames.

        This renders the same template the JS would consume but server-side,
        using the queryset returned by `get_queryset`.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # support pagination if configured
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            exames_data = serializer.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            exames_data = serializer.data

        context = {
            'paciente_id': kwargs.get('paciente_id'),
            'exames': exames_data,
        }
        return render(request, 'core/paciente_exames.html', context)
    
