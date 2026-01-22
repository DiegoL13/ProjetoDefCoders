from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.views import View
from .models import *
from .serializers import *
from django.contrib.auth import login
from .forms import PacienteCreationForm, MedicoCreationForm, LoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import random
from .choices import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import permissions

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
    
class MedicoExamesViewSet(viewsets.ModelViewSet):
    serializer_class = ExameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtra exames apenas do médico logado
        medico_id = self.kwargs.get('medico_id')
        return Exame.objects.filter(medico_id=medico_id).order_by('-data_criacao')

    def perform_update(self, serializer):
        # Garante que campos automáticos não sejam alterados manualmente no update
        serializer.save(medico=self.request.user.medico)

class CriarExameView(View):
    def get(self, request, medico_id):
        # Busca todos os pacientes para preencher o select
        pacientes = Paciente.objects.all() 
        return render(request, 'core/criar_exame.html', {
            'medico_id': medico_id,
            'pacientes': pacientes  # Adiciona a lista ao contexto
        })

    def post(self, request, medico_id):
        medico = get_object_or_404(Medico, id=medico_id)
        
        # Captura dados do formulário
        paciente_id = request.POST.get('paciente')
        descricao = request.POST.get('descricao')
        
        # Lógica automática para simular a IA e assinatura
        resultados_opcoes = ['BENIGNO', 'MALIGNO', 'SAUDÁVEL']
        
        if not paciente_id:
            # Retorna um erro caso o paciente não tenha sido selecionado
            return JsonResponse({'error': 'Paciente é obrigatório'}, status=400)
        
        try:
            exame = Exame.objects.create(
                medico=medico,
                paciente_id=paciente_id,
                descricao=descricao,
                resultado_ia=random.choice(resultados_opcoes),
                assinatura=medico.nome,
                resultado_medico='SAUDÁVEL', # Valor padrão inicial
                disponibilidade = False
            )

            # Salva as múltiplas imagens enviadas
            imagens_enviadas = request.FILES.getlist('imagens')
            for img in imagens_enviadas:
                Imagem.objects.create(exame=exame, path=img)

            return JsonResponse({'success': True}) # Retorna sucesso para o JavaScript
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
class EditarExameView(View):
    def post(self, request, exame_id):
        exame = get_object_or_404(Exame, id=exame_id)
        
        # 1. Verifica se o usuário tem perfil de médico
        if not hasattr(request.user, 'medico'):
            return JsonResponse({'success': False, 'error': 'Usuário não é um médico cadastrado.'}, status=403)
        
        # 2. Verifica se o médico logado é o responsável por este exame
        if exame.medico != request.user.medico:
            return JsonResponse({'success': False, 'error': 'Acesso negado: Você não é o médico deste exame.'}, status=403)

        # 3. Captura os dados enviados pelo JavaScript (FormData)
        resultado_medico = request.POST.get('resultado_medico')
        disponibilidade = request.POST.get('disponibilidade') == 'true'

        try:
            exame.resultado_medico = resultado_medico
            exame.disponibilidade = disponibilidade
            exame.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    

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


# ProjetoDefCoders/sistema/core/views.py

class PacienteExameViewSet(viewsets.ModelViewSet):
    queryset = Exame.objects.all()
    serializer_class = ExamePacienteSerializer

    def get_queryset(self):
        # 1. Recupera o ID do perfil de paciente vindo da URL
        paciente_id_url = self.kwargs.get('paciente_id')
        user = self.request.user
        
        # 2. Verifica se o utilizador tem um perfil de paciente
        if not hasattr(user, 'paciente'):
            return Exame.objects.none()

        # 3. Segurança: Garante que o ID da URL corresponde ao do utilizador logado
        if user.paciente.id != int(paciente_id_url):
            return Exame.objects.none()

        # 4. Filtra apenas exames do próprio paciente e já libertados pelo médico
        return Exame.objects.filter(
            paciente=user.paciente, 
            disponibilidade=True
        ).order_by('-data_criacao')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Se a requisição for do JavaScript (espera JSON), devolve os dados serializados
        if request.accepted_renderer.format == 'json':
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # Se for acesso direto pelo navegador, renderiza o template HTML
        serializer = self.get_serializer(queryset, many=True)
        context = {
            'paciente_id': self.kwargs.get('paciente_id'),
            'exames': serializer.data,
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
    
