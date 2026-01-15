from rest_framework import viewsets
from .models import Medico, Exame, Imagem, Usuario, Paciente, Laudo
from .serializers import UsuarioSerializer, PacienteSerializer, MedicoSerializer, ExameSerializer, ImagemSerializer, LaudoSerializer
from django.shortcuts import render, get_object_or_404, redirect

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

# Interface para Análise de Exames
def analise_exame(request, exame_id):
    exame = get_object_or_404(Exame, id=exame_id)
    imagens = exame.imagens.all()

    contexto = {
        'exame': exame,
        'imagens': imagens
    }

    if request.method == 'POST':
        # Aqui você pode adicionar a lógica para processar a análise do exame
        # Por exemplo, salvar um laudo ou atualizar o status do exame
        return redirect('alguma_view_de_sucesso')  # Redirecionar após o processamento
    return render(request, 'core/analise_exame.html', contexto)

# Interface para Visualização de Laudos
def visualizar_laudo(request, exame_id):
    exame = get_object_or_404(Exame, id=exame_id)
    laudo = getattr(exame, 'laudo', None)

    contexto = {
        'exame': exame,
        'laudo': laudo
    }

    return render(request, 'core/visualizar_laudo.html', contexto)