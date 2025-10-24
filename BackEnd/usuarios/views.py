import os
from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer
from django.core.mail import send_mail
from django.conf import settings
import requests


class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        usuario = serializer.save()

        # Llamar al microservicio de notificaciones vía HTTP
        notify_url = os.environ.get('NOTIFICACIONES_URL', 'http://notificaciones:5001/notify')
        payload = {
            'nombre': usuario.nombre if hasattr(usuario, 'nombre') else getattr(usuario, 'name', ''),
            'email': usuario.email,
            'telefono': getattr(usuario, 'telefono', None),
        }
        try:
            resp = requests.post(notify_url, json=payload, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            # No queremos que falle la creación del usuario por un fallo en notificaciones;
            # logueamos el error para diagnosticarlo.
            print(f"Error al notificar: {e}")
