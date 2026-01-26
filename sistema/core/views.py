from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework import viewsets
from django.views import View
from .models import *
from .serializers import *
from django.contrib.auth import authenticate, login
from .forms import PacienteCreationForm, MedicoCreationForm, LoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import random
from .choices import *
from rest_framework.response import Response
from rest_framework import permissions

class HomeView(View):
    def get(self, request):
        return render(request, 'core/home.html')
    
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
        # Filtra exames apenas do médico logado com verificação de segurança
        medico_id = self.kwargs.get('medico_id')
        
        # VERIFICAÇÃO EXPLÍCITA NO BANCO PARA GARANTIR PERMISSÕES
        from .models import Medico
        try:
            medico = Medico.objects.get(pk=medico_id)
            # Verificar se o usuário logado tem permissão para acessar este médico
            if hasattr(self.request.user, 'medico') and self.request.user.medico.id == medico.id:
                return Exame.objects.filter(medico_id=medico_id).order_by('-data_criacao')
            elif self.request.user.is_superuser:
                return Exame.objects.filter(medico_id=medico_id).order_by('-data_criacao')
        except Medico.DoesNotExist:
            pass
            
        return Exame.objects.none()

    def perform_update(self, serializer):
        # Garante que campos automáticos não sejam alterados manualmente no update
        serializer.save(medico=self.request.user.medico)

@method_decorator(login_required, name='dispatch')
class CriarExameView(View):
    def get(self, request, medico_id):
        # Verifica se o usuário está autenticado e é um médico
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Acesso negado: usuário não autenticado.")
        
        # VERIFICAÇÃO EXPLÍCITA NO BANCO PARA PERFIL MÉDICO
        from .models import Medico
        try:
            # Forçar atualização do usuário do banco
            request.user.refresh_from_db()
            
            # Verificar se usuário tem perfil de médico (consulta ao banco)
            if not Medico.objects.filter(usuario_ptr_id=request.user.id).exists():
                return HttpResponseForbidden("Acesso negado: usuário não é um médico.")
            
            medico = Medico.objects.get(usuario_ptr_id=request.user.id)
            
            # Verifica se o médico logado corresponde ao médico da URL
            if medico.id != int(medico_id):
                return HttpResponseForbidden("Acesso negado: médico não autorizado.")
                
        except Exception:
            return HttpResponseForbidden("Acesso negado: erro ao verificar perfil médico.")
        
        # Busca todos os pacientes para preencher o select
        pacientes = Paciente.objects.all() 
        return render(request, 'core/criar_exame.html', {
            'medico_id': medico_id,
            'pacientes': pacientes  # Adiciona a lista ao contexto
        })

    def post(self, request, medico_id):
        # Verifica se o usuário está autenticado e é um médico
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Acesso negado: usuário não autenticado.'}, status=403)
        
        # VERIFICAÇÃO EXPLÍCITA NO BANCO PARA PERFIL MÉDICO
        from .models import Medico
        try:
            # Forçar atualização do usuário do banco
            request.user.refresh_from_db()
            
            # Verificar se usuário tem perfil de médico (consulta ao banco)
            if not Medico.objects.filter(usuario_ptr_id=request.user.id).exists():
                return JsonResponse({'error': 'Acesso negado: usuário não é um médico.'}, status=403)
            
            medico = Medico.objects.get(usuario_ptr_id=request.user.id)
            
            # Verifica se o médico logado corresponde ao médico da URL
            if medico.id != int(medico_id):
                return JsonResponse({'error': 'Acesso negado: médico não autorizado.'}, status=403)
                
        except Exception as e:
            return JsonResponse({'error': f'Acesso negado: erro ao verificar perfil médico. {str(e)}'}, status=403)
        
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
            files_keys = list(request.FILES.keys())
            imagens_enviadas = request.FILES.getlist('imagens')
            imagens_recebidas = len(imagens_enviadas)
            imagens_salvas = 0
            for img in imagens_enviadas:
                Imagem.objects.create(exame=exame, path=img)
                imagens_salvas += 1

            return JsonResponse({
                'success': True,
                'files_keys': files_keys,
                'imagens_recebidas': imagens_recebidas,
                'imagens_salvas': imagens_salvas
            }) # Retorna sucesso para o JavaScript
        
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
        descricao = request.POST.get('descricao', '')

        try:
            # Atualizar campos básicos do exame
            exame.resultado_medico = resultado_medico
            exame.disponibilidade = disponibilidade
            exame.descricao = descricao
            exame.save()
            
            # 4. Processar remoção de imagens
            imagens_remover_ids = request.POST.getlist('imagens_remover')
            imagens_removidas = 0
            for img_id in imagens_remover_ids:
                try:
                    imagem = Imagem.objects.get(id=img_id, exame=exame)
                    # Remover arquivo do sistema de arquivos
                    if imagem.path and hasattr(imagem.path, 'delete'):
                        imagem.path.delete(save=False)
                    imagem.delete()
                    imagens_removidas += 1
                except Imagem.DoesNotExist:
                    continue
                except Exception as e:
                    print(f"Erro ao remover imagem {img_id}: {e}")
            
            # 5. Processar novas imagens
            novas_imagens = request.FILES.getlist('novas_imagens')
            imagens_adicionadas = 0
            for img_file in novas_imagens:
                try:
                    Imagem.objects.create(exame=exame, path=img_file)
                    imagens_adicionadas += 1
                except Exception as e:
                    print(f"Erro ao adicionar imagem: {e}")
            
            # Retornar sucesso com informações adicionais
            response_data = {
                'success': True,
                'message': 'Exame atualizado com sucesso!',
                'imagens_removidas': imagens_removidas,
                'imagens_adicionadas': imagens_adicionadas
            }
            
            return JsonResponse(response_data)
            
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
        
        # VERIFICAÇÃO EXPLÍCITA NO BANCO PARA GARANTIR PERMISSÕES
        from .models import Paciente
        try:
            paciente = Paciente.objects.get(pk=paciente_id_url)
            # Relacionar patient com user - FORÇAR CONSULTA
            user.refresh_from_db()
            
            # 2. Verificar no banco se usuário tem perfil de paciente
            if Paciente.objects.filter(usuario_ptr_id=user.id).exists():
                usuario_paciente = Paciente.objects.get(usuario_ptr_id=user.id)
                
                # 3. Segurança: Garante que o ID da URL corresponde ao do utilizador logado
                if usuario_paciente.id != int(paciente_id_url):
                    return Exame.objects.none()

                # 4. Filtra apenas exames do próprio paciente e já libertados pelo médico
                return Exame.objects.filter(
                    paciente=usuario_paciente, 
                    disponibilidade=True
                ).order_by('-data_criacao')
            
        except Paciente.DoesNotExist:
            pass
            
        return Exame.objects.none()

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
            from django.db import transaction
            try:
                with transaction.atomic():
                    # Garantir que o usuário seja salvo no banco antes do login
                    user = form.save(commit=True)
                    
                    # VERIFICAÇÃO EXPLÍCITA - Confirmar que foi salvo no banco
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user_db = User.objects.get(email=user.email)
                    
                    # Login após confirmação de salvamento
                    login(request, user_db)
                    
                    # Obtém o paciente criado com verificação explícita
                    paciente = Paciente.objects.get(usuario_ptr_id=user_db.id)
                    return redirect(f'/pacientes/{paciente.id}/exames/')
                    
            except Exception as e:
                # Adicionar erro no form em caso de falha
                form.add_error(None, f"Erro ao salvar usuário: {str(e)}")
                return render(request, 'core/cadastro_paciente.html', {'form': form})
    else:
        form = PacienteCreationForm()
    return render(request, 'core/cadastro_paciente.html', {'form': form})

