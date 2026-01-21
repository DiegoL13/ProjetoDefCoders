from django.urls import path, include
from rest_framework import routers
from .views import *
from . import views
from django.contrib.auth.views import LogoutView

router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'medicos', viewset=MedicoViewSet)
router.register(r'exames', viewset=ExameViewSet)
router.register(r'imagens', viewset=ImagemViewSet)
router.register(r'pacientes/(?P<paciente_id>\d+)/exames', viewset=PacienteExameViewSet, basename='paciente-exames')
router.register(r'medicos/(?P<medico_id>\d+)/exames', viewset=MedicoViewSet, basename='medico-exames')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('medicos/<int:medico_id>/dashboard/', MedicoDashboardView.as_view(), name='medico-dashboard'),
    path('medicos/<int:medico_id>/novo-exame/', CriarExameView.as_view(), name='criar-exame'),

    path('cadastro/paciente/', views.cadastro_paciente, name='cadastro_paciente'),
    path('cadastro/medico/', views.cadastro_medico, name='cadastro_medico'),
    
]