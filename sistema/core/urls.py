from django.urls import path, include
from rest_framework import routers
from .views import MedicoViewSet, ExameViewSet, ImagemViewSet, UsuarioViewSet, PacienteViewSet


router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'medicos', MedicoViewSet, basename='medico')
router.register(r'exames', ExameViewSet, basename='exame')
router.register(r'imagens', ImagemViewSet, basename='imagem')

urlpatterns = [
    path('', include(router.urls)),
]