def cadastro_medico(request):
    if request.method == 'POST':
        form = MedicoCreationForm(request.POST)
        if form.is_valid():
            from django.db import transaction
            try:
                with transaction.atomic():
                    # Garantir que o usuário seja salvo no banco antes do login
                    user = form.save(commit=True)
                    
                    # VERIFICAÇÃO EXPLÍCITA - Confirmar que foi salvo no banco
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user_db = User.objects.get(email=user.email)
                    
                    # Login após confirmação de salvamento
                    login(request, user_db)
                    
                    # Obtém o médico criado com verificação explícita
                    medico = Medico.objects.get(usuario_ptr_id=user_db.id)
                    return redirect(f'/medicos/{medico.id}/dashboard/')
                    
            except Exception as e:
                # Adicionar erro no form em caso de falha
                form.add_error(None, f"Erro ao salvar usuário: {str(e)}")
                return render(request, 'core/cadastro_medico.html', {'form': form})
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

        # FORÇAR CONSULTA AO BANCO PARA GARANTIR CONSISTÊNCIA
        from .models import Medico, Paciente
        user.refresh_from_db()

        # Verifica se o usuário NÃO tem perfil de médico E NÃO tem perfil de paciente
        is_medico = Medico.objects.filter(usuario_ptr_id=user.id).exists()
        is_paciente = Paciente.objects.filter(usuario_ptr_id=user.id).exists()

        if not is_medico and not is_paciente and not user.is_superuser:
            # Se não tiver perfil, adiciona uma mensagem de erro e cancela o login
            form.add_error(None, "Acesso permitido apenas para Médicos e Pacientes. Administradores devem usar a rota /admin.")
            return self.form_invalid(form)
            
        # Se tiver perfil, permite o login normal
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        
        # FORÇAR CONSULTA AO BANCO PARA GARANTIR CONSISTÊNCIA CACHE VS BANCO
        from django.db import transaction
        with transaction.atomic():
            user.refresh_from_db()
            
        # VERIFICAÇÃO EXPLÍCITA NO BANCO PARA REDIRECIONAMENTO CORRETO
        from .models import Medico, Paciente
        try:
            if Medico.objects.filter(usuario_ptr_id=user.id).exists():
                medico = Medico.objects.get(usuario_ptr_id=user.id)
                return reverse_lazy('medico-dashboard', kwargs={'medico_id': medico.id})
            elif Paciente.objects.filter(usuario_ptr_id=user.id).exists():
                paciente = Paciente.objects.get(usuario_ptr_id=user.id)
                return reverse_lazy('paciente-exames-list', kwargs={'paciente_id': paciente.id})
        except Exception:
            pass
            
        # Caso de segurança (inalcançável devido ao filtro acima)
        return '/'
    
