import os
from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer
import requests


class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        usuario = serializer.save()

        # --- URL del microservicio de notificaciones ---
        # Si no se definió una variable de entorno, usa el servicio Kubernetes interno
        default_url = 'http://notificaciones:5001/notify'
        notify_url = os.environ.get('NOTIFICACIONES_URL', default_url)

        # --- Datos del usuario para enviar ---
        payload = {
            'nombre': usuario.nombre,
            'email': usuario.email,
            'telefono': getattr(usuario, 'telefono', None),
        }

        # --- Enviar notificación ---
        try:
            resp = requests.post(notify_url, json=payload, timeout=5)
            resp.raise_for_status()
            print(f"✅ Notificación enviada correctamente a {usuario.email}")
        except Exception as e:
            print(f"⚠️ Error al notificar al microservicio: {e}")

