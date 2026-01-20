from rest_framework import viewsets
from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from django.contrib.auth import login
from .forms import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import random

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

    def perform_create(self, serializer):
        # 1. Validação de Médico
        if not hasattr(self.request.user, 'medico'):
            raise serializers.ValidationError("Apenas médicos podem criar exames.")
        
        medico_logado = self.request.user.medico

        # 2. Lógica Automática (IA e Assinatura)
        opcoes = [opcao[0] for opcao in RESULTADOS]
        resultado_ia_aleatorio = random.choice(opcoes)
        assinatura_automatica = medico_logado.nome

        # Define um valor padrão temporário para o resultado médico se não for enviado
        # (Assumindo que no banco temos um default, ou usamos um dos choices válidos)
        res_medico = serializer.validated_data.get('resultado_medico', 'SAUDÁVEL')

        # 3. Salva o Exame
        exame = serializer.save(
            medico=medico_logado,
            resultado_ia=resultado_ia_aleatorio,
            assinatura=assinatura_automatica,
            resultado_medico=res_medico,
            disponibilidade=False # Começa indisponível
        )

        # 4. Processamento das Imagens
        imagens = self.request.FILES.getlist('imagens_upload')
        for image_file in imagens:
            Imagem.objects.create(exame=exame, path=image_file)

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
    



