from django.urls import path, include
from rest_framework import routers
from django.contrib.auth.views import LoginView
from .views import *
from . import views
from django.contrib.auth.views import LogoutView


router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'medicos', MedicoViewSet, basename='medico')
router.register(r'exames', ExameViewSet, basename='exame')
router.register(r'imagens', ImagemViewSet, basename='imagem')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cadastro/paciente/', views.cadastro_paciente, name='cadastro_paciente'),
    path('cadastro/medico/', views.cadastro_medico, name='cadastro_medico'),
    
]