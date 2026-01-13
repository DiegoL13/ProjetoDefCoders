from django.urls import path, include
from rest_framework import routers
from .views import PacienteViewSet, MedicoViewSet, ExameViewSet, LaudoViewSet, ImagemViewSet 


router = routers.DefaultRouter()
router .register(r'pacientes', viewset=PacienteViewSet)   
router .register(r'medicos', viewset=MedicoViewSet)   
router .register(r'exames', viewset=ExameViewSet)
router .register(r'laudos', viewset=LaudoViewSet)
router .register(r'imagens', viewset=ImagemViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]