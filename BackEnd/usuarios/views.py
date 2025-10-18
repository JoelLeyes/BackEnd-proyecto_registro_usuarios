import os
import sys
from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer
from django.core.mail import send_mail
from django.conf import settings

# Ruta absoluta al repo de notificaciones
ruta_notificaciones = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Notificaciones-proyecto_registro_usuarios')
)

print("Ruta notificaciones:", ruta_notificaciones)  # para debug
sys.path.append(ruta_notificaciones)

from enviar_notificacion import enviar_notificacion

class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        usuario = serializer.save()

        # --- Llamar a la función del repo de notificaciones ---
        enviar_notificacion(usuario)
