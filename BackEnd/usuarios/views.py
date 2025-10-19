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

        # En un entorno de microservicios llamamos al notification-service
        # mediante HTTP. La URL se toma de la variable de entorno
        # NOTIFICATION_SERVICE_URL (p. ej. http://notification-service:8000/notify)
        notif_url = os.environ.get(
            'NOTIFICATION_SERVICE_URL', 'http://notification-service:8000/notify'
        )

        payload = {
            'nombre': getattr(usuario, 'nombre', ''),
            'email': getattr(usuario, 'email', ''),
            'id': getattr(usuario, 'id', None),
        }

        try:
            resp = requests.post(notif_url, json=payload, timeout=5)
            if resp.status_code >= 400:
                print(f"[Warning] Notification service returned {resp.status_code}: {resp.text}")
        except Exception as exc:
            # No interrumpimos la creación del usuario si la notificación falla
            print(f"[Error] fallo al notificar a notification-service: {exc}")
