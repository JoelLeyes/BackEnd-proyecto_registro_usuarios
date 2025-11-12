from django.urls import path
from .views import UsuarioListCreateView

urlpatterns = [
    path('', UsuarioListCreateView.as_view(), name='usuario-list-create'),
]
