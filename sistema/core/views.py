from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser #para não dar erro no json ao fazer upload de imagens
from .models import Medico, Exame, Imagem, Usuario, Paciente, Imagem
from .serializers import UsuarioSerializer, PacienteSerializer, MedicoSerializer, ExameSerializer,ExameDetailSerializer, ImagemSerializer
from django.shortcuts import render, redirect
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

class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer
    parser_classes = (MultiPartParser, FormParser)


class PacienteExameViewSet(viewsets.ModelViewSet):
    queryset = Exame.objects.all()
    serializer_class = ExameSerializer

    def get_queryset(self):
        paciente_id = self.kwargs.get('paciente_id')
        if paciente_id is None:
            return Exame.objects.none()
        return Exame.objects.filter(paciente_id=paciente_id)

    def list(self, request, *args, **kwargs):

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

# sistema/core/views.py

class CustomLoginView(LoginView):
    authentication_form = LoginForm 
    template_name = 'core/login.html'

    def form_valid(self, form):
        # Pega o usuário que está tentando logar
        user = form.get_user()

        # Verifica se o usuário NÃO tem perfil de médico E NÃO tem perfil de paciente
        if not hasattr(user, 'medico') and not hasattr(user, 'paciente'):
            # Se não tiver perfil, adiciona uma mensagem de erro e cancela o login
            form.add_error(None, "Acesso permitido apenas para Médicos e Pacientes. Administradores devem usar a rota /admin.")
            return self.form_invalid(form)
            
        # Se tiver perfil, permite o login normal
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        
        # Redirecionamento para Médicos
        if hasattr(user, 'medico'):
            return reverse_lazy('medico-exames-list', kwargs={'medico_id': user.medico.id})
            
        # Redirecionamento para Pacientes
        if hasattr(user, 'paciente'):
            return reverse_lazy('paciente-exames-list', kwargs={'paciente_id': user.paciente.id})
            
        # Caso de segurança (teoricamente inalcançável devido ao filtro acima)
        return '/'
