from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.views import View
from .models import Usuario, Paciente, Medico, Exame, Imagem
from .serializers import *
from django.contrib.auth import login
from .forms import PacienteCreationForm, MedicoCreationForm, LoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import random
from .choices import *

# Suas views abaixo...
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

    
class MedicoDashboardView(View):
    def get(self, request, medico_id):
        # Garante que o médico existe
        medico = get_object_or_404(Medico, id=medico_id)
        
        # Busca os exames vinculados a este médico
        exames = Exame.objects.filter(medico_id=medico_id).prefetch_related('imagens').order_by('-data_criacao')
        
        context = {
            'medico_id': medico_id,
            'exames': exames,
            'medico': medico
        }
        return render(request, 'core/medico_dashboard.html', context)

class CriarExameView(View):
    def get(self, request, medico_id):
        # Apenas renderiza o formulário
        return render(request, 'core/criar_exame.html', {'medico_id': medico_id})

    def post(self, request, medico_id):
        medico = get_object_or_404(Medico, id=medico_id)
        
        # Captura dados do formulário
        paciente_id = request.POST.get('paciente')
        descricao = request.POST.get('descricao')
        
        # Lógica automática para simular a IA e assinatura
        resultados_opcoes = ['BENIGNO', 'MALIGNO', 'SAUDÁVEL']
        
        exame = Exame.objects.create(
            medico=medico,
            paciente_id=paciente_id,
            descricao=descricao,
            resultado_ia=random.choice(resultados_opcoes),
            assinatura=medico.nome,
            resultado_medico='SAUDÁVEL' # Valor padrão inicial
        )

        # Salva as múltiplas imagens enviadas
        imagens_enviadas = request.FILES.getlist('imagens')
        for img in imagens_enviadas:
            Imagem.objects.create(exame=exame, path=img)

        return redirect('medico-dashboard', medico_id=medico_id)

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
        # 1. Recupera o ID do paciente da URL
        paciente_id = self.kwargs.get('paciente_id')
        
        # 2. Verifica se o usuário logado é o próprio paciente (Segurança)
        # Isso impede que o Paciente A acesse a URL do Paciente B
        user = self.request.user
        if not hasattr(user, 'paciente') or user.paciente.id != int(paciente_id):
            return Exame.objects.none()

        # 3. Filtra apenas exames do próprio paciente E que estejam disponíveis
        return Exame.objects.filter(
            paciente_id=paciente_id, 
            disponibilidade=True
        )

    def list(self, request, *args, **kwargs):
        # O restante do código permanece igual, 
        # ele usará o queryset filtrado acima automaticamente
        queryset = self.filter_queryset(self.get_queryset())

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
            return reverse_lazy('medico-dashboard', kwargs={'medico_id': user.medico.id})
            
        # Redirecionamento para Pacientes
        if hasattr(user, 'paciente'):
            return reverse_lazy('paciente-exames-list', kwargs={'paciente_id': user.paciente.id})
            
        # Caso de segurança (teoricamente inalcançável devido ao filtro acima)
        return '/'
    



