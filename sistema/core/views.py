from rest_framework import viewsets
from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from django.contrib.auth import login
from .forms import PacienteCreationForm, MedicoCreationForm, LoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

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

# sistema/core/views.py

class MedicoExameViewSet(viewsets.ModelViewSet):
    # Usa o mesmo serializer, pois os dados do exame são os mesmos
    serializer_class = ExameSerializer

    def get_queryset(self):
        # Pega o ID do médico vindo da URL
        medico_id = self.kwargs.get('medico_id')
        if medico_id is None:
            return Exame.objects.none()
        # Filtra os exames onde o campo 'medico' é igual ao ID capturado
        return Exame.objects.filter(medico_id=medico_id)

    def list(self, request, *args, **kwargs):
        # Lógica para filtrar e serializar os dados
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            exames_data = serializer.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            exames_data = serializer.data

        context = {
            'medico_id': kwargs.get('medico_id'),
            'exames': exames_data,
        }
        # Renderiza um template específico para o médico (vamos criar no passo 3)
        return render(request, 'core/medico_exames.html', context)

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
    

def cadastro_paciente(request):
    if request.method == 'POST':
        form = PacienteCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Faz o login automático após cadastro
            return redirect('paciente-exames-list', paciente_id=user.id) # Redireciona para a home ou dashboard
    else:
        form = PacienteCreationForm()
    return render(request, 'core/cadastro_paciente.html', {'form': form})

def cadastro_medico(request):
    if request.method == 'POST':
        form = MedicoCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('medico-exames-list', medico_id=user.id) 
    else:
        form = MedicoCreationForm()
    return render(request, 'core/cadastro_medico.html', {'form': form})

class CustomLoginView(LoginView):
    # Usa o seu formulário de login personalizado
    authentication_form = LoginForm 
    template_name = 'core/login.html'

    def get_success_url(self):
        user = self.request.user
        
        if hasattr(user, 'medico'):
            return reverse_lazy('medico-exames-list', kwargs={'medico_id': user.medico.id})
            
        # Verifica se o usuário tem um perfil de Paciente
        elif hasattr(user, 'paciente'):
            return reverse_lazy('paciente-exames-list', kwargs={'paciente_id': user.paciente.id})
            
        # Se for superusuário (admin) ou outro tipo, manda para a raiz ou admin
        return reverse_lazy('admin:index') # Ou '/' se preferir