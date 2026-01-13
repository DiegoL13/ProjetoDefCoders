from django.urls import path, include
from rest_framework import routers
from .views import MedicoViewSet, ExameViewSet, ImagemViewSet, PacienteExameViewSet, UsuarioViewSet, PacienteViewSet

router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'medicos', viewset=MedicoViewSet)
router.register(r'exames', viewset=ExameViewSet)
router.register(r'imagens', viewset=ImagemViewSet)
router.register(r'pacientes/(?P<paciente_id>\d+)/exames', viewset=PacienteExameViewSet, basename='paciente-exames')

urlpatterns = [
    path('', include(router.urls)),

]