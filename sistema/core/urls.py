from django.urls import path, include
from rest_framework import routers
from .views import MedicoViewSet, ExameViewSet, ImagemViewSet, UsuarioViewSet, PacienteViewSet, LaudoViewSet
from . import views   

router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'medicos', viewset=MedicoViewSet)
router.register(r'exames', viewset=ExameViewSet)
router.register(r'imagens', viewset=ImagemViewSet)
router.register(r'laudos', viewset=LaudoViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('laudo/<int:laudo_id>/analizar/', views.analisar_laudo, name='analizar_laudo_pdf'),

    path('laudo/<int:laudo_id>/pdf/', views.exportar_laudo_pdf, name='exportar_laudo_pdf'),

    path('laudo/<int:laudo_id>/resultado/', views.consulta_resultado, name='consulta_resultado'),
]